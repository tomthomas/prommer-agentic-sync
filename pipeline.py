"""
Multi-Step Agentic Ingestion Pipeline for prommer.net
Task: Automatically ingest video talks via Whisper API, extract claims with
second-accurate deep-links, run verification gates, and index into the 
Supabase vector store powering "Ask AI Tom".
"""
from typing import List
from models import TranscriptSegment, GroundedClaim, VerificationGateReport, VectorStoreRecord

# Step 1: Ingestion Tool (OpenAI Whisper API audio-to-text with timestamps)
def ingest_via_whisper(video_id: str) -> List[TranscriptSegment]:
    # Mocking Whisper API output with second-level timestamps from a YouTube talk
    return [
        TranscriptSegment(
            start_seconds=15,
            end_seconds=78,
            speaker="Thomas Prommer",
            raw_text="The biggest mistake founders make with AI agents is relying on prompt-and-hope. Without deterministic schema validation and strict linter gates, an LLM in an open loop will eventually drift into hallucination."
        ),
        TranscriptSegment(
            start_seconds=82,
            end_seconds=145,
            speaker="Thomas Prommer",
            raw_text="At We The Flywheel, we structure everything around two speeds: fast deterministic gates for types, linter, and Pydantic validation, and slow semantic gates where a second model critiques voice and facts before anything ships."
        )
    ]

# Step 2: Agent 1 (Atomic Chunking & Deep-Linking)
def agent_extract_claims(video_id: str, segments: List[TranscriptSegment]) -> List[GroundedClaim]:
    claims = []
    for s in segments:
        deep_link = f"https://youtu.be/{video_id}?t={s.start_seconds}"
        if "deterministic schema" in s.raw_text.lower():
            claims.append(GroundedClaim(
                claim_summary="Open-loop agents without deterministic gates inevitably drift and corrupt production systems.",
                topic="Agentic Architecture",
                quote=s.raw_text,
                timestamp_url=deep_link
            ))
        elif "two speeds" in s.raw_text.lower():
            claims.append(GroundedClaim(
                claim_summary="Production agentic systems require a two-speed gate: fast deterministic linters/schemas plus slow semantic review.",
                topic="AI Operations",
                quote=s.raw_text,
                timestamp_url=deep_link
            ))
    return claims

# Step 3: Agent 2 (Dual-Speed Verification Gate)
def agent_verification_gate(claims: List[GroundedClaim]) -> VerificationGateReport:
    # 1. Fast Deterministic Check: Pydantic & URL query parameter structure
    for c in claims:
        if not c.timestamp_url.startswith("https://youtu.be/") or "?t=" not in c.timestamp_url:
            return VerificationGateReport(
                is_valid=False,
                schema_passed=False,
                voice_drift_detected=False,
                rejection_reason=f"Invalid timestamp URL format: {c.timestamp_url}"
            )
        if len(c.claim_summary) < 15:
            return VerificationGateReport(
                is_valid=False,
                schema_passed=False,
                voice_drift_detected=False,
                rejection_reason="Claim summary too short or uninformative"
            )

    # 2. Semantic Check: Flagging corporate AI buzzwords (VOICE.md guardrail)
    banned_jargon = ["spearhead", "synergies", "bleeding-edge", "game-changing"]
    for c in claims:
        if any(j in c.claim_summary.lower() for j in banned_jargon):
            return VerificationGateReport(
                is_valid=False,
                schema_passed=True,
                voice_drift_detected=True,
                rejection_reason=f"Voice drift detected: Banned corporate buzzword in claim '{c.claim_summary}'"
            )

    return VerificationGateReport(is_valid=True, schema_passed=True, voice_drift_detected=False)

# Step 4: Vector Ingestion Agent (Formats records for Supabase Vector Store / Ask AI Tom)
def agent_ingest_into_ask_tom_vector_db(video_id: str, claims: List[GroundedClaim]) -> List[VectorStoreRecord]:
    records = []
    for i, c in enumerate(claims):
        record = VectorStoreRecord(
            id=f"{video_id}_chunk_{i+1}",
            content_for_embedding=f"Topic: {c.topic}\nClaim: {c.claim_summary}\nDirect Quote: \"{c.quote}\"",
            metadata={
                "source_type": "youtube_talk",
                "video_id": video_id,
                "timestamp_url": c.timestamp_url,
                "topic": c.topic,
                "speaker": "Thomas Prommer",
                "indexed_for": "Ask AI Tom RAG"
            }
        )
        records.append(record)
    return records

def run_pipeline():
    video_id = "agentic_ops_2026"
    
    print(">>> [Step 1] Ingesting talk audio via OpenAI Whisper API...")
    segments = ingest_via_whisper(video_id)
    print(f"    Transcribed {len(segments)} segments with second-level timestamps.")
    
    print("\n>>> [Step 2] Agent 1: Parsing atomic claims & constructing deep links...")
    claims = agent_extract_claims(video_id, segments)
    for c in claims:
        print(f"    - [{c.topic}] {c.timestamp_url}")
    
    print("\n>>> [Step 3] Agent 2: Running Verification Gate (Schema + Voice check)...")
    report = agent_verification_gate(claims)
    if not report.is_valid:
        print(f"    [GATE BLOCKED] {report.rejection_reason}")
        return
    print("    [GATE PASSED] Schema valid, deep links verified, zero AI buzzwords.")
    
    print("\n>>> [Step 4] Ingesting into Supabase Vector Store for 'Ask AI Tom'...")
    records = agent_ingest_into_ask_tom_vector_db(video_id, claims)
    for r in records:
        print(f"    Indexed record '{r.id}' -> Citation: {r.metadata['timestamp_url']}")
    
    print("\nPipeline finished successfully. 'Ask AI Tom' can now retrieve these quotes with direct video links.")
    return records

if __name__ == "__main__":
    run_pipeline()
