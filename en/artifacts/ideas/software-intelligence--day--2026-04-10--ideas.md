---
kind: ideas
granularity: day
period_start: '2026-04-10T00:00:00'
period_end: '2026-04-11T00:00:00'
run_id: ead7a913-d224-4dbe-aa9c-41958ae9d654
status: succeeded
topics:
- coding-agents
- repo-generation
- secure-code
- human-in-the-loop
- evaluation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repo-generation
- topic/secure-code
- topic/human-in-the-loop
- topic/evaluation
language_code: en
pass_output_id: 47
pass_kind: trend_ideas
upstream_pass_output_id: 46
upstream_pass_kind: trend_synthesis
---

# Coding agent control gates

## Summary
The clearest near-term changes are more explicit control points around coding agents: a contract artifact before repo generation, a security scoring layer paired with bounded edit tools, and a required clarification step for ambiguous work. The evidence supports concrete builds and workflow changes more than broad autonomy claims.

## Contract-first repository generation for multi-file greenfield work
Build a contract-first repo generator for greenfield internal tools and small product modules. The useful change is to make the agent write a machine-checkable spec before it writes files: required modules, file mapping, APIs, type signatures, and state definitions. Contract-Coding gives a concrete reason to do this. On Greenfield-5 it reports 100% success on Gomoku and Plane Battle, 87% on City Sim, 80% on Snake++, and 47% on Roguelike, with a clear edge over OpenHands, MetaGPT, ChatDev, and FLOW on the hardest task in the set. The speed result also matters for product teams that want shorter iteration loops: the Hierarchical Execution Graph kept Roguelike success at 47% while cutting runtime from 510s to 232s.

The first users are teams generating new multi-file services, admin tools, game prototypes, or migration scaffolds where cross-file consistency breaks more often than local syntax. A cheap test is simple: take ten greenfield tasks that currently require several rounds of agent repair, add a contract artifact that must be approved or auto-checked before code generation, and measure file-level consistency, rerun count, and elapsed time to a passing repo. The weak point is visible in the same evidence: this helps most when the job can be reduced to explicit interfaces and module boundaries. Tasks with dense policy logic or business-rule conflicts still need another control layer above the contract.

### Evidence
- [Contract-Coding: Towards Repo-Level Generation via Structured Symbolic Paradigm](../Inbox/2026-04-10--contract-coding-towards-repo-level-generation-via-structured-symbolic-paradigm.md): Repo-level results, benchmark comparisons, and runtime gains support a contract-first build for multi-file generation.
- [Can Coding Agents Be General Agents?](../Inbox/2026-04-10--can-coding-agents-be-general-agents.md): The Odoo case shows where explicit structure still struggles once policy constraints and interdependent business decisions accumulate.

## Security-biased code generation with patch-based edits and approval gates
Add a security scoring layer to code generation and pair it with bounded editing tools. DeepGuard shows a concrete model-side path: aggregate security signals from multiple transformer layers, then apply a cheap inference-time bias so the model prefers secure tokens without giving up much functional correctness. Across five code LLMs it improves secure-and-correct generation by 11.9% on average over SVEN, and on Qwen2.5-Coder-3B it lifts sec-pass@1 from 70.47% to 80.76% while keeping pass@1 near the base model.

That is enough to justify a narrow product build for teams shipping internal coding agents into codebases with routine security exposure: web handlers, auth flows, file operations, database access, and dependency glue. Zup's deployment paper gives the tool-side complement. Their internal agent relied on targeted string-replacement edits, layered shell restrictions, audit logging, and approval mode before broader autonomy. A practical rollout is to route high-risk files through a security-hardened model path, keep edits patch-based, and require approval for shell and write actions in the early phase. The cheap check is to replay a few hundred accepted agent tasks with security review labels and compare vulnerability findings, pass rate, and manual rework before expanding access.

### Evidence
- [DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation](../Inbox/2026-04-10--deepguard-secure-code-generation-via-multi-layer-semantic-aggregation.md): Provides the concrete secure-code gain and the mechanism that preserves correctness while improving security.
- [Building an Internal Coding Agent at Zup: Lessons and Open Questions](../Inbox/2026-04-10--building-an-internal-coding-agent-at-zup-lessons-and-open-questions.md): Shows the surrounding tool controls that make a security-hardened coding agent usable in production.

## Clarification-first ticket triage for coding agents
Put an explicit clarification gate in front of ambiguous coding tasks and score it as a product feature. HiL-Bench shows the gap is large enough to warrant its own workflow. On SQL tasks, models that score 86% to 91% pass@3 with full information fall to 5% to 38% when they must decide when to call `ask_human()`. On SWE tasks, models that reach 64% to 88% with full information drop to 2% to 12% with selective escalation. No model clears 50% blocker recall on SWE. The issue is not rare edge cases. The benchmark contains 1,131 human-validated blockers, averaging 3.8 per task, across missing information, ambiguous requests, and contradictory information.

The build here is straightforward: add a required blocker check before execution on tickets that touch unclear requirements, hidden policy choices, or incomplete repo context. The agent should surface candidate blockers, ask targeted questions, and pause when those questions remain unanswered. This also needs evaluation beyond pass/fail. Ask-F1, blocker recall, and question precision should sit next to task completion in internal scorecards. The nearby logging study points to the same operational problem from another angle. Agents miss non-functional expectations and humans do the cleanup later: in 58.4% of repositories, humans changed logging more often than agents, agents failed to comply with constructive logging requests 67% of the time, and humans handled 72.5% of post-generation logging repairs. Teams deploying agents into issue-to-PR workflows need a formal clarification step before coding, not only a chat box that the model rarely uses well.

### Evidence
- [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](../Inbox/2026-04-10--hil-bench-human-in-loop-benchmark-do-agents-know-when-to-ask-for-help.md): Quantifies how badly agents perform when they must decide when to ask for clarification.
- [Do AI Coding Agents Log Like Humans? An Empirical Study](../Inbox/2026-04-10--do-ai-coding-agents-log-like-humans-an-empirical-study.md): Shows a related failure in observability requirements where humans repair what agents omit or mis-handle.
