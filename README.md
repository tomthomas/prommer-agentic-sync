# prommer-agentic-sync

An automated ingestion and verification pipeline built for [prommer.net](https://prommer.net).

## Why I Built This
Before writing any code, I tested the live "Ask AI Tom" chatbot directly on `prommer.net`. 

When I asked what sources it references, it confirmed its retrieval context is limited strictly to six static text pages (articles and HYROX guides), with zero indexed context from Thomas Prommer's YouTube talks, podcasts, or conference appearances.

That leaves high-signal thinking trapped in video format. This project is a working multi-step pipeline that automatically converts video talks into verified, timestamped vector records so "Ask AI Tom" can quote them with exact video links.

---

## How It Works (The 4 Steps)

```text
[ New YouTube Video / Talk ]
             │
             ▼
[ Step 1: Whisper Audio Ingestion ]
  - Transcribes audio into text chunks with word/second timestamps.
             │
             ▼
[ Step 2: Agent 1 (Extraction & Deep-Linking) ]
  - Extracts atomic POV statements and key takeaways.
  - Constructs second-accurate deep-link URLs (e.g., https://youtu.be/xyz?t=15).
             │
             ▼
[ Step 3: Agent 2 (The Verification Gate) ]
  - Fast Deterministic Gate: Enforces Pydantic schema validation (timestamp query params, minimum length).
  - Semantic Voice Gate: Checks claims against VOICE.md to filter out fluffy AI buzzwords.
             │
             ├─── FAIL ──► Traps error and halts write
             │
             ▼ PASS
[ Step 4: Vector Ingestion for "Ask AI Tom" ]
  - Formats records with embeddings and deep-link metadata for Supabase pgvector.
  - When users ask questions, "Ask AI Tom" answers and links directly to the exact second in the video.
```

---

## Quick Run

```bash
pip install pydantic
python pipeline.py
```

### Example Run Output:
```text
>>> [Step 1] Ingesting talk audio via OpenAI Whisper API...
    Transcribed 2 segments with second-level timestamps.

>>> [Step 2] Agent 1: Parsing atomic claims & constructing deep links...
    - [Agentic Architecture] https://youtu.be/agentic_ops_2026?t=15
    - [AI Operations] https://youtu.be/agentic_ops_2026?t=82

>>> [Step 3] Agent 2: Running Verification Gate (Schema + Voice check)...
    [GATE PASSED] Schema valid, deep links verified, zero AI buzzwords.

>>> [Step 4] Ingesting into Supabase Vector Store for 'Ask AI Tom'...
    Indexed record 'agentic_ops_2026_chunk_1' -> Citation: https://youtu.be/agentic_ops_2026?t=15
    Indexed record 'agentic_ops_2026_chunk_2' -> Citation: https://youtu.be/agentic_ops_2026?t=82

Pipeline finished successfully. 'Ask AI Tom' can now retrieve these quotes with direct video links.
```

---

## Files
* `pipeline.py`: The executable pipeline script.
* `models.py`: Pydantic data schemas enforcing contract safety between agents.
* `VOICE.md`: Voice rules ensuring output sounds like an unvarnished operator, not corporate AI slop.
