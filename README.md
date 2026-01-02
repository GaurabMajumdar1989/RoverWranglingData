User Query
   ↓
Retrieval Pipeline (Vector Search)
   ↓
Retrieval Metrics & Evaluation
   ↓
Guardrails & Failure Surfaces
   ↓
Deterministic Fallback OR
   ↓
Controlled LLM Generation (with citations)

Tech Stack

Python 3.11+

FAISS for vector search

NumPy

Dataclasses for structured metrics

Ollama for local LLM execution

Modular, package-based project layout

No cloud dependencies.
No hidden services.
Everything runs locally and transparently.

RoverWranglingData/
│
├── rag_core/
│   ├── ingest.py            # Document ingestion & chunking
│   ├── retrieve.py          # Vector + hybrid retrieval
│   ├── embed.py             # Embedding logic
│   ├── store.py             # Vector store abstraction
│   ├── guardrails/
│   │   ├── evaluator.py     # Guardrail evaluation logic
│   │   ├── config.py        # Thresholds and limits
│   │   └── fallbacks.py     # Safe fallback responses
│   ├── agents/
│   │   ├── deterministic_agent.py
│   │   └── contracts.py
│   ├── tools/
│   │   └── condense_evidence.py
│   ├── llm/
│   │   └── generator.py
│   └── main_phase4.py       # Retrieval + generation entry point
│
├── tests/                   # Unit + integration tests (Phase 6)
│   ├── guardrails/
│   ├── agents/
│   ├── tools/
│   └── integration/
│
├── fantasy_doc.txt          # Sample knowledge base
├── pytest.ini
├── requirements.txt
└── README.md

| Phase | Description                           | Status                |
| ----: | ------------------------------------- | --------------------- |
|     0 | Mental Model Alignment                | Complete              |
|     1 | Core RAG Pipeline                     | Complete              |
|     2 | Retrieval Intelligence                | Complete & Frozen     |
|     3 | Async System Design                   | Complete & Frozen     |
|     4 | Evaluation, Guardrails & Trust        | Complete & Frozen     |
|     5 | Prompt-Governed Decision Layer        | Complete & Frozen     |
|     6 | Agent-Aware RAG (Non-Autonomous Core) | **Complete & Frozen** |

Setup Instructions (Local)
1️⃣ Prerequisites

Python 3.11+

Git

Ollama (local)

Verify:

python --version
ollama --version

2️⃣ Clone
git clone https://github.com/<your-username>/RoverWranglingData.git
cd RoverWranglingData

3️⃣ Virtual Environment

Windows

python -m venv env
env\Scripts\activate


macOS / Linux

python -m venv env
source env/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Install Local LLM (Ollama)

Example:

ollama pull llama3.1


Model name can be adjusted in configuration.

Running the System

Currently, ingestion and retrieval are intentionally decoupled.

python -m rag_jobs.playground     # Ingest documents
python -m rag_core.main_phase4    # Query, evaluate, generate


Expected output includes:

Retrieved chunk IDs

Retrieval confidence scores

Guardrail evaluation results

Either:

A deterministic fallback response

OR a grounded LLM answer with citations

Retrieval Evaluation Model

Each query produces structured metrics:

Mean confidence

Confidence spread

Top-K coverage

These metrics determine whether:

Generation is permitted

Evidence must be condensed

A safe fallback is required

There is no blind generation.

Guardrails & Safety

RWD explicitly detects:

Low evidence coverage

Over-diffuse evidence (high entropy)

Hallucination risk via query–evidence mismatch

When triggered, the system:

Rejects unsafe queries

Returns explainable fallbacks

Preserves trust over fluency

Failures are treated as signals, not bugs.

Agent-Aware Design (Phase 6)

Agents in RWD are:

Deterministic

Non-autonomous

Read-only over the core pipeline

They may:

Condense evidence

Recommend retries

Justify decisions

They cannot:

Modify retrieval logic

Bypass guardrails

Generate answers independently

This separation defines the trust boundary of the system.

Gray-Zone Behavior (By Design)

Some queries lie near the semantic sufficiency boundary.

Example:

“Who is Rover Wrangler and what struggles does he face in Aethelgard?”

In such cases:

Evidence may strongly support events but weakly support identity

Coverage may hover near thresholds

Valid outcomes include:

Safe rejection due to insufficient evidence

A grounded answer that explicitly refuses unsupported details

Both are correct.

This mirrors real production RAG behavior, not demo pipelines.

Intended Audience

This project is for:

Senior AI / ML Engineers

Backend-first AI developers

System-design interview preparation

Engineers tired of prompt-only demos

It is not optimized for beginners or no-code workflows.

Disclaimer

This is a learning and demonstration project.

It intentionally prioritizes:

Correctness over speed

Transparency over convenience

Engineering discipline over hype

Final Note

If your RAG system cannot explain why it answered,
then it does not deserve to answer at all.

Happy wrangling.

