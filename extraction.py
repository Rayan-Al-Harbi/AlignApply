import logging
import time

from langsmith import traceable
from model import JobProfile, CandidateProfile
from prompt import JOB_EXTRACTION_PROMPT, CV_EXTRACTION_PROMPT
from utils import parse_llm_json, tracked_llm_call

logger = logging.getLogger("applycheck.extraction")


@traceable(name="job_extraction", metadata={"component": "extraction"})
def extract_job_profile(job_description_text: str) -> JobProfile:
    start = time.perf_counter()

    prompt = JOB_EXTRACTION_PROMPT.format(
        job_description_text=job_description_text
    )

    raw = tracked_llm_call(
        agent="analyzer",
        messages=[{"role": "user", "content": prompt}],
    )

    result = parse_llm_json(raw, JobProfile, agent="analyzer")

    logger.info("Job profile extracted", extra={"event_data": {
        "event": "llm_call",
        "function": "extract_job_profile",
        "latency_ms": round((time.perf_counter() - start) * 1000, 2),
        "title": result.title,
        "skills_count": len(result.required_skills),
    }})

    return result


@traceable(name="cv_extraction", metadata={"component": "extraction"})
def extract_cv_profile(cv_description_text: str) -> CandidateProfile:
    start = time.perf_counter()

    prompt = CV_EXTRACTION_PROMPT.format(
        cv_description_text=cv_description_text
    )

    raw = tracked_llm_call(
        agent="analyzer",
        messages=[{"role": "user", "content": prompt}],
    )

    result = parse_llm_json(raw, CandidateProfile, agent="analyzer")

    logger.info("CV profile extracted", extra={"event_data": {
        "event": "llm_call",
        "function": "extract_cv_profile",
        "latency_ms": round((time.perf_counter() - start) * 1000, 2),
        "name": result.name,
    }})

    return result
