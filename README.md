# prommer-agentic-sync

A multi-step agentic ingestion and verification pipeline for [prommer.net](https://prommer.net).

## The Core Problem Addressed
When querying the production "Ask AI Tom" chatbot directly on `prommer.net`, it confirmed that its retrieval context is limited strictly to six static text pages, leaving Thomas Prommer's extensive video talks, interviews, and podcast appearances unindexed. 

This repository implements an automated, multi-step pipeline to ingest raw executive talk transcripts, extract atomic claims with second-accurate deep-link citations, run deterministic schema and voice validation gates, and emit Astro-ready static content and Google Entity JSON-LD.

---

## The Workflow Architecture

```text
[ Raw Talk Audio / Transcript ]
             │
             ▼
[ Step 1: Ingestion & Parsing ]
  - Extracts timestamped transcript segments (start/end seconds)
             │
             ▼
[ Step 2: Agent 1 (Extraction & Deep-Linking) ]
  - Identifies atomic POV statements and takeaways
  - Constructs exact deep-link timestamp URLs (e.g., https://youtu.be/xyz?t=15)
             │
             ▼
[ Step 3: Agent 2 (Verification Gate) ]
  - Fast Deterministic Gate: Enforces Pydantic model validation (valid timestamp formatting, minimum claim length)
  - Semantic Voice Gate: Cross-references VOICE.md to filter out corporate AI buzzwords
             │
             ├─── FAIL ──► Emits structured error report & halts downstream write
             │
             ▼ PASS
[ Step 4: Publisher Agent ]
  - Formats Astro-compatible static markdown with deep-link citations
  - Generates Schema.org TechArticle JSON-LD for Google Knowledge Graph ingestion
```

---

## File Structure
* `pipeline.py`: The executable multi-step agent pipeline.
* `models.py`: Pydantic data schemas enforcing contract safety between agents.
* `VOICE.md`: Operator voice standards and anti-AI-slop rules for prommer.net.

---

## Running the Pipeline
```bash
pip install pydantic
python pipeline.py
```
