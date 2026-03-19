---
source: hn
url: https://hantverkskod.se/2026/03/01/saaspocalypse/
published_at: '2026-03-10T23:10:46'
authors:
- mosura
topics:
- agent-memory
- developer-tools
- agentic-coding
- event-sourcing
- multi-agent
- saas-disruption
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# SaaSpocalypse Now

## Summary
This article argues that generative AI has significantly lowered the barrier to “building a tool yourself” relative to buying SaaS, and uses the author’s self-built Shelby as an example of how to provide more controllable project memory for agentic coding. The core point is not to propose a new model, but to demonstrate a lightweight agent workflow infrastructure that can be embedded locally in a repository.

## Problem
- The article addresses the **context and memory management problem in agentic AI development**: project state is scattered across arbitrary Markdown files, making it neither structured nor easy to maintain over the long term.
- This matters because agents must repeatedly parse large amounts of global documentation to understand task background, causing inefficiency and fragility, and becoming harder to scale as the project grows.
- The author also implicitly points to a broader industry problem: when AI makes customized development cheap, many software products that sell fixed workflows may lose their value.

## Approach
- The core method is simple: record “what was done and what was decided” in an **append-only JSONL event log** instead of relying on scattered Markdown; the author calls these records *mementos*.
- Each time a Shelby command runs, it first **replays the event log to reconstruct the current state**, thereby producing the project’s latest structured memory.
- When an agent needs to handle a task, use `shelby context <id-or-alias>` to **generate the needed context for that task on demand**, avoiding blind retrieval through global documentation.
- The tool is implemented as a **single self-contained executable** that can be dropped directly into any project; on first use, `shelby help agent` guides the setup of the development loop in `AGENTS.md`.
- The design also considers **multiple parallel agents**, although the author says this has not yet actually been put into use.

## Results
- The article does not provide standard academic benchmarks, public datasets, or quantitative comparison results against other systems.
- The most concrete engineering result given is that the author completed Shelby in **7 evenings**, with an implementation size of **5,168 lines of Rust code**.
- For test coverage, the article reports **120 unit tests** and **60 integration tests**.
- The author claims Shelby has already reached a usable state and is being used for “**building Shelby with Shelby**,” which is presented as the strongest practical validation case.
- The qualitative conclusion is that a structured event log is better suited than random Markdown for agent memory; the main bottleneck in current agent programming is not capability but **speed**, so the next direction will shift toward **multi-agent orchestration**.

## Link
- [https://hantverkskod.se/2026/03/01/saaspocalypse/](https://hantverkskod.se/2026/03/01/saaspocalypse/)
