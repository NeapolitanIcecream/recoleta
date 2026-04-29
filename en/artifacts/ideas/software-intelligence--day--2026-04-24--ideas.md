---
kind: ideas
granularity: day
period_start: '2026-04-24T00:00:00'
period_end: '2026-04-25T00:00:00'
run_id: f9f4ae89-06b0-46d4-b288-2d12297bfb6b
status: succeeded
topics:
- coding-agents
- token-cost
- repo-level-generation
- verification
- traceability
- agent-safety
tags:
- recoleta/ideas
- topic/coding-agents
- topic/token-cost
- topic/repo-level-generation
- topic/verification
- topic/traceability
- topic/agent-safety
language_code: en
pass_output_id: 107
pass_kind: trend_ideas
upstream_pass_output_id: 106
upstream_pass_kind: trend_synthesis
---

# Code Change Control

## Summary
The clearest near-term changes are operational. Coding-agent products need explicit token controls during execution, repo-scale generation needs dependency-ordered workflows once projects get larger, and maintenance teams can justify a traceability layer that links requirements to code with smaller context and visible evidence.

## Repo-aware token budget controller for coding-agent runs
Engineering teams using coding agents need a cost gate before long-horizon runs, with a hard stop on repeated file viewing and editing. The evidence is no longer limited to vague complaints about expensive agents. On SWE-bench Verified in OpenHands, agentic coding used about 3500× more tokens than single-round code reasoning and about 1200× more than multi-turn code chat, with runs on the same task differing by up to 30×. The paper ties the worst failures to redundant search behavior, especially repeated file access and edits, and it shows that models are poor at forecasting their own token bill before they start.

A practical build is a repo-aware budget controller that watches action traces in real time and cuts the run into smaller scopes when the agent starts thrashing. The control point is simple: count file opens, revisits, edit reversions, and context growth, then require either a narrower subtask or human approval once those counters cross a threshold. Teams already paying for autonomous bug fixing or feature work would care first, because they absorb the cost of failed trajectories and usually do not get a reliable estimate upfront.

A cheap test is to replay past agent traces and measure how often an early stop after repeated file churn would have reduced token spend without hurting pass rate. If the controller mostly catches failures and late-stage wandering, it is worth shipping as a default guard in coding-agent products.

### Evidence
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): Token-cost study reports 3500× and 1200× cost gaps, up to 30× run variance, and poor self-prediction.
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): Paper excerpt ties higher cost to repeated actions and shows input-heavy cost growth.

## Dependency-ordered file generation for repositories above 1000 LOC
Repo-level generation workflows should split planning from implementation once a project passes roughly 1000 lines of code. RealBench shows current models still struggle on full repositories even when they receive natural-language requirements and UML package and class diagrams. The best average Pass@1 is 19.39%, performance is above 40% below 500 LOC and below 15% above 2000 LOC, and only 44.73% of methods are standalone on average. In the largest repositories, standalone methods drop to 26.23%, which points to dependency handling as the main source of failure.

The concrete workflow change is to stop asking a model for whole-repo output on medium and large codebases. Use the model first to map modules, interfaces, and dependency edges from the design artifacts, then generate files incrementally with tests after each step. RealBench’s own comparison supports this: whole-repo generation works better on smaller repositories, while incremental generation works better once repositories get larger.

A cheap check is to take an internal backlog item that already has architecture notes or diagrams and run it both ways: one-shot full-repo generation versus dependency-ordered file generation. Measure test pass rate, number of broken imports, and manual repair time. Teams building internal scaffolds, SDKs, or CRUD-heavy services can try this without changing their whole toolchain.

### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): RealBench summary provides Pass@1 by repository scale and dependency statistics.
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): Paper excerpt states smaller repos favor whole-repo generation while complex repos favor incremental generation.

## Pull-request traceability sidecar for requirement-linked impact analysis
Requirements traceability can now justify a narrower maintenance tool that links a changed requirement to the file, class, or method most likely to break, while keeping context small enough to run in everyday development. R2Code reports an average F1 gain of 7.4% over strong baselines across five datasets and cuts token use by up to 41.7% with adaptive context control. The mechanism matters for product design: it decomposes requirements and code into aligned semantic parts, checks the explanation for each proposed link, and adjusts retrieval depth to the complexity of the requirement.

That supports a concrete build for teams with stale tickets, weak documentation, or regulated change review: a pull-request sidecar that takes a requirement ID, proposes the code links, shows the explanation for each link, and flags low-consistency matches for review. This is more useful than broad code chat when the job is impact analysis or audit preparation, because the user needs a compact evidence trail tied to named artifacts.

A cheap check is to sample resolved tickets from one service, hide the known touched files, and compare the tool’s top-k link suggestions against the actual implementation diff. If the links are accurate enough to cut search time for maintainers, the traceability layer earns its place before any broader agent workflow.

### Evidence
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): R2Code summary reports F1 gains, adaptive retrieval, and lower token use.
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): Paper excerpt states 7.4% average F1 gain and up to 41.7% token reduction.
