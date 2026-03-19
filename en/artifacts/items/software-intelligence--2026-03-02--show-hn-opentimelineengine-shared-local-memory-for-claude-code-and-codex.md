---
source: hn
url: https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine
published_at: '2026-03-02T22:59:15'
authors:
- joeljoseph_
topics:
- ai-memory
- code-agents
- local-first
- behavioral-cloning
- policy-enforcement
- multi-agent
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Show HN: OpenTimelineEngine – Shared local memory for Claude Code and codex

## Summary
Open Timeline Engine is a local-first shared memory and control platform for AI coding agents, aiming to let agents like Claude/Codex/Cursor remember real working practices across sessions instead of starting from zero each time. It extends "memory retrieval" into "timeline-based behavior cloning, policy constraints, audit trails, and dual-AI collaborative execution."

## Problem
- Existing AI coding agents usually **cold-start every session**, repeatedly forgetting codebase conventions, prior corrections, and user preferences, causing the same mistakes to recur.
- Chat memory or prompts alone are insufficient to support **reliable autonomous execution**: when the same model both decides and executes, hallucinated plans can be acted on directly, and prompt injection can more easily bypass safeguards.
- For day-to-day software development, users also need **local data control, auditability, cross-agent shared context, and safety constraints**, not just "the ability to recall some preferences."

## Approach
- Use a **local-first timeline engine** to continuously capture signals from real workflows: CLI, Git, VSCode, browsers, MCP sessions, etc., turning "what happened, why it was decided that way, and what the outcome was" into searchable memory.
- Adopt a **dual-AI architecture**: the executor agent does the work; the API-side advisor agent reads the timeline, provides suggestions/rewrites/safety gating, and does not directly write events, architecturally separating "action" from "supervision."
- Provide **shared or isolated workspace memory**, allowing multiple executors such as Claude, Codex, and Cursor to share the same workspace memory or remain isolated by executor; retrieval defaults to user-only, with cross-user/cross-executor expansion only on explicit request.
- Introduce a **progressive autonomy mechanism**: each round is scored on four dimensions—goal clarity, evidence strength, outcome stability, and classifier certainty—to decide whether to continue quickly, perform cautious retrieval/deeper deliberation, or pause for human confirmation.
- Constrain execution through **policy and firewall-style safety controls**: ABAC, default blocking for sensitive levels, `check_context` before edits, protected-directory blocking, instruction text stripping, audit logs, and redaction before embedding and before response, avoiding reliance on prompt-only security.

## Results
- The text **does not provide standard academic benchmarks or independent experimental evaluation results**, so there are no verifiable SOTA numbers; the current public version is **v0.3.0**, and the project is explicitly labeled **experimental and not production-ready**.
- The paper/project claims it can build a **25-dimensional behavioral fingerprint** covering **6 categories** (such as decision-making style, communication, prioritization, context switching, learning style, and emotional patterns), and classify situations into **12 behavioral categories**.
- Autonomous decision confidence is weighted by **4 factors**: goal clarity **40%**, evidence strength **25%**, outcome stability **20%**, and classifier certainty **15%**; these determine whether to proceed, deliberate, or request human input.
- Retrieval budgets are tightly constrained to **≤120ms total per round** and **≤60ms per backend/source**; when the pgvector quality score is **<0.42** or hit count is **<2**, it can fall back to Qdrant; an example working-set quality threshold is **context_quality_score ≥ 0.72**.
- Session takeover state is persisted by `session_id` with a **120-minute** timeout; execution instructions can be set to expire in **30–120 seconds**; the working set is typically refreshed **every 6 rounds**, and goal discovery is also retriggered **every 6th round** or **after more than 2 failures**.
- The project cites an external comparative claim: Stanford research reportedly found that "a 2-hour interview can reach **85%** personality-clone accuracy"; the author claims this system can **passively** approach that goal from real working behavior, but the text **does not provide its own experimental accuracy, baseline comparisons, or reproducibility data**.

## Link
- [https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine](https://github.com/JOELJOSEPHCHALAKUDY/open-timeline-engine)
