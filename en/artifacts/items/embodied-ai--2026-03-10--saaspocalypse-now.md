---
source: hn
url: https://hantverkskod.se/2026/03/01/saaspocalypse/
published_at: '2026-03-10T23:10:46'
authors:
- mosura
topics:
- agentic-coding
- developer-tools
- ai-workflow
- context-management
- event-log
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# SaaSpocalypse Now

## Summary
This article is not a robotics/AI research paper, but an engineering reflection on an "AI agent programming workflow." The author argues that, compared with buying SaaS/workflow products, generative AI makes it more worthwhile for developers to build a lightweight, customizable "agent memory" tool themselves.

## Problem
- The author believes that the existing approach of providing context to an agent through a pile of Markdown files is arbitrary, hard to maintain, and, as a project grows, forces the agent to repeatedly parse unstructured text inefficiently.
- Developers need a more structured and sustainable way to record tasks, decisions, and project state so they can quickly construct the required context each time a task is executed.
- This matters because generative AI/agentic coding is changing the cost balance between "buy off-the-shelf SaaS" and "build it yourself," and workflow tools may become the next core productivity bottleneck.

## Approach
- The author borrows Beads' core idea: record all operations and decisions in database-like persistent storage rather than scattering them across Markdown files.
- They implemented an extremely minimal tool called Shelby: a single executable file that can be dropped directly into any project to provide the agent with "better memory."
- Shelby uses an append-only JSONL event log to record data; the author calls these records mementos. Before each command runs, it reconstructs the current state by replaying the log.
- Once a task is identified, `shelby context <id-or-alias>` generates the precise context the agent needs for that task, instead of scanning global files.
- The tool is also designed with collaboration among multiple parallel agents in mind, although the author says they have not actually used this capability yet.

## Results
- The article does not provide formal experiments, benchmark datasets, or quantitative comparison results with existing systems.
- The most concrete engineering result is that the author built Shelby in **7 evenings**, with **5,168 lines of Rust code**, **120 unit tests**, and **60 integration tests**.
- The author's main concluding claim is that generative AI has significantly shifted the economics in favor of "building your own tools" relative to "buying SaaS/workflow products," but this is an opinion-based judgment rather than a rigorous experimental conclusion.
- The author also claims that the biggest current area for improvement in agentic coding is not capability but **speed**; at present, developers use **multi-agent orchestration** to compensate for the inefficiency of "single-threaded" interaction, but no quantified gains are provided.

## Link
- [https://hantverkskod.se/2026/03/01/saaspocalypse/](https://hantverkskod.se/2026/03/01/saaspocalypse/)
