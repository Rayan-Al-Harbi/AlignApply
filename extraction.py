import json
import os
from groq import Groq
from model import JobProfile, CandidateProfile
from prompt import JOB_EXTRACTION_PROMPT, CV_EXTRACTION_PROMPT

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def extract_job_profile(job_description_text: str) -> JobProfile:
    prompt = JOB_EXTRACTION_PROMPT.format(
        job_description_text=job_description_text
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw_output = response.choices[0].message.content.strip().strip("```json").strip("```").strip()
    parsed = json.loads(raw_output)
    return JobProfile(**parsed)



def extract_cv_profile(cv_description_text: str) -> CandidateProfile:
    prompt = CV_EXTRACTION_PROMPT.format(
        cv_description_text=cv_description_text
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw_output = response.choices[0].message.content.strip().strip("```json").strip("```").strip()
    parsed = json.loads(raw_output)
    return CandidateProfile(**parsed)