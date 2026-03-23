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

SKILL_EVAL_PROMPT = """
You are evaluating whether a candidate has a specific skill based on their CV.

Skill to evaluate: {skill}

Relevant CV sections:
{context}

Return ONLY valid JSON:
{{
    "skill": "{skill}",
    "matched": true or false,
    "evidence": "Direct quote or paraphrase from the CV that supports your judgment. If no evidence found, write 'No relevant evidence in CV.'"
}}

Evaluation rules:
{rules}
"""



OVERALL_FIT_PROMPT = """
You are summarizing a candidate's fit for a job.

Job title: {title}
Matched skills: {matched_list}
Missing skills: {missing_list}

Write a 2-3 sentence summary of the candidate's alignment with this role.
Be specific and honest. Do not use generic filler language.

Return ONLY the summary text, no JSON.
"""


SKILL_CLASSIFIER_PROMPT = """
Classify each skill as "hard", "soft", or "language".

- hard: technical skills, tools, programming languages, frameworks
- soft: interpersonal, cognitive, or behavioral skills
- language: spoken/written human languages

Skills: {skills}

Return ONLY valid JSON:
{{
    "classifications": [
        {{"skill": "Python", "type": "hard"}},
        {{"skill": "Communication", "type": "soft"}}
    ]
}}
"""


HARD_SKILL_EVAL_RULES = """
- Only mark matched if the skill is explicitly mentioned or a direct technical synonym exists.
- A direct technical synonym is a specific implementation of the skill (e.g., PostgreSQL, MySQL, SQLite → SQL; React, Vue → JavaScript).
- For broad foundational skills (e.g., "Programming concepts", "Software development"), match if the CV demonstrates proficiency through specific languages, frameworks, or projects.
- Do not infer from loosely related technologies.
"""

SOFT_SKILL_EVAL_RULES = """
- Soft skills are rarely stated explicitly.
- Infer from responsibilities and achievements described in the CV.
- "Built and maintained microservices" implies problem-solving.
- "Worked across teams" or any collaborative work implies communication.
- Mark matched if there is reasonable evidence, and explain your inference.
"""

LANGUAGE_EVAL_RULES = """
- If the CV is written in this language, that is sufficient evidence.
- Also check for explicit language proficiency mentions.
"""