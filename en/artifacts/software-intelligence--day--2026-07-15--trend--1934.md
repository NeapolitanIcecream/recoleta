---
kind: trend
trend_doc_id: 1934
granularity: day
period_start: '2026-07-15T00:00:00'
period_end: '2026-07-16T00:00:00'
topics:
- agent evaluation
- coding agents
- software security
- agent governance
run_id: materialize-outputs
aliases:
- recoleta-trend-1934
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/coding-agents
- topic/software-security
- topic/agent-governance
language_code: en
pass_output_id: 328
pass_kind: trend_synthesis
---

# Harness choices alter agent scores, tool habits, and security outcomes

## Overview
Recent evidence on engineered context and executable checks is becoming more specific at the harness level. Today’s studies show that interaction protocols can change benchmark scores, persistent sessions can lock agents into stale tool routines, and targeted exploration can improve security analysis. Deployment remains immature: observed coding-agent use was sparse and usually supervised by one person.

## Findings

### Harness-dependent evaluation
AgentCompass separates benchmarks, harnesses, and execution environments, then shows that the same model’s result can vary with the harness. On SWE-bench-Pro, Claude-Opus-4.8 scored 66.21 with Mini-SWE-agent and 73.87 with OpenHands. A separate set-shifting benchmark finds that agents quickly settle into recurring tool routines and may keep using an unreliable group after a silent backend change. Together, the studies make interaction history and harness configuration part of the measured capability, rather than incidental test plumbing.

#### Sources
- [AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities](../Inbox/2026-07-15--agentcompass-a-unified-evaluation-infrastructure-for-agent-capabilities.md): Reports harness-dependent SWE-bench-Pro scores and trajectory-level failure analysis across seven models.
- [Set-shifting Behavioral Test for Harnessed Agents](../Inbox/2026-07-15--set-shifting-behavioral-test-for-harnessed-agents.md): Measures adaptation after hidden tool-reliability changes and finds recurring, sometimes stale routing routines.

### Targeted evidence for software security
Security agents benefit when exploration is driven by a concrete hypothesis. DREA’s planner requests repository evidence from a lightweight explorer; pair-level correctness rose from 19% to 42% for DeepSeek-V3.2 while more than 93% of tokens were handled locally. ProfMalPlus similarly routes uncertain package judgments toward static, registry, or sandbox evidence, reporting 98.1% F1 and 597 newly identified malicious NPM packages. VisualRepair applies the same selective-attention principle to screenshots, resolving 196 SWE-bench Multimodal test issues—10 more than its best baseline. The shared result is conditional: narrower evidence gathering helps, but DREA still found flawed rationales behind 26–55% of true positives.

#### Sources
- [DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection](../Inbox/2026-07-15--drea-decoupled-reasoning-and-exploration-agents-for-repository-level-vulnerability-detection.md): Reports repository-guided exploration gains, local-token offloading, and the rate of correct labels supported by flawed rationales.
- [ProfMalPlus: Agent-Coordinated Detection of Malicious NPM Packages via Static-Dynamic Analysis Synergy](../Inbox/2026-07-15--profmalplus-agent-coordinated-detection-of-malicious-npm-packages-via-static-dynamic-analysis-synergy.md): Combines static, dynamic, and registry evidence and reports 98.1% F1 plus 597 confirmed malicious packages.
- [VisualRepair: Dynamic Tool Calling and Region Focusing for Visual Software Issue Repair](../Inbox/2026-07-15--visualrepair-dynamic-tool-calling-and-region-focusing-for-visual-software-issue-repair.md): Uses type-specific visual tools and dynamic region focusing, resolving 196 test issues on SWE-bench Multimodal.

### Early operational governance
Real-world adoption still centers human oversight. Across 2,361 GitHub repositories, the median project produced only one or two agentic pull requests in three months; one-person workflows accounted for 88.7% of observed cases. Governance proposals are appearing alongside this limited deployment base. EBAE separates an agent’s proposal from protected execution through action-specific, epoch-bound authorization, while DNSid links agent identity to internet domains and cryptographic registration records. Both mechanisms remain lightly validated: EBAE provides no quantitative evaluation, and DNSid reports unnamed trials without results.

#### Sources
- [Early Adoption of Agentic Coding Tools by GitHub Projects](../Inbox/2026-07-15--early-adoption-of-agentic-coding-tools-by-github-projects.md): Measures sparse project-level adoption and predominantly single-human oversight across 25,264 agentic pull requests.
- [EBAE: A protocol for bounding the real-world authority of autonomous agents](../Inbox/2026-07-15--ebae-a-protocol-for-bounding-the-real-world-authority-of-autonomous-agents.md): Specifies epoch-bound, action-specific authorization but reports no quantitative evaluation.
- [Vint Cerf is working on a plan to unleash AI agents on the open internet](../Inbox/2026-07-15--vint-cerf-is-working-on-a-plan-to-unleash-ai-agents-on-the-open-internet.md): Describes domain-linked agent identity and cryptographic registration history, with trials but no published outcomes.
