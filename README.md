# RoverWranglingData (RWD)

A **production‑style Retrieval‑Augmented Generation (RAG) system** built from first principles.

This project is **not a demo chatbot**. It is a deliberately engineered RAG pipeline that emphasizes:

* Deterministic behavior
* Traceability & provenance
* Evaluation before generation
* Guardrails and fallbacks
* Agent‑aware (but non‑autonomous) decision layers

RWD is designed to resemble **real enterprise AI systems** used in regulated, high‑trust environments rather than prompt‑heavy prototypes.

---

## Why This Project Exists

Most RAG examples:

* Jump straight to LLM calls
* Hide failure cases
* Lack evaluation, metrics, and fallback logic
* Cannot explain *why* an answer was produced

**RoverWranglingData flips that order.**

Retrieval quality is measured **before** generation. Decisions are logged. Failures are explicit. LLM calls are controlled, not assumed.

---

## High‑Level Architecture

```
User Query
   ↓
Retrieval Pipeline (FAISS)
   ↓
Retrieval Metrics & Evaluation
   ↓
Guardrails & Failure Surfaces
   ↓
Deterministic Fallback OR
   ↓
LLM Generation (Controlled)
```

Optional agent‑aware layers sit **on top** of this pipeline without mutating the core.

---

## Tech Stack

* **Python 3.11+**
* **FAISS** (vector search)
* **NumPy**
* **Dataclasses** for structured metrics
* **Ollama** (local LLM provider)
* Modular, package‑based project layout

No cloud dependencies. No hidden services.

---

## Project Structure

```
RoverWranglingData/
│
├── rag_core/           # Core RAG pipeline
│   ├── ingest.py       # Document ingestion & chunking
│   ├── retriever.py    # FAISS retrieval logic
│   ├── metrics.py      # Retrieval metrics & evaluation
│   ├── guardrails.py   # Guardrail checks & failure detection
│   ├── generator.py   # Controlled LLM generation
│   ├── main.py         # Entry point
│
├── rag_jobs/           # Async / batch job simulations
├── notebooks/          # Exploratory analysis & experiments
├── fantasy_doc.txt     # Sample knowledge base (demo)
├── insight_forge_doc.txt
├── requirements.txt
├── install_all.ps1     # Windows setup helper
└── README.md
```

---

## Supported RAG Phases

| Phase   | Name                             | Status                |
| ------- | -------------------------------- | --------------------- |
| Phase 0 | Mental Model Alignment           | Complete              |
| Phase 1 | Core RAG Pipeline                | Complete              |
| Phase 2 | Retrieval Intelligence           | Complete & Frozen     |
| Phase 3 | Async System Design              | Complete & Frozen     |
| Phase 4 | Evaluation, Guardrails & Trust   | Complete & Frozen     |
| Phase 5 | Prompt‑Governed Decision Layer   | Design Only           |
| Phase 6 | Agent‑Aware RAG (Non‑Autonomous) | Design / Experimental |
| Phase 7 | Interview Weaponization          | Planned               |

---

## Setup Instructions (Local)

### 1️⃣ Prerequisites

* Python **3.11 or higher**
* Git
* Ollama installed locally

Verify:

```bash
python --version
ollama --version
```

---

### 2️⃣ Clone or Fork

```bash
git clone https://github.com/<your-username>/RoverWranglingData.git
cd RoverWranglingData
```

---

### 3️⃣ Create Virtual Environment

**Windows (PowerShell):**

```bash
python -m venv env
env\Scripts\activate
```

**macOS / Linux:**

```bash
python -m venv env
source env/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Install a Local LLM via Ollama

Example:

```bash
ollama pull llama3.1
```

You can change the model name in the config if needed.

---

## Running the Project

From the project root:
Ingestion and Retrival are decoupled for now, once final version is developed will be merged into one main.py
```bash
python -m rag_jobs.playground ## For ingesting a document
python -m rag_core.main_phase4 ## For retrieval and generation
```

Expected output includes:

* Retrieved chunk IDs
* Confidence scores
* Guardrail evaluation
* Either:

  * Deterministic fallback response
  * OR LLM‑generated answer with citations

---

## How Retrieval Evaluation Works

Each query produces structured metrics:

* **Mean confidence** of retrieved chunks
* **Confidence spread** (distribution quality)
* **Top‑K coverage**

These metrics determine whether:

* Generation is allowed
* A fallback is triggered
* A retry path is considered

No blind generation.

---

## Guardrails & Fallbacks

RWD explicitly detects:

* Low evidence coverage
* Over‑distributed confidence
* Weak retrieval signals

When triggered, the system:

* Avoids hallucination
* Returns safe, explainable responses
* Logs failure surfaces for auditability

---

## Agent‑Aware Design (Phase 6)

Agents in RWD are:

* **Non‑autonomous**
* **Prompt‑governed**
* **Read‑only over core pipeline**

They may:

* Condense evidence
* Justify decisions
* Recommend retries

They **cannot**:

* Modify retrieval logic
* Bypass guardrails
* Act independently

---

## Intended Audience

This project is for:

* Senior AI / ML Engineers
* Backend‑first AI developers
* System design interview preparation
* Engineers tired of prompt‑only demos

Not optimized for beginners or no‑code tools.

---

## Forking & Experimentation

You are encouraged to:

* Swap FAISS with pgvector
* Change chunking strategies
* Add new evaluation metrics
* Plug in cloud LLMs

But **do not remove evaluation layers** if you want to preserve the project philosophy.

---

Gray-Zone Test Description:

RWD may exhibit non-binary outcomes for the same query without any code or data changes. This behavior occurs when retrieval results lie near the semantic sufficiency boundary.

A representative example is the query:

“Who is Rover Wrangler and what struggles does he face in Aethelgard?”

In this case:

Retrieved chunks are highly relevant but fragmented

Evidence strongly supports struggles but only implicitly defines identity

Coverage metrics hover close to the LOW_COVERAGE threshold

Observed Behavior

Depending on how the LLM internally aggregates the same evidence:

Run A:
The system correctly rejects the query with
Insufficient evidence in retrieved context.

Run B:
The system produces a grounded answer using only cited chunks, while explicitly refusing unsupported details.

Both outcomes are considered valid and expected.

Why This Happens

This is not randomness or instability.

RWD operates deterministically but allows the LLM to make a final judgment on whether the retrieved context forms a minimally sufficient narrative to answer the question without hallucination.

This edge behavior typically occurs when:

Chunks are semantically overlapping

Declarative identity statements are weak or distributed

Evidence supports “what happened” more than “what is”

Design Rationale

RWD intentionally favors false rejection over false confidence.

When evidence quality is borderline, the system:

Preserves safety

Avoids hallucination

Surfaces uncertainty instead of smoothing it away

This mirrors real-world production RAG behavior rather than demo-grade pipelines.

Takeaway

Failures at the semantic boundary are signals, not bugs.

They indicate where data shape, not model logic, limits answerability.

---

## Disclaimer

This is a learning and demonstration project.

It intentionally prioritizes:

* Correctness over speed
* Transparency over convenience
* Engineering discipline over hype

---

## License

MIT License

---

## Final Note

If your RAG system cannot explain *why* it answered,
then it does not deserve to answer at all.

Happy wrangling.
