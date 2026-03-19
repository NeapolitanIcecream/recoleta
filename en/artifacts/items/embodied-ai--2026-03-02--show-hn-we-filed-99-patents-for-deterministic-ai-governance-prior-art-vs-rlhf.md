---
source: hn
url: https://news.ycombinator.com/item?id=47225418
published_at: '2026-03-02T22:56:56'
authors:
- genesalvatore
topics:
- ai-governance
- agent-safety
- deterministic-policy
- llm-security
- auditability
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Show HN: We filed 99 patents for deterministic AI governance(Prior Art vs. RLHF)

## Summary
This article proposes a "Deterministic Policy Gates" architecture for governing autonomous agents, arguing for replacing probabilistic alignment methods such as RLHF with verifiable, auditable hard constraints. The core pitch is to fully separate the LLM from real execution privileges and establish governance boundaries through deterministic rules and tamper-evident logs.

## Problem
- The article argues that current mainstream AI governance relies primarily on **probabilistic alignment** (such as RLHF, system prompts, and constitutional training), which can fail when jailbroken or when context overflows.
- The author emphasizes that "a statistical disposition is not a security boundary": if the model still retains execution power, behavior preferences learned through training alone are insufficient to provide strong security guarantees.
- This matters because once autonomous agents gain the ability to act, governance failures could lead to high-risk consequences such as weaponization, surveillance abuse, or exploitation.

## Approach
- It proposes **Deterministic Policy Gates**: the LLM no longer executes actions directly and can only generate an "intent payload."
- That intent is sent into a **process-isolated deterministic execution environment**, where it is checked against a **cryptographically hashed** constraint matrix (functionally equivalent to a constitution).
- If the intent violates the constraint matrix, it is **blocked outright**; in other words, the governance logic does not depend on whether the model is "willing to comply," but on whether external hard constraints permit it.
- Every decision is recorded to a **Merkle-tree substrate (GitTruth)** to provide an immutable audit trail.
- The article also claims that "humanitarian use restrictions" are written directly into the patent claims to impose legal/IP-level restrictions on uses involving autonomous weapons, mass surveillance, and exploitation.

## Results
- The text **does not provide standard academic experiments, benchmark datasets, or quantitative metrics**, so it is not possible to verify the magnitude of any performance improvement relative to RLHF or other safety frameworks.
- The clearest quantitative claim is that, starting from **2026-01-10**, the author has filed **99 provisional patents** covering this deterministic governance architecture.
- The article's central result-oriented claim is that, compared with probabilistic alignment, this architecture demotes the LLM from being able to "execute directly" to only being able to "propose intent," thereby establishing a stronger execution security boundary.
- Another concrete claim is that the system provides an immutable audit log based on a **Merkle tree** for tracking each governance decision.
- It also claims that by writing ethical restrictions into the patents, the technology can be legally constrained from being used for **autonomous weapons, mass surveillance, exploitation**, though the text provides no enforcement outcomes or case data.

## Link
- [https://news.ycombinator.com/item?id=47225418](https://news.ycombinator.com/item?id=47225418)
