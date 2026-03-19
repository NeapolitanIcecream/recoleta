---
source: arxiv
url: http://arxiv.org/abs/2603.06365v1
published_at: '2026-03-06T15:15:26'
authors:
- Elzo Brito dos Santos Filho
topics:
- security-audit
- event-sourcing
- llm-agents
- ai-generated-code
- verifiable-systems
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# ESAA-Security: An Event-Sourced, Verifiable Architecture for Agent-Assisted Security Audits of AI-Generated Code

## Summary
ESAA-Security proposes an event-sourced architecture for security auditing of AI-generated/modified code, transforming LLM-based review from a "free-form conversational review" into a "verifiable audit pipeline." Its core value is not in claiming to find more vulnerabilities, but in making the audit scope, evidence chain, state changes, and final report all traceable, replayable, and auditable.

## Problem
- Problem addressed: AI-assisted programming has increased development speed, but even when code is functionally correct, it may still contain structural security flaws in areas such as authentication, authorization, input validation, key management, and dependency security.
- Why it matters: Existing prompt-based LLM security review commonly suffers from unstable coverage, hard-to-reproduce conclusions, weak evidence, inconsistent severity classification, and the lack of an immutable audit trail, making it difficult to use for governance and accountability.
- In agentic software engineering, long-horizon, multi-step, stateful execution amplifies the risks of context omission and unverifiable intermediate steps, so simply improving prompts is not enough.

## Approach
- Core mechanism: Security auditing is modeled as an **event-driven, governed process**, rather than having an LLM directly "read a repository and then write an audit opinion." Agents output only structured intentions, while actual state changes are validated by a deterministic orchestrator before being written to an append-only event log.
- The architecture adopts event sourcing and CQRS ideas: the **event log is the single source of truth**, the current audit state is obtained through event projections, and consistency is verified through replay and hash checks, thereby ensuring traceability and reproducibility.
- The audit workflow is divided into 4 phases: reconnaissance, domain audit execution, risk classification, and final reporting; it is further refined into 26 tasks, 16 security domains, and 95 executable checks, explicitly constraining coverage.
- Agent behavior is controlled through strict protocols and invariants, such as claim-before-work, complete-after-work, lock ownership, boundary writes, and done cannot be silently reopened; any schema error, illegal state transition, or out-of-bounds write is rejected before persistence.
- The output is not an arbitrarily generated text report, but a process that starts from check-level evidence objects and progressively aggregates them into a vulnerability inventory, severity classification, risk matrix, remediation guidance, executive summary, and final Markdown/JSON report.

## Results
- The paper's main contribution is its **architecture and methodology**, not a completed large-scale quantitative experiment; the text **does not provide specific benchmark data, accuracy/recall, or numerical comparison results with baselines**.
- The explicitly claimed structured outputs include: **4 audit phases, 26 tasks, 16 security domains, and 95 executable checks**, and it generates vulnerability inventories, risk matrices, remediation guidance, executive summaries, and final reports.
- The executive summary defines a **0–100 security score** output, but the excerpt does not report any real-case scores or statistical results.
- The paper proposes evaluation dimensions and a case study protocol: comparing ESAA-Security with prompt-only review and checklist-only review, focusing on replayability, traceability, explicit coverage, artifact completeness, and remediation usefulness, rather than only comparing the number of vulnerabilities.
- The strongest concrete claim is that the system can shift the "unit of trust" in AI-assisted security auditing from free-text opinions to an audit process and report that are **protocol-valid, event-traceable, and state-replay-verifiable**.

## Link
- [http://arxiv.org/abs/2603.06365v1](http://arxiv.org/abs/2603.06365v1)
