from enum import Enum
from pydantic import BaseModel, model_validator

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


# --- Alignment Analysis Models ---

class SkillType(str, Enum):
    HARD = "hard"
    SOFT = "soft"
    LANGUAGE = "language"


class _SkillClassificationItem(BaseModel):
    skill: str
    type: SkillType


class SkillClassifierOutput(BaseModel):
    classifications: list[_SkillClassificationItem]



class SkillMatch(BaseModel):
    skill: str
    matched: bool
    evidence: str  # the CV chunk or quote that supports the judgment


class AlignmentAnalysis(BaseModel):
    matched_skills: list[SkillMatch]
    missing_skills: list[str]
    overall_fit: str  # brief narrative summary


# --- Scorer Models ---

class DimensionScore(BaseModel):
    dimension: str
    score: float  # 0-100
    weight: float
    reasoning: str


class ScorerOutput(BaseModel):
    dimensions: list[DimensionScore]
    overall_score: float
    summary: str

    @model_validator(mode="after")
    def enforce_weighted_average(self):
        expected = round(sum(d.score * d.weight for d in self.dimensions), 1)
        if abs(self.overall_score - expected) > 2.0:
            self.overall_score = expected
        return self
