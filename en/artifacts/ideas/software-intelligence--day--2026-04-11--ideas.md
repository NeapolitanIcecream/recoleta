---
kind: ideas
granularity: day
period_start: '2026-04-11T00:00:00'
period_end: '2026-04-12T00:00:00'
run_id: ead7a913-d224-4dbe-aa9c-41958ae9d654
status: succeeded
topics:
- coding-agents
- verification
- agent-memory
- benchmarks
- systems-optimization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/verification
- topic/agent-memory
- topic/benchmarks
- topic/systems-optimization
language_code: en
pass_output_id: 49
pass_kind: trend_ideas
upstream_pass_output_id: 48
upstream_pass_kind: trend_synthesis
---

# Agent Runtime Infrastructure

## Summary
The clearest applied changes in this evidence are structural files for code navigation, memory control in the agent harness, and execution-validated plan rewrites in Apache DataFusion. Each one gives a specific build or workflow change with measured effects, while the broader pair-programming and benchmark papers are more useful as supporting context than as immediate product directions.

## Versioned architecture descriptor files for agent code navigation
Repository maintainers can add an architecture descriptor as a first-class file for coding agents, then measure whether it cuts navigation before they ask for more autonomous edits. The evidence here is more about wasted search than raw coding quality. In the controlled study, architecture context cut average navigation steps on a 22K-line Rust project from 5.2 to 3.4 with S-expressions or JSON, and to 2.9 with Markdown. In a second study on a 43K-line Rust project, an auto-generated 170-line descriptor reached 100% accuracy on 15 tasks, against 80% for blind search. That is enough to justify a concrete build: generate a repo descriptor that names components, symbol boundaries, constraints, and data flow, keep it in version control, and feed it to the agent at task start.

The near-term user is the team already running Claude Code, Cursor, or similar tools on a medium-sized codebase where agents spend too many turns on grep, file search, and module reading. The cheap check is simple: compare explore/edit ratios and tool-call counts on a fixed set of code localization and patch tasks before and after adding the descriptor. The format question looks secondary for model performance. The paper reports similar comprehension across S-expression, JSON, YAML, and Markdown, while JSON had the lowest silent corruption in error injection tests and S-expressions caught structural completeness errors more reliably. That points to an adoption path where teams pick the format that best fits their tooling and validation needs, then enforce it with schema checks in CI.

### Evidence
- [Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents](../Inbox/2026-04-11--formal-architecture-descriptors-as-navigation-primitives-for-ai-coding-agents.md): Architecture descriptors reduced navigation steps and an auto-generated descriptor improved task accuracy.
- [Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents](../Inbox/2026-04-11--formal-architecture-descriptors-as-navigation-primitives-for-ai-coding-agents.md): The paper frames codebase exploration overhead as the operational pain for coding agents.

## Harness-managed typed memory pages for long-running coding sessions
Agent builders now have enough evidence to move long-session memory control out of prompt text and into the harness. The operational pain is familiar in coding sessions that run across many context windows: plans disappear after compaction, constraints are dropped on reset, and the agent repeats tool calls because it cannot tell what state is still valid. ClawVM proposes a concrete implementation: store state as typed pages, define a minimum-fidelity representation for each page type, assemble prompts in two phases so required state always lands first, and require validated writeback at lifecycle boundaries.

The reported gains are large enough to support a build decision. Across four workload families and six token budgets, ClawVM reduced mean policy-controllable faults from 67.8 in a retrieval baseline and 1.5 in a compaction-plus-retrieval baseline to zero when the minimum-fidelity set fit in budget. On 12 real traces and 30 task replays, it also reported zero policy-controllable faults and 100% success at the tightest budget, with median policy overhead under 50 microseconds per turn. A practical first deployment would target coding agents that keep plans, constraints, evidence, and user preferences across long sessions. The first test is whether typed memory pages cut duplicate tool calls, lost-plan incidents, and reset failures on your own traces without pushing latency high enough for users to notice.

### Evidence
- [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](../Inbox/2026-04-11--clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md): ClawVM reports zero policy-controllable faults under fit-to-budget conditions and describes the typed-page memory policy.
- [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](../Inbox/2026-04-11--clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md): The abstract states that harness-managed residency and durability are the enforcement point for long-running tool-using agents.

## Offline JSON Patch plan rewriting for expensive DataFusion queries
Database teams working on Apache DataFusion can trial an LLM-assisted physical-plan rewriter that edits plans with JSON Patch and keeps only rewrites that execute faster. This is a narrow workflow, but the mechanism is concrete and the user-visible effect is clear. The system serializes the physical operator graph into a compact JSON form, asks the model for localized edits such as join reordering, validates candidate plans by execution, and iterates from the improved plan.

The main case study moved a `d_year=2001` filter earlier in the plan, cutting a sales table from 15.1 million rows to 2.9 million before later joins. That run reported a 4.78x speedup, hash-table build time dropping from 10.16 seconds to 0.41 seconds, and build memory falling from 3.3 GB to 411 MB. Median gains on generated TPC-H and TPC-DS workloads were smaller, around 1.1x to 1.2x, so this fits best as a targeted tuning pass for complex OLAP queries where cardinality estimation is weak. A cheap validation path is to run the patch loop offline on a saved set of bad plans, require semantic equivalence through execution, and log which operator edits recur often enough to harden into native optimizer rules.

### Evidence
- [AI for Systems: Using LLMs to Optimize Database Query Execution](../Inbox/2026-04-11--ai-for-systems-using-llms-to-optimize-database-query-execution.md): The summary gives the JSON Patch mechanism and the measured speed and memory improvements in Apache DataFusion.
- [AI for Systems: Using LLMs to Optimize Database Query Execution](../Inbox/2026-04-11--ai-for-systems-using-llms-to-optimize-database-query-execution.md): The content describes DBPlanBench exposing compact physical plans to the LLM because native plans are too large to reason over directly.
