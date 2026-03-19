---
source: arxiv
url: http://arxiv.org/abs/2603.08993v1
published_at: '2026-03-09T22:29:47'
authors:
- Tony Mason
topics:
- llm-agents
- system-prompt-analysis
- prompt-interference
- multi-model-evaluation
- coding-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Arbiter: Detecting Interference in LLM Agent System Prompts

## Summary
This paper proposes Arbiter, a framework for auditing LLM agent system prompts as "software artifacts" and detecting internal instruction interference and architectural failure modes within them. The authors conduct a cross-vendor analysis on the prompts of three coding agents—Claude Code, Codex CLI, and Gemini CLI—and emphasize that complementary review by multiple models is better than single-model analysis at uncovering different categories of problems.

## Problem
- The paper addresses the fact that LLM agent system prompts are often long and complex, yet lack the type checking, linting, and testing used in traditional software. As a result, internal contradictions may be silently "smoothed over" by the executing model, leading to unstable behavior that is hard to diagnose.
- This matters because system prompts effectively define an agent's tool usage, workflow, safety boundaries, and memory mechanisms; once internal conflicts exist, the agent may make inconsistent or even dangerous decisions across different invocations.
- The authors also argue that the same LLM responsible for executing a prompt is not suitable to serve as its own auditor, so an external, formalized, cross-model detection mechanism is needed.

## Approach
- The core method is a two-stage framework called **Arbiter**: first **directed analysis**, then **undirected scouring**. It can be understood as "first systematically checking errors by rules, then letting multiple different models freely explore unknown issues."
- Directed analysis splits the prompt into blocks and labels each block with hierarchy, category, tone, and scope; it then uses five rule classes to check for interference between blocks, such as mandate-prohibition conflict, scope overlap redundancy, priority ambiguity, implicit dependency, and verbatim duplication.
- To avoid exhaustively enumerating all block pairs, the method first uses scope and tone for pre-filtering, reducing roughly 15,680 candidate checks on Claude Code to 100–200 relevant pairs.
- Undirected scouring hands the prompt to multiple different LLMs and gives them intentionally vague instructions to "read and find interesting things"; in each round, they see findings from prior rounds and try to explore still-uncovered areas, continuing until three consecutive models all conclude there is no need to continue.
- The authors also add a prompt AST structural analysis layer that parses the prompt into a document tree for structural profiling, clone detection, and version diffing, though this is more of a supporting analysis tool than the main source of results.

## Results
- Across the three vendors, undirected scouring found **152** issues in total: Claude Code **116**, Codex CLI **15**, and Gemini CLI **21**; the numbers of rounds required for convergence were **10 / 2 / 3**, respectively, and total API cost was only **$0.27**.
- In directed analysis of Claude Code, the authors divided the prompt into **56** blocks and identified **21** interference patterns: **4** critical direct contradictions, **13** scope overlaps, **2** priority ambiguities, and **2** implicit dependencies; **20/21 = 95%** were judged to be statically detectable.
- In terms of severity distribution, the undirected scouring results for Claude Code were Curious **34 (29%)**, Notable **36 (31%)**, Concerning **34 (29%)**, and Alarming **12 (10%)**; for Codex CLI they were **3/7/5/0**; for Gemini CLI **4/9/6/2**. Based on this, the authors claim that prompt architecture is strongly correlated with "failure class" but not strongly correlated with "severity."
- The main architectural conclusion is that **monolithic** Claude Code is more prone to growth-driven contradictions at subsystem boundaries, **flat** Codex CLI is more consistent but expresses fewer capabilities, and **modular** Gemini CLI is more prone to design-level bugs in the seams between composed modules.
- One of the strongest external validation cases comes from Gemini CLI: the scourer found that the XML schema for its history compression lacked a field for preserving user memory, causing saved preferences to be structurally lost after compression. The authors say Google later independently filed and patched the related P0 compression bug, but **did not** fix the schema-level root cause they identified.
- The main methodological breakthrough claimed is not higher accuracy on traditional task benchmarks, but that "**multiple models discover categorically different problems**": for example, resource/economic risk, permission-pattern vulnerabilities, data integrity, and trust-architecture flaws are each areas where different models excel, and single-model analysis cannot cover this complementarity.

## Link
- [http://arxiv.org/abs/2603.08993v1](http://arxiv.org/abs/2603.08993v1)
