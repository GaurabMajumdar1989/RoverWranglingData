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
