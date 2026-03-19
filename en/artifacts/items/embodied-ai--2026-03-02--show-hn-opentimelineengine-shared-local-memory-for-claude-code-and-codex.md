---
source: hn
url: https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine
published_at: '2026-03-02T22:59:15'
authors:
- joeljoseph_
topics:
- agent-memory
- local-first
- ai-coding-agent
- dual-agent-architecture
- policy-enforcement
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: OpenTimelineEngine – Shared local memory for Claude Code and codex

## Summary
Open Timeline Engine is a local-first shared memory and behavioral constraint platform for AI agents, aimed at ensuring executors such as Claude/Codex/Cursor no longer have to start from zero every time. It emphasizes auditable memory, policy enforcement, a dual-AI architecture, and passive learning based on real workflows, but it is currently still an experimental project.

## Problem
- It addresses the **session amnesia** problem of AI coding agents: users have to repeatedly restate coding conventions, architectural context, and past corrections, leading to low efficiency and repeated mistakes.
- It addresses the risk of a single-model agent both **deciding and executing**: once the plan goes wrong, is prompt-injected, or ignores constraints, there is no independent check-and-balance or safety gating.
- It addresses the need among teams/individuals for **local control, audit trails, and stylistic consistency** in AI usage, which is especially important for developers working long-term on the same codebase.

## Approach
- It builds a **local-first timeline memory engine**: passively collecting the user's real workflow from multiple sources such as CLI, Git, editors, and browsers, forming a searchable decision timeline rather than just chat logs.
- It uses a **dual-AI architecture**: the executor AI does the work, while the advisor AI reads the timeline on the API side and provides constraints/rewrites/arbitration; both share memory, but the advisor cannot write events, reducing the risk of self-contamination.
- It implements progressive autonomy through a **takeover mechanism**: each round computes a 4-factor confidence score (goal clarity 40%, evidence strength 25%, outcome stability 20%, classification certainty 15%), then decides whether to continue execution, enter deliberation, or request a human.
- It replaces pure prompting with **architecture-level safety policies**: ABAC, default blocking for sensitive levels, `check_context` before edits, protected directory lockdown, instruction text stripping, preventing the advisor from writing events, audit logs, and versioned schemas.
- It mines historical behavior into **patterns and a personality fingerprint**: claiming to continuously update a 25-dimensional behavioral fingerprint, 6 major categories, and 12 situational labels from the timeline, and to feed success/failure back into subsequent retrieval and recommendations.

## Results
- The text **does not provide quantitative experimental results on standard academic benchmarks**, nor does it provide comparative metrics on public datasets, ablation studies, or statistically significant results.
- The most specific system-level numbers given by the project include: a **25-dimensional** behavioral fingerprint covering **6 categories** of behavioral dimensions; **12 categories** of situational classification; a retrieval budget of **≤120ms per round** and **≤60ms per backend**; a session takeover timeout of about **120 minutes**; and instruction expiration times of **30–120 seconds**.
- In the memory/retrieval flow, it states that pgvector is preferred, with fallback to Qdrant when the quality score is **<0.42** or the hit count is **<2**; if `context_quality_score ≥ 0.72`, it skips expensive retrieval and uses cached context.
- The goal discovery and working-set refresh rules provide specific thresholds: continue when the goal selection score is **>0.45**; refresh the working set on the first round, when the goal changes, or **every 6 rounds**; re-trigger goal discovery after **more than 2 failures**; stop if low relevance persists for **3 consecutive cycles**.
- The project cites external research claiming that “Stanford research shows a **85%** personality-cloning accuracy from a 2-hour interview,” using this to justify its direction of passive behavioral cloning, but **this is not an experimental result of the project itself**.
- Its strongest core claim is that, compared with a typical memory layer, the system can provide **shared local memory, behavioral style learning, dual-AI executor/advisor separation, auditable safety gating, and consistent cross-executor constraints** to improve the continuity and controllability of long-running AI coding agents.

## Link
- [https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine](https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine)
