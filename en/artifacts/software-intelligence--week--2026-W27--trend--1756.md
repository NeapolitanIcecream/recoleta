---
kind: trend
trend_doc_id: 1756
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
topics:
- coding agents
- agent evaluation
- software engineering agents
- LLM operations
- agent security
- identity and access control
- cost control
run_id: materialize-outputs
aliases:
- recoleta-trend-1756
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering-agents
- topic/llm-operations
- topic/agent-security
- topic/identity-and-access-control
- topic/cost-control
language_code: en
pass_output_id: 306
pass_kind: trend_synthesis
---

# Coding agents are being judged by review load, run cost, and containment

## Overview
This week’s evidence treats coding agents as production systems. The strongest work measured review burden, token spend, and privilege control after agents leave single-task demos. SWE-INTERACT cut top-model resolve rates to about half of single-turn results, TraceLab showed long-context reads dominate serving cost, and Securing Agentic Identity kept reusable OAuth tokens out of agent runtimes.

## Clusters

### Interactive coding-agent evaluation
Benchmarks are putting the user back into the loop. SWE-Together reconstructed 109 repository-level tasks from 11,260 recorded sessions and scored both final correctness and User Correction, a measure of how much explicit or soft feedback the agent needed. Claude Opus 4.8 led the reported agents at 63% pass@1, while the reference patch baseline stayed around 78%.

SWE-INTERACT made the cost of interaction more visible. On the same underlying tasks, Opus 4.8 dropped from 50.7% single-turn resolve rate to 26.7% in the multi-turn setting. GPT 5.5 dropped from 48.0% to 24.7%, while its per-trial cost rose from $2.78 to $9.84. The failures were not only missed goals; forgotten requirements and implementation bugs remained common after long exchanges.

#### Evidence
- [SWE-Together: Evaluating Coding Agents in Interactive User Sessions](../Inbox/2026-06-29--swe-together-evaluating-coding-agents-in-interactive-user-sessions.md): SWE-Together benchmark design, task count, User Correction metric, and reported pass rates.
- [SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions](../Inbox/2026-06-29--swe-interact-reimagining-swe-benchmarks-as-user-driven-long-horizon-coding-sessions.md): SWE-INTERACT multi-turn setup, resolve-rate drops, cost increase, and failure labels.

### Runtime evidence for code changes
The strongest repair work tied model output to executable artifacts. SWE-Doctor generated multi-faceted bug reproduction tests, ran them under a debugger, and fed runtime diagnosis records into patch generation. It reported 75.7% average resolution on SWE-bench Verified and 59.4% on SWE-bench Pro, with an 8.0 to 8.9 percentage-point gain over baseline agents on SWE-bench Pro.

Other work in the week used feature maps, profiling traces, compiler errors, benchmarks, and approval records as control points for repository-level edits, memory optimization, and C-to-Rust migration. The common pattern is concrete evidence before final code submission: tests, traces, diagnostics, and explicit approval artifacts become part of the agent’s work product.

#### Evidence
- [SWE-Doctor: Guiding Software Engineering Agents with Runtime Diagnosis from Multi-Faceted Bug Reproduction Tests](../Inbox/2026-07-01--swe-doctor-guiding-software-engineering-agents-with-runtime-diagnosis-from-multi-faceted-bug-reproduction-tests.md): SWE-Doctor approach and reported SWE-bench Verified and Pro results.

### Agent cost and repository quality
Cost evidence became more concrete. TraceLab analyzed 4,265 real coding-agent sessions, 357,161 LLM steps, and 432,510 tool calls from Claude Code and Codex. Prefix tokens accounted for 52.56B of 54.90B input tokens and 59.5% of estimated API cost. Even with a 95.7% global prefix-cache hit rate, misses caused 3.8 times more prefilling than truly new input.

Repository quality also showed up as an operating cost. A controlled minimal-pair study across 660 Claude Code trials found no pass-rate change from cleaner code, but cleaner repositories used 7% to 8% fewer tokens and reduced file revisits by 34%. A separate budget RFC proposed run-scoped atomic spend reservations before provider calls, with machine-readable budget state so agents can downshift model choice, shorten context, or stop cleanly.

#### Evidence
- [TraceLab: Characterizing Coding Agent Workloads for LLM Serving](../Inbox/2026-06-29--tracelab-characterizing-coding-agent-workloads-for-llm-serving.md): TraceLab dataset scale, token distribution, prefix-cache behavior, and cost attribution.
- [Does Code Cleanliness Affect Coding Agents?](../Inbox/2026-07-05--does-code-cleanliness-affect-coding-agents.md): Controlled study showing cleaner code reduced token use and file revisits without changing pass rate.
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): Run-scoped budget authority proposal and cost-control mechanism.

### Containment, identity, and action boundaries
Safety work focused on what the agent is allowed to touch. UnderSpecBench tested 2,208 DevOps prompt variants and found that acted runs violated action boundaries 55.8% to 67.8% of the time across evaluated configurations. Wrong-target and overscope outcomes matter because a plausible cleanup, rollback, or access-change command can hit the wrong branch, namespace, database, or service.

Identity and execution designs treated the model runtime as a place to minimize trust. Securing Agentic Identity proposed a broker, proxy, and mutual TLS pattern so real OAuth tokens never enter the agent environment. Fly.io’s Sprite pattern kept the long-lived agent loop separate from disposable command sandboxes, with single-command token injection and checkpoint rollback. The Claude Desktop red-team report showed why that separation matters: synced preferences plus command-capable connectors can turn an account compromise into workstation code execution.

#### Evidence
- [Coding Agents Are Guessing: Measuring Action-Boundary Violations in Underspecified DevOps Instructions](../Inbox/2026-07-02--coding-agents-are-guessing-measuring-action-boundary-violations-in-underspecified-devops-instructions.md): UnderSpecBench design and reported boundary-violation rates.
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Token-broker, proxy, and mTLS design for keeping OAuth tokens out of agent runtimes.
- [Building Agents That Don't Break Themselves](../Inbox/2026-07-05--building-agents-that-don-t-break-themselves.md): Fly.io Sprite isolation pattern, single-command token injection, and rollback example.
- [Red teamers turned Claude Desktop into a double agent to do their evil bidding](../Inbox/2026-07-01--red-teamers-turned-claude-desktop-into-a-double-agent-to-do-their-evil-bidding.md): Claude Desktop red-team path from account compromise to workstation command execution.
- [Show HN: A Firewall for AI agents with auditing](../Inbox/2026-06-29--show-hn-a-firewall-for-ai-agents-with-auditing.md): MCP gateway using sealed commitments and data-flow checks for multi-step tool safety.
