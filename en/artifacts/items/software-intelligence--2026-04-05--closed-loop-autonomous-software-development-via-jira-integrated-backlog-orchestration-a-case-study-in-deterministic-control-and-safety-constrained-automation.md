---
source: arxiv
url: http://arxiv.org/abs/2604.05000v1
published_at: '2026-04-05T21:54:03'
authors:
- Elias Calboreanu
topics:
- autonomous-software-development
- jira-orchestration
- bounded-autonomy
- software-lifecycle-automation
- safety-controls
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation

## Summary
This paper describes a production case study of autonomous software lifecycle management built around a deterministic Jira-backed control loop, not an open-ended code generator. The main claim is that bounded AI actions, explicit state transitions, and recovery rules can automate backlog and ticket work with high observed reliability.

## Problem
- Software teams spread requirements, tickets, compliance items, and scan results across many places, which makes backlog maintenance slow, inconsistent, and hard to audit.
- The paper reports a fragmented baseline with 820 Jira items in To Do, 223 In Progress, and 689 Done, plus 13 structured source documents and compliance-related ticket families.
- The missing piece was a closed loop that could ingest inputs, deduplicate and prioritize work, execute fixes, verify them, and publish results back to Jira without losing traceability or letting concurrent agents collide.

## Approach
- The system uses a deterministic seven-stage pipeline implemented as 7 scheduled automation lanes: intake, codebase audit, backlog grooming, AI code fixing, ops monitoring, quality gate, and spec-completeness audit.
- It keeps two synchronized views of work: a local canonical backlog as the authority of record and Jira as the shared status surface. A Jira Status Contract with states To Do, In Progress, On Hold, and Done acts as the ticket lock and re-entry policy.
- AI is restricted to a supervisory role inside fixed rails: structured context packages, confidence thresholds, time budgets, diff-size review rules, output re-validation, and human review gates. Items with confidence score `s >= 0.83` may run autonomously, `0.50 <= s < 0.83` go to human review, and lower scores are re-ingested.
- Matching and ticket mapping use a four-step canonicalization process with exact tags, key matching, weighted summary similarity, and fuzzy text matching. Execution happens in isolated worktrees, then product and security verifiers check the result before Jira is updated.
- Safety controls include 19 FMEA failure modes, 12 centralized lock mechanisms, degraded-mode operation during Jira outages, checkpoint-based timeouts, and a recovery cascade with retries, replay logs, backoff, circuit breaking, and stalled-state handling.

## Results
- In the initial evaluation window, the system completed 152 runs with **100% terminal-state success**, with a **95% Clopper-Pearson interval of [97.6%, 100%]**.
- The deployment later accumulated **more than 795 run artifacts** in continuous operation.
- Three rounds of adversarial code review produced **51 findings**; **48 were fully remediated**, **3 were closed with deferred hardening**, and the paper reports **zero false negatives within the injected set**.
- In the autonomous security ticket family of **10 items**, **6 were completed autonomously** through dispatch and verification, **2 required manual remediation**, and **2 were closed by policy decision**.
- The architecture was consolidated from **11 lanes to 7**, cutting script count by **55% (51 to 23)** and automation code by **45% (22,946 to 12,661 LOC)** while keeping the safety controls.
- The paper also reports **zero duplicate Jira posts** during the evaluation period. Lane 7 for specification-completeness checking is implemented, but the excerpt says its empirical validation is still future work.

## Link
- [http://arxiv.org/abs/2604.05000v1](http://arxiv.org/abs/2604.05000v1)
