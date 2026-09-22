"""
Multi-Step Agentic Ingestion Pipeline for prommer.net
Task: Automatically extract, verify, and syndicate executive video talks into 
"Ask AI Tom" RAG vector store and Astro static knowledge base.
"""
import json
import re
from typing import List, Dict
from models import TranscriptSegment, GroundedClaim, VerificationGateReport, PublishedKnowledgeArticle

# Step 1: Ingestion Tool (Extract raw transcript with timestamps)
def ingest_raw_talk(video_id: str) -> List[TranscriptSegment]:
    # Mocking sample raw transcript segments from a Thomas Prommer YouTube talk on Agentic Engineering
    return [
        TranscriptSegment(
            start_seconds=15,
            end_seconds=78,
            speaker="Thomas Prommer",
            raw_text="The biggest mistake founders make with AI agents is relying on prompt-and-hope. If you don't have deterministic schema validation and strict linter gates, an LLM in an open loop will eventually destroy your production database or drift into hallucination."
        ),
        TranscriptSegment(
            start_seconds=82,
            end_seconds=145,
            speaker="Thomas Prommer",
            raw_text="At We The Flywheel, we structure everything around two speeds: fast deterministic gates for types, linter, and Pydantic validation, and slow semantic gates where a second model critiques voice and facts before any code or content ships."
        )
    ]

# Step 2: Agent 1 (Entity & Claim Extraction with Timestamp Deep-Linking)
def agent_extract_claims(video_id: str, segments: List[TranscriptSegment]) -> List[GroundedClaim]:
    claims = []
    for s in segments:
        deep_link = f"https://youtu.be/{video_id}?t={s.start_seconds}"
        # Extract atomic claim
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

# Step 3: Agent 2 (Deterministic Schema + Semantic Voice Verification Gate)
def agent_verification_gate(claims: List[GroundedClaim], voice_rules_path: str = "VOICE.md") -> VerificationGateReport:
    # Deterministic Schema Check
    for c in claims:
        if not c.timestamp_url.startswith("https://youtu.be/"):
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
                rejection_reason="Claim summary too short or lacks substantive POV"
            )

    # Voice & Jargon Check (Anti-AI Fluff)
    banned_jargon = ["spearhead", "synergies", "bleeding-edge", "game-changing"]
    for c in claims:
        if any(j in c.claim_summary.lower() for j in banned_jargon):
            return VerificationGateReport(
                is_valid=False,
                schema_passed=True,
                voice_drift_detected=True,
                rejection_reason=f"Voice drift detected: Banned corporate jargon in claim '{c.claim_summary}'"
            )

    return VerificationGateReport(is_valid=True, schema_passed=True, voice_drift_detected=False)

# Step 4: Publisher Agent (Formats Astro Markdown & Google Entity JSON-LD)
def agent_publish_knowledge(video_id: str, title: str, claims: List[GroundedClaim]) -> PublishedKnowledgeArticle:
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    
    # Generate JSON-LD for Google Knowledge Graph / Entity Search
    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "author": {
            "@type": "Person",
            "name": "Thomas Prommer",
            "url": "https://prommer.net"
        },
        "citation": [c.timestamp_url for c in claims]
    }
    
    summary = (
        f"In this talk, Thomas Prommer details the operational necessity of deterministic validation gates "
        f"in production agentic workflows, contrasting ungrounded prompt loops with dual-speed verification architectures."
    )
    
    return PublishedKnowledgeArticle(
        title=title,
        slug=slug,
        published_date="2026-09-22",
        summary_150_words=summary,
        key_claims=claims,
        json_ld_schema=json_ld
    )

def run_pipeline():
    video_id = "agentic_ops_2026"
    title = "Why Open-Loop AI Agents Fail Without Deterministic Gates"
    
    print(">>> [Step 1] Ingesting talk audio transcript...")
    segments = ingest_raw_talk(video_id)
    print(f"    Ingested {len(segments)} segments with exact timestamps.")
    
    print("\n>>> [Step 2] Agent 1: Extracting atomic claims & deep-link citations...")
    claims = agent_extract_claims(video_id, segments)
    print(f"    Extracted {len(claims)} verified claims.")
    
    print("\n>>> [Step 3] Agent 2: Running Verification Gate (Schema + Voice + Jargon Check)...")
    report = agent_verification_gate(claims)
    if not report.is_valid:
        print(f"    [GATE BLOCKED] Pipeline halted: {report.rejection_reason}")
        return
    print("    [GATE PASSED] 100% schema validation & zero voice drift.")
    
    print("\n>>> [Step 4] Publisher: Generating Astro static markdown & JSON-LD...")
    article = agent_publish_knowledge(video_id, title, claims)
    print(f"    Article '{article.title}' ready for static merge.")
    print("    JSON-LD Entity Citations generated successfully.")
    
    # Write sample markdown output
    output_md = f"""---
title: "{article.title}"
date: "{article.published_date}"
slug: "{article.slug}"
author: "Thomas Prommer"
---

# {article.title}

{article.summary_150_words}

## Key Citations & Timestamps
"""
    for c in article.key_claims:
        output_md += f"\n- **{c.topic}**: \"{c.claim_summary}\" ([Listen at timestamp]({c.timestamp_url}))\n"

    print("\n--- Output Artifact Preview ---\n" + output_md)
    return article

if __name__ == "__main__":
    run_pipeline()
