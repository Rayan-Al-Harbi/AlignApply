from pydantic import BaseModel

# --- Job Description Models ---

class JobProfile(BaseModel):
    title: str
    required_skills: list[str]
    preferred_skills: list[str]
    experience_level: str
    responsibilities: list[str]


# --- CV / Candidate Models ---

class Experience(BaseModel):
    company: str
    role: str
    duration: str
    description: str


class Education(BaseModel):
    institution: str
    degree: str
    field: str


class CandidateProfile(BaseModel):
    name: str
    skills: list[str]
    experiences: list[Experience]
    education: list[Education]
    summary: str


