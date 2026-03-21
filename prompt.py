JOB_EXTRACTION_PROMPT = """
You are a job description parser. Extract structured information from the following job description.

Return ONLY valid JSON matching this exact schema:
{{
    "title": "string",
    "required_skills": ["string"],
    "preferred_skills": ["string"],
    "experience_level": "string",
    "responsibilities": ["string"]
}}

Rules:
- If a field is not found, use an empty string or empty list as appropriate.
- Do not invent information. Only extract what is explicitly stated.
- Skills should be concise (e.g., "Python", "Project Management", "AWS").

Job Description:
{job_description_text}
"""


CV_EXTRACTION_PROMPT = """
You are a CV qualification parser. Extract structured information from the following CV.

Return ONLY valid JSON matching this exact schema:
{{
    "name": "string",
    "skills": ["string"],
    "experiences": [
        {{
            "company": "string",
            "role": "string",
            "duration": "string",
            "description": "string"
        }}
    ],
    "education": [
        {{
            "institution": "string",
            "degree": "string",
            "field": "string"
        }}
    ],
    "summary": "string"
}}

Rules:
- If a field is not found, use an empty string or empty list as appropriate.
- Do not invent information. Only extract what is explicitly stated.
- Skills should be concise (e.g., "Python", "Project Management", "AWS").

CV Description:
{cv_description_text}
"""