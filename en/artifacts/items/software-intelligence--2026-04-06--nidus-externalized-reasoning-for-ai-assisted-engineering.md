---
source: arxiv
url: http://arxiv.org/abs/2604.05080v1
published_at: '2026-04-06T18:32:09'
authors:
- Danil Gorinevski
topics:
- ai-software-engineering
- code-governance
- formal-verification
- llm-agents
- traceability
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Nidus: Externalized Reasoning for AI-Assisted Engineering

## Summary
Nidus is a governance runtime for AI-assisted software engineering that moves requirements, architecture, traceability, and verification into one solver-checked artifact. The paper’s main claim is that engineering discipline should be enforced by an external mechanism on every change, not left to LLM behavior.

## Problem
- LLM coding agents can produce code, but they do not reliably preserve engineering invariants such as requirement traceability, justified design decisions, and evidence for delivery.
- In safety-critical or high-assurance work, self-checking by the same model that proposed the change is weak assurance; the paper argues that verification must come from an external, decidable checker.
- Usual project state is split across tools like issue trackers, docs, spreadsheets, and CI logs, which makes it hard for agents to see and maintain the full engineering context.

## Approach
- Nidus stores the whole project as a single "living specification" in S-expressions: requirements, architecture, design, workflows, features, traces, proof obligations, coordination state, and imported organizational rules.
- Every proposed mutation is checked before it is saved. The kernel runs finite structural checks and SMT checks with Z3; failed changes are rejected with violations and UNSAT feedback.
- Organizational standards compile into reusable "guidebooks". A project imports them, and inherited constraints are enforced automatically alongside local proof obligations.
- The same artifact is read by humans, LLM agents, and the solver. The paper calls this representational closure: one object is the database, the model context, the spec, and the verifier input.
- The system also tracks agent claims with leases and an append-only friction ledger, then adjusts agent trust tiers based on rejection history.

## Results
- The paper reports a self-hosting deployment where three LLM families, Claude, Gemini, and Codex, delivered a **100,000-line** system under proof obligations checked on **every commit**.
- It claims recursive self-governance: the system governed changes to its own governing artifact during its construction.
- It gives one concrete verification example: a feature delivery is rejected because guidebook constraint **GC-SCOPE-COMPLETENESS** finds missing test paths; Z3 returns **UNSAT**, the agent adds `tests/test_brain.py`, and the delivery then passes.
- It states formal verification cost per mutation as **O(|Π| · |S|)**, with graph checks at **O(|C| + |E| + |T|)**, schema checks at **O(|F|)**, and workflow arithmetic solved in polynomial time for fixed-size guards.
- The excerpt does **not** provide benchmark metrics such as defect rate, pass rate, latency, ablations, or comparison against a baseline toolchain.

## Link
- [http://arxiv.org/abs/2604.05080v1](http://arxiv.org/abs/2604.05080v1)
