import logging
import time

from model import AlignmentAnalysis, JobProfile, ScorerOutput
from prompt import SCORER_PROMPT
from utils import parse_llm_json, tracked_llm_call
from api.metrics import AGENT_LATENCY, PIPELINE_ERROR_COUNT, SCORE_DISTRIBUTION, SKILLS_MATCHED

logger = logging.getLogger("applycheck.scorer")


def _format_job_profile(job_profile: JobProfile) -> str:
    return (
        f"Title: {job_profile.title}\n"
        f"Experience Level: {job_profile.experience_level}\n"
        f"Required Skills: {', '.join(job_profile.required_skills)}\n"
        f"Responsibilities:\n" + "\n".join(f"  - {r}" for r in job_profile.responsibilities)
    )


def _format_analysis(analysis: AlignmentAnalysis) -> str:
    matched_section = "\n".join(
        f"  - {m.skill} (MATCHED — evidence: {m.evidence})"
        for m in analysis.matched_skills
    )
    missing_section = "\n".join(f"  - {skill}" for skill in analysis.missing_skills)
    return (
        f"Matched Skills:\n{matched_section or '  none'}\n\n"
        f"Missing Skills:\n{missing_section or '  none'}\n\n"
        f"Overall Fit: {analysis.overall_fit}"
    )


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

        prompt = SCORER_PROMPT.format(
            job_profile=_format_job_profile(job_profile),
            analysis=_format_analysis(analysis),
            cover_letter=cover_letter,
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
