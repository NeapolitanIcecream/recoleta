---
kind: trend
trend_doc_id: 277
granularity: day
period_start: '2026-04-10T00:00:00'
period_end: '2026-04-11T00:00:00'
topics:
- coding-agents
- repo-generation
- secure-code
- human-in-the-loop
- evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-277
tags:
- recoleta/trend
- topic/coding-agents
- topic/repo-generation
- topic/secure-code
- topic/human-in-the-loop
- topic/evaluation
language_code: en
pass_output_id: 46
pass_kind: trend_synthesis
---

# Coding-agent research is centering on explicit control surfaces

## Overview
The day’s strongest work tightens coding agents around explicit structure, bounded action, and judgment under uncertainty. Contract-Coding posts the clearest repo-level result, DeepGuard gives one of the sharper security gains, and HiL-Bench shows that asking for help is still a weak point. The through line is control that can be checked: contracts, guardrails, and evaluation that exposes missing judgment.

## Clusters

### Structured plans are carrying repo-scale coding work
Repo-scale coding papers keep writing down structure before code. Contract-Coding is the clearest result: it turns an underspecified request into a Language Contract, uses that contract to coordinate file generation, and reports strong multi-file performance on Greenfield-5. On Roguelike it reaches 47% success, above OpenHands at 30%, MetaGPT and ChatDev at 10%, and FLOW at 0%. The same paper also reports a speed gain from its Hierarchical Execution Graph, cutting Roguelike runtime from 510s to 232s. A second paper broadens the target beyond software tickets: in an Odoo ERP case study, coding agents clear easy business workflows, but scores fall once policy constraints and interdependent decisions pile up. The common thread is explicit task structure. It helps at repository scale, and it still strains when business rules must stay aligned with execution.

#### Evidence
- [Contract-Coding: Towards Repo-Level Generation via Structured Symbolic Paradigm](../Inbox/2026-04-10--contract-coding-towards-repo-level-generation-via-structured-symbolic-paradigm.md): Repo-level contract-based generation and benchmark results.
- [Can Coding Agents Be General Agents?](../Inbox/2026-04-10--can-coding-agents-be-general-agents.md): Evidence that harder business workflows break coding agents even with tool access.

### Coding-agent safety is moving into both the model and the tool loop
Safety and control show up as concrete engineering choices, not just model tuning. DeepGuard improves secure-and-correct code generation by 11.9% on average over SVEN across five code LLMs, with Qwen2.5-Coder-3B rising from 70.47% to 80.76% sec-pass@1 while keeping pass@1 close to the base model. The production paper from Zup makes the same point at the tool layer: targeted string-replacement edits beat full-file rewrites for reliability, shell access needs layered restrictions, and teams start with approval mode before giving the agent more freedom. Together these papers put the control surface in two places: inside the model for security biasing, and around the model for bounded actions and review.

#### Evidence
- [DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation](../Inbox/2026-04-10--deepguard-secure-code-generation-via-multi-layer-semantic-aggregation.md): Quantified secure code generation gains from multi-layer security signals.
- [Building an Internal Coding Agent at Zup: Lessons and Open Questions](../Inbox/2026-04-10--building-an-internal-coding-agent-at-zup-lessons-and-open-questions.md): Production design choices for safer, more reliable coding agents.

### Benchmarks are testing judgment, not just execution
Evaluation is getting stricter about what counts as competent autonomy. HiL-Bench shows that strong models still struggle to ask for clarification at the right time. On SQL tasks, pass@3 drops from 86% to 91% with full information down to 5% to 38% when the agent must decide when to call ask_human(). On SWE tasks, the drop is sharper: 64% to 88% with full information becomes 2% to 12% with selective escalation. A separate empirical study finds the same kind of gap in observability work. Across 77 repositories, humans changed logging more often than agents in 58.4% of repos, agents failed to comply with constructive logging requests 67% of the time, and humans performed 72.5% of post-generation logging repairs. Current coding agents can execute many tasks, but they still miss when to ask, when to log, and when a human will need the trail later.

#### Evidence
- [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](../Inbox/2026-04-10--hil-bench-human-in-loop-benchmark-do-agents-know-when-to-ask-for-help.md): Benchmark evidence on selective escalation and ask_human performance gaps.
- [Do AI Coding Agents Log Like Humans? An Empirical Study](../Inbox/2026-04-10--do-ai-coding-agents-log-like-humans-an-empirical-study.md): Empirical evidence that agents underserve logging and leave repair work to humans.
