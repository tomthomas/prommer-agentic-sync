from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class TranscriptSegment(BaseModel):
    start_seconds: int = Field(..., description="Timestamp in seconds")
    end_seconds: int = Field(..., description="Timestamp in seconds")
    speaker: str = Field(default="Thomas Prommer")
    raw_text: str

class GroundedClaim(BaseModel):
    claim_summary: str = Field(..., description="Atomic POV statement or engineering takeaway")
    topic: str = Field(..., description="E.g., Agentic Architecture, AI Operations, Technical Leadership")
    quote: str = Field(..., description="Exact verifiably quoted words")
    timestamp_url: str = Field(..., description="Deep-link to YouTube second e.g. https://youtu.be/xyz?t=142")

class VerificationGateReport(BaseModel):
    is_valid: bool
    schema_passed: bool
    voice_drift_detected: bool
    rejection_reason: Optional[str] = None

class PublishedKnowledgeArticle(BaseModel):
    title: str
    slug: str
    published_date: str
    summary_150_words: str
    key_claims: List[GroundedClaim]
    json_ld_schema: dict
