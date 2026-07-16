---
kind: ideas
granularity: day
period_start: '2026-07-15T00:00:00'
period_end: '2026-07-16T00:00:00'
run_id: acf45499-b112-4bf5-b5f4-a7aeb417f6c1
status: succeeded
topics:
- agent evaluation
- coding agents
- software security
- agent governance
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/coding-agents
- topic/software-security
- topic/agent-governance
language_code: en
pass_output_id: 329
pass_kind: trend_ideas
upstream_pass_output_id: 328
upstream_pass_kind: trend_synthesis
---

# Agent release checks tied to interaction history and executable evidence

## Summary
Agent evaluations should preserve the interaction conditions that alter behavior, while security and pull-request workflows should bind consequential actions to inspectable evidence and narrow authorization. The most useful near-term changes are release tests for tool adaptation, evidence-gated security findings, and lightweight authorization receipts designed around the single-maintainer workflows seen in current coding-agent use.

## Release tests for tool failover within persistent agent sessions
Agent-platform teams operating redundant APIs should add silent backend shifts to release testing and run them across every supported harness. AgentCompass shows that changing the harness can move the same model’s SWE-bench-Pro score by several points and can expose different trajectory failures. The set-shifting benchmark shows a separate operational risk: after reliability changes during a persistent session, agents can remain locked into an obsolete tool routine even when an equivalent working tool is available. A release report should therefore include a model-by-harness matrix with post-shift tool shares, task completion, repeated calls, and recovery latency—not only aggregate task success. The cheapest check is to replay a small set of production-like sessions, silently fail the preferred backend halfway through, and compare recovery with a fresh-session control; this determines whether session history or the backend failure itself causes the loss.

### Sources
- [AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities](../Inbox/2026-07-15--agentcompass-a-unified-evaluation-infrastructure-for-agent-capabilities.md): On SWE-bench-Pro, Claude-Opus-4.8 scored 66.21 with Mini-SWE-agent and 73.87 with OpenHands; trajectory analysis also identified harness-visible failure patterns such as repeated calls and empty outputs.
- [Set-shifting Behavioral Test for Harnessed Agents](../Inbox/2026-07-15--set-shifting-behavioral-test-for-harnessed-agents.md): Across hidden reliability shifts, agents settled into recurring tool routines; reported cumulative set-shifting accuracy ranged from 0.02 to 0.33 for mimo-v2.5 and 0.17 to 0.82 for deepseek-v4-pro.

## Evidence-gated repository security findings with selective sandbox escalation
Application-security teams should prevent an automated repository finding from blocking a merge until its claimed mechanism is supported by a code path, configuration, registry record, or sandbox trace. DREA improves vulnerability detection through hypothesis-directed repository exploration, yet 26–55% of true positives across evaluated systems had flawed rationales. ProfMalPlus supplies a practical escalation pattern: begin with static behavior graphs and source-preserving slices, then request registry or sandbox evidence only when the judgment remains unresolved. Applied to pull-request scanning, the detector would emit a provisional hypothesis, gather the cheapest evidence that could refute it, and attach the resulting slice or trace to the review. Test this first by relabeling a sample of current true-positive alerts for mechanism correctness and measuring how many merge-blocking findings would lose support after expert review.

### Sources
- [DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection](../Inbox/2026-07-15--drea-decoupled-reasoning-and-exploration-agents-for-repository-level-vulnerability-detection.md): DREA raised pair-level correctness from 19% to 42% for DeepSeek-V3.2 and offloaded over 93% of tokens, but 26–55% of true positives across systems were supported by flawed rationales.
- [ProfMalPlus: Agent-Coordinated Detection of Malicious NPM Packages via Static-Dynamic Analysis Synergy](../Inbox/2026-07-15--profmalplus-agent-coordinated-detection-of-malicious-npm-packages-via-static-dynamic-analysis-synergy.md): ProfMalPlus routes unresolved judgments to registry enrichment or sandboxed execution and reports 98.1% F1, with 88.9% line-level localization F1.

## Action-specific authorization receipts for coding-agent pull requests
Git hosting providers should test narrow, action-specific authorization inside the dominant one-person coding-agent workflow rather than begin with organization-wide autonomous permissions. In the observed GitHub sample, 88.7% of agentic pull-request workflows involved one human, and the median repository produced only one or two agentic pull requests in three months. EBAE provides a concrete execution rule for this setting: the agent may propose an action, but a protected executor releases it only when a one-use certificate, policy, freshness state, and exact intent agree within the same epoch. A GitHub App could turn a maintainer’s approval into a short-lived receipt limited to one repository, branch, commit range, and operation such as opening a pull request or rerunning CI. Because EBAE has no quantitative evaluation, the first useful test is operational: compare approval time, rejected stale actions, and maintainer overrides against the existing GitHub App permission flow on low-volume repositories.

### Sources
- [Early Adoption of Agentic Coding Tools by GitHub Projects](../Inbox/2026-07-15--early-adoption-of-agentic-coding-tools-by-github-projects.md): Across 2,361 repositories, the median project produced one to two agentic pull requests in three months; one-person workflows accounted for 88.7% of observed cases.
- [EBAE: A protocol for bounding the real-world authority of autonomous agents](../Inbox/2026-07-15--ebae-a-protocol-for-bounding-the-real-world-authority-of-autonomous-agents.md): EBAE separates proposal from protected execution and requires action-specific, one-use authorization plus aligned policy, freshness, and anti-rollback state; the supplied evidence reports no quantitative evaluation.
