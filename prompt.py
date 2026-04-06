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
- Extract each skill as a specific, evaluatable item — not a broad umbrella category.
  When a requirement lists sub-items (in parentheses, after a colon, or as examples), extract the sub-items individually.
  BAD:  "Software engineering" — too broad to evaluate.
  GOOD: "APIs", "Testing", "Reliability" — each can be checked against a CV.
- Include soft skills (communication, collaboration, leadership) and language proficiency when stated.
- Any skills listed under "nice to have", "preferred", "bonus", or similar sections go in preferred_skills, not required_skills.

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
- A direct technical synonym is a specific implementation of the evaluated skill (e.g., PostgreSQL, MySQL, SQLite → SQL; React, Vue → JavaScript).
- For broad foundational skills, match if the CV demonstrates proficiency through specific languages, frameworks, or projects that fall under that umbrella.
- Do not infer from loosely related technologies.
"""

SOFT_SKILL_EVAL_RULES = """
- Soft skills are rarely stated explicitly. You MUST infer them from behavioral evidence in the CV.
- Professional work experience is strong evidence. Building software in a team, maintaining services, collaborating across roles, holding multiple professional positions — all demonstrate soft skills in action.
- Do not require the exact skill name to appear in the CV. Look for actions and responsibilities that exercise the skill.
- Use your judgment to map actions to skills. If a responsibility or achievement would require exercising the evaluated skill, that counts as evidence.
- Mark matched if there is reasonable behavioral evidence. Explain your inference by citing the specific CV content.
"""

LANGUAGE_EVAL_RULES = """
- If the CV is written in this language, that is sufficient evidence.
- Also check for explicit language proficiency mentions.
"""


WRITER_PROMPT = """
You are a career advisor generating actionable CV improvements and a tailored cover letter for a candidate applying to a specific role.

Job Title: {title}
Job Responsibilities: {responsibilities}

Alignment Analysis:
{analysis}

Candidate CV:
{cv_text}

Return ONLY valid JSON matching this exact schema:
{{
    "cv_suggestions": [
        "string — a specific, actionable improvement to the candidate's CV"
    ],
    "cover_letter": "string — a complete, professional cover letter tailored to this role"
}}

Rules:
- Generate 3-6 CV suggestions. Each must be specific and reference concrete sections of the CV (e.g., "Skills section", "Experience at [company]", "Education").
- For missing skills: suggest adding them ONLY if the candidate has transferable experience. Do not suggest adding skills the candidate does not have.
- For matched skills with weak evidence: suggest how to strengthen the phrasing by referencing the specific experience from the evidence field above.
- Do not invent experience the candidate does not have.
- The cover letter must be professional, 3-4 paragraphs, and directly connect the candidate's strengths to the job requirements.
- Highlight matched skills as strengths. Acknowledge gaps honestly and frame them as areas of active growth.
- Do not use generic filler language. Every sentence should be specific to this candidate and role.
"""


SCORER_PROMPT = """
Score this job application across three dimensions.

Job Profile:
{job_profile}

Alignment Analysis:
{analysis}

Cover Letter:
{cover_letter}

Return ONLY valid JSON matching this schema:
{{
    "dimensions": [
        {{
            "dimension": "Skill Match",
            "score": 0,
            "weight": 0.35,
            "reasoning": "1-2 sentences explaining the score, referencing specific matched and missing skills."
        }},
        {{
            "dimension": "Experience Relevance",
            "score": 0,
            "weight": 0.35,
            "reasoning": "1-2 sentences on how directly the candidate's experience maps to the job responsibilities."
        }},
        {{
            "dimension": "Overall Presentation",
            "score": 0,
            "weight": 0.30,
            "reasoning": "1-2 sentences on the coherence and completeness of the candidate's profile relative to the role."
        }}
    ],
    "overall_score": 0,
    "summary": "2-3 sentence overall assessment addressed directly to the candidate using you/your."
}}

Rules:
- Score each dimension independently based on evidence, not impression.
- overall_score must equal the exact weighted average: sum of (score * weight) across all dimensions.
- Be honest and calibrated: a candidate missing 3 of 5 required skills should not score above 50 on Skill Match.
- 80+ means strong fit, 50-79 means partial fit with notable gaps, below 50 means weak fit.
- Skill Match scoring: use a two-step process. Step 1: compute a base score from the required skill match rate (matched_required / total_required * 100). Step 2: adjust based on preferred skills — each matched preferred skill adds a small bonus, missing most preferred skills subtracts a small penalty (up to ~10 points either way). Required skills should dominate this dimension; preferred skills are a secondary modifier. Do NOT average required and preferred together as equals.
- Reference specific skills, experiences, and cover letter content. No generic statements.
"""