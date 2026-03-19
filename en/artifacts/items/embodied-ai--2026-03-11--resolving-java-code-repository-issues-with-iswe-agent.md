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
- java-code-repair
- issue-resolution
- llm-agents
- static-analysis
- software-engineering-benchmarks
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Resolving Java Code Repository Issues with iSWE Agent

## Summary
This paper proposes iSWE Agent for fixing issues in Java code repositories. By splitting localization and editing into two sub-agents and combining them with Java static analysis and controlled editing tools, it improves the effectiveness and efficiency of automated issue resolution. The authors claim that the method achieves state-of-the-art or near-state-of-the-art repair success rates on two Java benchmarks, while also significantly reducing inference cost.

## Problem
- Existing automated issue resolution systems mostly favor Python and perform relatively weakly on Java, even though Java is very important in enterprise software.
- Java’s strong typing, compilation dependencies, multi-file changes, and object-oriented structure make automated repair harder than in Python, so generic tools or simple linters alone are insufficient.
- A key question is whether **Java-specific tools and language-aware mechanisms** can substantially improve repository-level issue resolution capability.

## Approach
- The task is split into two ReAct sub-agents: the **localization agent** first finds the code locations that need to be modified, and the **editing agent** then generates patches based on those locations.
- Localization uses 7 mainly read-only Java-specific tools, such as class/method/symbol queries, call-chain analysis, and inheritance hierarchy analysis; the underlying implementation uses **CLDK + Tree-Sitter** for rule-based static analysis.
- Editing uses controlled **search-replace / merge-conflict formats** to generate patches, instead of arbitrarily executing bash or code, reducing side effects and lowering the number of LLM interaction rounds.
- The editing stage adopts stepwise validation: it first checks patch format and matching, then performs lightweight Java linting, and only enters containerized project build/compilation checks when necessary, balancing safety and feedback quality.
- The overall system is **LLM-agnostic**; prompts and workflow are orchestrated through PDL, emphasizing the combination of rule-based tools and model-based reasoning.

## Results
- Evaluated on **Multi-SWE-bench (Java, 128 instances)** and **SWE-PolyBench (Java, 165 instances)**, for a total of **293 Java instances**.
- The paper claims that iSWE reaches **state-of-the-art or near-the-top** issue resolution success rates on both public Java leaderboards, but the excerpt **does not provide specific success-rate percentages, comparison-method numbers, or detailed per-leaderboard metrics**.
- On cost, the authors explicitly claim that, compared with other leading agents using the **same LLM**, iSWE reduces model API inference cost by about **2× to 3×**.
- The paper also mentions analysis of other metrics, such as **localization precision / recall** and performance broken down by problem complexity, but the currently provided text **does not include specific values**.
- The strongest verifiable conclusion is that a **Java-specific, rule-enhanced two-stage agent** achieves both stronger performance and lower cost for Java issue resolution.

## Link
- [http://arxiv.org/abs/2603.11356v1](http://arxiv.org/abs/2603.11356v1)
