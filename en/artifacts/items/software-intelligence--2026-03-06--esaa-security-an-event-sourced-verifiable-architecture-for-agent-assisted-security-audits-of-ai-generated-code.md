---
source: arxiv
url: http://arxiv.org/abs/2603.06365v1
published_at: '2026-03-06T15:15:26'
authors:
- Elzo Brito dos Santos Filho
topics:
- agentic-security-audit
- event-sourcing
- verifiable-ai-systems
- code-security
- multi-agent-governance
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# ESAA-Security: An Event-Sourced, Verifiable Architecture for Agent-Assisted Security Audits of AI-Generated Code

## Summary
This paper proposes ESAA-Security, an agent-assisted security auditing architecture for AI-generated or AI-modified code, transforming “having an LLM chat to find vulnerabilities” into a “verifiable, replayable, and traceable event-driven audit process.” Its core contribution is not the claim that it finds more vulnerabilities, but that it makes the audit process and final report auditable at the governance and evidence levels.

## Problem
- The paper addresses the following issue: AI-assisted development accelerates delivery, but even if code is functionally correct, it may still be structurally insecure in areas such as authentication, authorization, input validation, secret handling, and dependency security.
- Existing prompt-based LLM security reviews typically suffer from uneven coverage, irreproducible results, weak evidence, inconsistent severity classification, and the lack of an immutable audit trail; this makes security conclusions difficult to trust and verify.
- This matters because in agentic software engineering and long-running automated workflows, if intermediate states and conclusions are not verifiable, security audits cannot effectively support governance, remediation prioritization, or final accountability.

## Approach
- The core method is event-sourced governance: agents do not directly modify audit state, but can only output constrained, structured “intentions”; the orchestrator is responsible for validating them, writing accepted ones into an append-only event log, and then reconstructing the current audit state through deterministic projections.
- The audit is divided into 4 phases: reconnaissance, domain audit execution, risk classification, and final reporting; this is further operationalized into 26 tasks, 16 security domains, and 95 executable checks, making what is being audited explicitly encoded.
- Mechanistically, it relies on a set of fail-closed protocol invariants, such as claim-before-work, complete-after-work, lock ownership, bounded writes, and done not being silently reopened; any schema, state, or boundary violation is rejected before persistence.
- To ensure verifiability, the system treats the append-only event log as the source of truth and performs replay + hashing verification, ensuring that the final report, risk matrix, vulnerability inventory, and other outputs can all be traced back to check-level evidence.
- The output is not free-form text, but a structured evidence chain: check results → vulnerability inventory → severity classification and risk matrix → remediation guidance and executive summary → final Markdown/JSON report.

## Results
- The paper’s main results are architectural and systematic design results rather than empirical performance results; the text **does not provide** quantitative experimental metrics on real datasets, recall/accuracy/F1, or numerical improvements relative to a baseline.
- Its most concrete implementation result is the definition of **4 audit phases, 26 tasks, 16 security domains, and 95 executable checks**, covering areas such as authentication, authorization, input validation, dependencies, API security, cryptography, AI/LLM security, and DevSecOps.
- In terms of reporting artifacts, the system claims it can generate **structured check results, vulnerability inventories, CRITICAL/HIGH/MEDIUM/LOW/INFO severity classifications, risk matrices, technical remediation guidance, best-practice recommendations, a 0–100 security score, executive summaries, and a final Markdown/JSON audit report**.
- The paper proposes clear evaluation dimensions and baselines, but it remains at the validation design stage: it suggests comparison with **prompt-only review** and **checklist-only review**, evaluating explicitness of coverage, evidence structure, replayability, and report completeness, rather than simply the number of vulnerabilities.
- The authors’ strongest claim is that, compared with free-form LLM review, ESAA-Security can provide stronger **traceability, reproducibility, explicit coverage, artifact completeness, and remediation usability** in audit results; however, these claims have not yet been formally validated with case-study numbers in the excerpt provided.

## Link
- [http://arxiv.org/abs/2603.06365v1](http://arxiv.org/abs/2603.06365v1)
