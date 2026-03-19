---
source: arxiv
url: http://arxiv.org/abs/2603.11356v1
published_at: '2026-03-11T22:43:55'
authors:
- Jatin Ganhotra
- Sami Serhan
- Antonio Abu Nassar
- Avraham Shinnar
- Ziv Nevo
- Martin Hirzel
topics:
- java-issue-resolution
- software-engineering-agent
- static-analysis-tools
- react-agents
- code-repair
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Resolving Java Code Repository Issues with iSWE Agent

## Summary
This paper presents iSWE Agent, a specialized agent for automatic issue fixing in Java code repositories. It improves the effectiveness and cost efficiency of automated repair in Java scenarios by splitting the task into two sub-agents—one for problem localization and one for generating edits—and combining them with rule-based static analysis tools.

## Problem
- Existing automated issue-fixing systems are mostly optimized around Python, and perform significantly worse on Java, even though Java is highly important in enterprise software.
- Java code often involves more cross-file changes, strong static typing, and dependency-driven build processes, making it harder to reliably fix issues using only general-purpose LLMs or lightweight tools.
- The research question is whether Java issue fixing requires language-specific knowledge and tools, and whether such a design can significantly improve success rate and efficiency on public benchmarks.

## Approach
- The task is split into two ReAct sub-agents: the **localization agent** first identifies the files/classes/methods that should be modified based on the issue description and codebase; the **editing agent** then generates patches based on those locations.
- The localization sub-agent is provided with 7 **read-only Java static analysis tools**, such as file/class/method/symbol queries, inheritance hierarchy, callers, and call chains, built on CLDK and Tree-Sitter.
- The localization result is first output by the LLM as simplified JSON, then a **rule-based sanitizer** fills in line numbers and scopes and resolves conflicts, reducing the instability of purely LLM-generated output.
- The editing sub-agent uses **merge-conflict-style search-replace** to generate patches, and performs layered validation on candidate edits: formatting checks, match repair, Java linter, and finally project build/compilation execution in a container.
- The overall design emphasizes combining **rules + models**: relying less on arbitrary bash/code execution, reducing side effects, lowering the number of iterations, and enabling containerized environments only when necessary.

## Results
- The paper claims that iSWE achieves **state-of-the-art** or near-top issue resolution rates on both the **Multi-SWE-bench Java subset (128 instances)** and the **SWE-PolyBench Java subset (165 instances)**.
- The total evaluation covers **293 Java instances (128 + 165)**, which is the main experimental scale used by the authors to support their conclusions.
- In terms of cost, the authors claim that when **using the same base LLM**, iSWE's model API inference cost is **2× to 3×** lower than that of other leading agents.
- The paper also states that the results section analyzes **localization precision/recall** and performance broken down by issue complexity, but the provided excerpt **does not include the specific values of these metrics**.
- Qualitatively, the paper’s strongest claim is that a Java-specific toolchain not only improves repair success rate, but also reduces LLM rounds, lowers the risk of side effects, and is better suited to enterprise-grade Java repositories.

## Link
- [http://arxiv.org/abs/2603.11356v1](http://arxiv.org/abs/2603.11356v1)
