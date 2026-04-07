import logging
import re
import time

from model import AlignmentAnalysis, JobProfile, ScorerOutput
from prompt import SCORER_PROMPT
from utils import parse_llm_json, tracked_llm_call
from api.metrics import AGENT_LATENCY, PIPELINE_ERROR_COUNT, SCORE_DISTRIBUTION, SKILLS_MATCHED

logger = logging.getLogger("applycheck.scorer")


def _format_job_profile(job_profile: JobProfile) -> str:
    lines = [
        f"Title: {job_profile.title}",
        f"Experience Level: {job_profile.experience_level}",
        f"Required Skills: {', '.join(job_profile.required_skills)}",
    ]
    if job_profile.preferred_skills:
        lines.append(f"Preferred Skills: {', '.join(job_profile.preferred_skills)}")
    lines.append("Responsibilities:\n" + "\n".join(f"  - {r}" for r in job_profile.responsibilities))
    return "\n".join(lines)


def _format_analysis(analysis: AlignmentAnalysis) -> str:
    matched_section = "\n".join(
        f"  - {m.skill} (MATCHED — evidence: {m.evidence})"
        for m in analysis.matched_skills
    )
    missing_section = "\n".join(f"  - {skill}" for skill in analysis.missing_skills)

    req_matched = len(analysis.matched_skills)
    req_total = req_matched + len(analysis.missing_skills)

    lines = [
        f"Required Skills — {req_matched}/{req_total} matched:",
        f"  Matched:\n{matched_section or '    none'}",
        f"  Missing:\n{missing_section or '    none'}",
    ]

    if analysis.matched_preferred or analysis.missing_preferred:
        pref_matched_count = len(analysis.matched_preferred)
        pref_total = pref_matched_count + len(analysis.missing_preferred)
        pref_matched = "\n".join(
            f"  - {m.skill} (MATCHED — evidence: {m.evidence})"
            for m in analysis.matched_preferred
        )
        pref_missing = "\n".join(f"  - {skill}" for skill in analysis.missing_preferred)
        lines.append(f"\nPreferred Skills — {pref_matched_count}/{pref_total} matched:")
        lines.append(f"  Matched:\n{pref_matched or '    none'}")
        lines.append(f"  Missing:\n{pref_missing or '    none'}")

    return "\n".join(lines)


def _job_requires_experience_years(experience_level: str) -> bool:
    """Check if the job profile specifies a concrete number of years."""
    if not experience_level:
        return False
    return bool(re.search(r'\d+\s*\+?\s*(?:year|yr)', experience_level, re.IGNORECASE))


def _format_experience_summary(experiences: list[dict]) -> str:
    """Format experience durations from LLM-extracted CV profile."""
    if not experiences:
        return "No professional experience listed"
    professional = [e for e in experiences if e.get("type", "professional") == "professional"]
    other = [e for e in experiences if e.get("type", "professional") != "professional"]
    lines = []
    if professional:
        lines.append(f"Professional experience — {len(professional)} position(s):")
        lines.extend(f"  - {e.get('role', 'Role')} at {e.get('company', 'Company')} ({e.get('duration', 'unknown duration')})" for e in professional)
    else:
        lines.append("Professional experience — none")
    if other:
        lines.append(f"Non-professional (academic/extracurricular) — {len(other)} position(s):")
        lines.extend(f"  - {e.get('role', 'Role')} at {e.get('company', 'Company')} ({e.get('duration', 'unknown duration')}, {e.get('type', 'other')})" for e in other)
    return "\n".join(lines)


def rescore(job_profile: JobProfile, analysis: AlignmentAnalysis, cover_letter: str, candidate_experience: str = "Not available") -> ScorerOutput:
    """Standalone rescore — used by the UI when the user disputes missing skills."""
    prompt = SCORER_PROMPT.format(
        job_profile=_format_job_profile(job_profile),
        analysis=_format_analysis(analysis),
        cover_letter=cover_letter,
        candidate_experience=candidate_experience,
    )
    raw = tracked_llm_call(
        agent="scorer",
        messages=[{"role": "user", "content": prompt}],
    )
    return parse_llm_json(raw, ScorerOutput, agent="scorer")


def scorer_node(state) -> dict:
    trace_id = state.trace_id
    start = time.perf_counter()

    logger.info("Scorer started", extra={"event_data": {
        "event": "agent_start",
        "agent": "scorer",
        "trace_id": trace_id,
    }})

    try:
        job_profile = state.job_profile
        analysis = state.alignment_analysis
        cover_letter = state.cover_letter

        # Only include candidate experience when the job specifies years
        if _job_requires_experience_years(job_profile.experience_level) and state.cv_experiences:
            candidate_experience = _format_experience_summary(state.cv_experiences)
        else:
            candidate_experience = "Not specified by the job — do not evaluate experience gap"

        prompt = SCORER_PROMPT.format(
            job_profile=_format_job_profile(job_profile),
            analysis=_format_analysis(analysis),
            cover_letter=cover_letter,
            candidate_experience=candidate_experience,
        )

        raw = tracked_llm_call(
            agent="scorer",
            messages=[{"role": "user", "content": prompt}],
        )

        logger.info("Scorer LLM call complete", extra={"event_data": {
            "event": "llm_call",
            "agent": "scorer",
            "trace_id": trace_id,
        }})

        scorer_output = parse_llm_json(raw, ScorerOutput, agent="scorer")

        # Track score and skills-match ratio
        SCORE_DISTRIBUTION.observe(scorer_output.overall_score)
        total_skills = len(analysis.matched_skills) + len(analysis.missing_skills)
        if total_skills > 0:
            ratio = len(analysis.matched_skills) / total_skills
            SKILLS_MATCHED.observe(ratio)

        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info("Scorer complete", extra={"event_data": {
            "event": "agent_complete",
            "agent": "scorer",
            "trace_id": trace_id,
            "overall_score": scorer_output.overall_score,
            "latency_ms": round(elapsed_ms, 2),
        }})

        return {
            "scorer_output": scorer_output,
            "is_complete": True,
        }
    except Exception:
        PIPELINE_ERROR_COUNT.labels(agent="scorer").inc()
        raise
    finally:
        AGENT_LATENCY.labels(agent="scorer").observe(time.perf_counter() - start)
