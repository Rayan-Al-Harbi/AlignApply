# api/schemas.py

from pydantic import BaseModel


# --- Request ---

class AnalyzeRequest(BaseModel):
    job_description: str
    cv_text: str


# --- Response sub-models ---

class SkillMatchResponse(BaseModel):
    skill: str
    matched: bool
    evidence: str


class AnalysisResponse(BaseModel):
    matched_skills: list[SkillMatchResponse]
    missing_skills: list[str]
    overall_fit: str


class DimensionScoreResponse(BaseModel):
    dimension: str
    score: float
    weight: float
    reasoning: str


class ScoreResponse(BaseModel):
    dimensions: list[DimensionScoreResponse]
    overall_score: float
    summary: str


class AnalyzeResponse(BaseModel):
    job_title: str
    analysis: AnalysisResponse
    cv_suggestions: list[str]
    cover_letter: str
    score: ScoreResponse