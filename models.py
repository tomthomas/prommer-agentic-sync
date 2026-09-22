from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TranscriptSegment(BaseModel):
    start_seconds: int = Field(..., description="Start timestamp from Whisper API")
    end_seconds: int = Field(..., description="End timestamp from Whisper API")
    speaker: str = Field(default="Thomas Prommer")
    raw_text: str

class GroundedClaim(BaseModel):
    claim_summary: str = Field(..., description="Atomic POV takeaway")
    topic: str = Field(..., description="E.g., Agentic Architecture, AI Operations")
    quote: str = Field(..., description="Verbatim quote from transcript")
    timestamp_url: str = Field(..., description="Deep-link to YouTube second e.g. https://youtu.be/xyz?t=15")

class VerificationGateReport(BaseModel):
    is_valid: bool
    schema_passed: bool
    voice_drift_detected: bool
    rejection_reason: Optional[str] = None

class VectorStoreRecord(BaseModel):
    id: str
    content_for_embedding: str
    metadata: Dict[str, Any]
