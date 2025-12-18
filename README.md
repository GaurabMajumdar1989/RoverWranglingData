# RoverWranglingData (RWD)

## A Governed, Asynchronous RAG System with Agent-Constrained Decisioning

---

## Overview

RoverWranglingData (RWD) is a production-oriented Retrieval-Augmented Generation (RAG) system designed with engineering rigor over agentic hype.

The project demonstrates how to build:

- An asynchronous, fault-aware RAG pipeline
- Deterministic retrieval evaluation and guardrails
- Agent-like decision logic that is governed, auditable, and non-autonomous
- Enterprise-grade traceability, retry discipline, and accountability

RWD intentionally avoids uncontrolled autonomous agents.  
Instead, it showcases how agents should exist in real systems: constrained, explainable, and subordinate to the pipeline.

---

## Core Design Principles

- Determinism before intelligence
- Metrics before opinions
- Pipelines before agents
- Governance before autonomy

Every response produced by the system is:

- Grounded in retrieved evidence
- Evaluated using explicit metrics
- Routed using deterministic rules
- Logged with immutable provenance

---

## System Capabilities

### Phase 1–2: Core RAG Pipeline

- Document ingestion and chunking
- Embedding generation
- Vector-based retrieval
- Ranked evidence selection

### Phase 3: Asynchronous Architecture

- Job-based document processing
- Background workers with heartbeat and status tracking
- Query-time decoupling from ingestion
- Safe handling of partial and in-progress data

### Phase 4: Evaluation, Guardrails & Trust

- Retrieval quality metrics:
  - Mean confidence
  - Confidence spread
  - Top-K coverage
- Deterministic guardrails
- Failure surface detection
- Safe, explainable fallbacks
- No LLM-based judging

### Phase 5: Governed Decision Agents (Non-Autonomous)

- Deterministic decision routing
- Prompt-governed justification (read-only LLM use)
- Single bounded retry with confidence-aware re-prompting
- Immutable decision provenance and audit trails

Agents in RWD cannot:

- Re-run retrieval
- Override guardrails
- Change metrics
- Access tools
- Escalate authority

---

## High-Level Architecture

User Query
↓
Retrieval Layer (Vector Search)
↓
Evaluation & Guardrails
↓
Decision Agent (Rule-Based)
↓
Justification (Read-Only LLM)
↓
Response Generation
↓
Provenance & Audit Log

---

## Agent Philosophy

In RWD, agents are not decision-makers.

They:

- Route decisions
- Explain outcomes
- Operate under strict constraints

They do not:

- Act autonomously
- Modify system state
- Override pipeline guarantees

This mirrors real-world enterprise AI systems.

---

## What This Project Demonstrates

- Deep understanding of RAG failure modes
- Asynchronous system design maturity
- Metric-driven evaluation
- Controlled use of LLMs
- Agent governance and accountability
- Engineering restraint over hype

This is not a toy project.  
It is a senior-level AI systems design artifact.

---

## Future Work (Intentionally Excluded)

- Autonomous agent loops
- Tool-using agents
- Self-modifying pipelines

These are intentionally excluded to preserve system discipline and trust.

---

## Final Note

RoverWranglingData is built to answer one question clearly:

"Can AI systems be both powerful and trustworthy?"

This repository answers yes — with evidence.
