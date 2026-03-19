---
source: arxiv
url: http://arxiv.org/abs/2603.08993v1
published_at: '2026-03-09T22:29:47'
authors:
- Tony Mason
topics:
- llm-agents
- prompt-analysis
- coding-agents
- multi-model-evaluation
- system-prompt-testing
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Arbiter: Detecting Interference in LLM Agent System Prompts

## Summary
This paper presents Arbiter, which treats system prompts for LLM coding agents as testable software artifacts and analyzes them to detect “instruction interference/conflicts.” The authors conduct a cross-model, cross-architecture analysis on prompts from three vendors—Claude Code, Codex CLI, and Gemini CLI—and claim they can uncover different kinds of structural failure modes at extremely low cost.

## Problem
- System prompts for LLM agents effectively determine agent behavior, but unlike traditional software they lack type checking, linting, or tests; when they contain internal contradictions, the model will “quietly smooth them over,” leading to unstable and unauditable behavior.
- Having the same LLM that executes a prompt also audit that prompt is unreliable, because it may mask conflicts using its own heuristics; this is especially important for coding agents, since the prompt controls tool usage, state management, workflows, and security boundaries.
- Existing research focuses more on prompt engineering or prompt injection, rather than on the internal consistency and compositional defects of system prompts themselves as software architecture.

## Approach
- Arbiter has two stages: **directed evaluation** first splits the prompt into labeled blocks (hierarchy, category, tone, scope), then uses formal rules to check for interference between block pairs, such as mandate/prohibition conflicts, scope overlap, priority ambiguity, implicit dependencies, and verbatim duplication.
- To avoid the cost of exhaustive enumeration, the authors apply rule-based prefiltering, reducing the theoretical ~15,680 block-pair/rule combinations on Claude Code to 100–200 relevant checks.
- **undirected scouring** then has multiple different LLMs use very open-ended instructions to “look for interesting problems”; each round inherits what previous rounds have already found, encouraging later models to explore new areas; the process stops when 3 consecutive models all judge that no further searching is needed.
- The core idea is “external auditing + multi-model complementarity”: different models bring different analytic biases, so the goal is not consensus but using those differences to discover vulnerability classes that a single model would miss.
- The authors also build a prompt AST, parsing documents into a structural tree and performing structural hashing/diffing to quantify prompt architecture and cross-version changes.

## Results
- Across the three agents, undirected scouring produced **152 findings** in total: Claude Code **116**, Codex CLI **15**, Gemini CLI **21**; the numbers of convergence rounds were **10/2/3** respectively, with a total API cost of just **$0.27** (approximately **$0.236 / $0.012 / $0.014** respectively).
- In the directed analysis of Claude Code, the authors manually classified **56** blocks and labeled **21** interference patterns: **4** critical direct conflicts, **13** scope overlaps, **2** priority ambiguities, and **2** implicit dependencies; **20/21 (95%)** are claimed to be statically detectable.
- In terms of severity distribution, Claude Code’s scourer results were **34 curious (29%) / 36 notable (31%) / 34 concerning (29%) / 12 alarming (10%)**; Codex CLI had **3/7/5/0**; Gemini CLI had **4/9/6/2**. Based on this, the authors argue that longer, more monolithic prompts have a larger surface area for severe conflicts.
- The authors’ central empirical conclusion is that **prompt architecture is strongly correlated with failure class, but not strongly correlated with severity**. Monolithic Claude is more prone to growth-related conflicts at subsystem boundaries; flat Codex is more consistent but more limited in capability; modular Gemini shows design-level bugs in the seams between modules.
- The strongest case on Gemini CLI is **structural data loss** in the memory compression pipeline: preferences saved by `save_memory` do not enter the compressed XML `state_snapshot`, which the authors say means preferences are “structurally guaranteed to be deleted” when compression occurs. The paper also claims that Google later independently filed and fixed a related compression-symptom bug, but **did not fix the schema-level root cause identified here**.
- Methodologically, the authors emphasize that multiple models did in fact find **categorically different** problems, not just more problems; for example, Claude leaned toward structure/safety, Kimi toward economics and resource exhaustion, and GLM toward data integrity. For Claude Code, **116 findings corresponded to 107 unique categories**, which is used to support the claim of “model complementarity rather than redundancy.”

## Link
- [http://arxiv.org/abs/2603.08993v1](http://arxiv.org/abs/2603.08993v1)
