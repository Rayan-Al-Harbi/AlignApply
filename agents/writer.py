import json
import os
from groq import Groq
from model import AlignmentAnalysis
from prompt import WRITER_PROMPT

client = Groq(api_key=os.environ["GROQ_API_KEY"])


def _format_analysis(analysis: AlignmentAnalysis) -> str:
    matched_section = "\n".join(
        f"- {m.skill} (MATCHED — evidence: {m.evidence})"
        for m in analysis.matched_skills
    )
    missing_section = "\n".join(
        f"- {skill}" for skill in analysis.missing_skills
    )
    return f"MATCHED SKILLS:\n{matched_section or 'none'}\n\nMISSING SKILLS:\n{missing_section or 'none'}"


def writer_node(state) -> dict:
    job_profile = state.job_profile
    analysis = state.alignment_analysis
    cv_text = state.cv_text

    prompt = WRITER_PROMPT.format(
        title=job_profile.title,
        responsibilities="\n".join(f"- {r}" for r in job_profile.responsibilities),
        analysis=_format_analysis(analysis),
        overall_fit=analysis.overall_fit,
        cv_text=cv_text,
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    raw = response.choices[0].message.content.strip().strip("```json").strip("```").strip()
    parsed = json.loads(raw, strict=False)

    return {
        "cv_suggestions": parsed["cv_suggestions"],
        "cover_letter": parsed["cover_letter"],
        "current_agent": "scorer",
    }
