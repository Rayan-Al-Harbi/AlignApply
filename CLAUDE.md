# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AlignApply** is a tutorial project that uses an LLM (OpenAI GPT) to extract structured data from job descriptions and CVs, then align/match candidates to jobs.

## Running the Project

Requires an `OPENAI_API_KEY` environment variable set before running any script.

```bash
pip install openai pydantic
python main.py   # or whatever entry point is created
```

## Architecture

The project follows a three-layer pipeline:

1. **`model.py`** — Pydantic data models. Defines `JobProfile` (title, required_skills, preferred_skills, experience_level, responsibilities) and `CandidateProfile` (name, skills, experiences, education, summary), plus nested `Experience` and `Education` models.

2. **`prompt.py`** — Prompt templates. `JOB_EXTRACTION_PROMPT` and `CV_EXTRACTION_PROMPT` use `.format()` placeholders (`{job_description_text}`, `{cv_description_text}`) and instruct the LLM to return raw JSON only.

3. **`extraction.py`** — OpenAI API calls. `extract_job_profile(text)` and `extract_cv_profile(text)` format a prompt, call `gpt-4o-mini` at temperature 0, parse the JSON response, and return a validated Pydantic model instance. **Note:** `extraction.py` does not import from `model.py` or `prompt.py` — those names must be injected into its namespace before use (e.g., from `main.py`).

## Known Issue in extraction.py

`extraction.py` references `JobProfile`, `CandidateProfile`, `JOB_EXTRACTION_PROMPT`, and `CV_EXTRACTION_PROMPT` without importing them. When creating a `main.py` entry point, inject these after importing the module:

```python
from model import JobProfile, CandidateProfile
from prompt import JOB_EXTRACTION_PROMPT, CV_EXTRACTION_PROMPT
import extraction

extraction.JobProfile = JobProfile
extraction.CandidateProfile = CandidateProfile
extraction.JOB_EXTRACTION_PROMPT = JOB_EXTRACTION_PROMPT
extraction.CV_EXTRACTION_PROMPT = CV_EXTRACTION_PROMPT
```
