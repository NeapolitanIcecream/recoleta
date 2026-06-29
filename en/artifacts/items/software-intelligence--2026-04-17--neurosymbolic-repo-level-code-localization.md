---
source: arxiv
url: http://arxiv.org/abs/2604.16021v2
published_at: '2026-04-17T12:49:18'
authors:
- Xiufeng Xu
- Xiufeng Wu
- Zejun Zhang
- Yi Li
topics:
- repo-level-code-localization
- neurosymbolic-reasoning
- datalog
- code-intelligence
- software-engineering-agents
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Neurosymbolic Repo-level Code Localization

## Summary
This paper argues that current repo-level code localization benchmarks reward keyword matching more than structural reasoning. It introduces a keyword-agnostic benchmark and a neurosymbolic system, LogicLoc, that translates natural language into Datalog queries over extracted program facts.

## Problem
- The paper targets repo-level code localization when the query does not contain file names, class names, function names, or other lexical anchors.
- This matters because autonomous software engineering agents need to find the right code from intent alone, and issue-based benchmarks such as SWE-bench often let systems win by matching keywords from stack traces or identifiers.
- The authors call this failure mode the **Keyword Shortcut** and claim current methods collapse when they must reason over repository structure instead of surface text.

## Approach
- The authors define **Keyword-Agnostic Logical Code Localization (KA-LCL)** and build **KA-LogicQuery**, a diagnostic benchmark of **25** logical queries with ground-truth locations and no naming hints.
- LogicLoc first runs static analysis on the repository to extract **program facts** such as functions, classes, containment, inheritance, imports, calls, references, and optional control/data-flow relations.
- An LLM reads the natural-language query and writes a **Datalog** program that expresses the structural conditions to match in those facts.
- The system uses **parser-gated validation** plus a **synthesize-check-refine** loop. It repairs simple syntax issues, executes partial rules, inspects empty intermediate relations, and uses mutation-based diagnostics to help the LLM fix over-constrained rules.
- The validated query runs in the **Soufflé** Datalog engine, which returns exact code locations and can also return no result when nothing matches.

## Results
- The paper claims a **catastrophic** drop for state-of-the-art localization methods on **KA-LogicQuery**, but the excerpt does **not** provide exact scores, datasets-per-method tables, or absolute deltas.
- It claims **LogicLoc significantly outperforms SOTA methods on KA-LogicQuery**, though the excerpt gives no exact metric values or named baseline numbers.
- It also claims LogicLoc keeps **competitive performance on issue-driven benchmarks** such as **SWE-bench**, again without quantitative values in the provided text.
- The authors state that LogicLoc uses **fewer tokens** and runs **faster** than iterative LLM-heavy approaches because structural traversal is handled by the deterministic Datalog engine, but the excerpt gives no token counts or latency numbers.
- The concrete example in the paper shows a query for functions with **more than 15 parameters** and excluding `__init__`, and the system returns **2** matches: `astropy/convolution/convolve.py: convolve_fft` with **19** parameters at line **442**, and `astropy/io/fits/column.py: _verify_keywords` with **17** parameters at line **952**.

## Link
- [http://arxiv.org/abs/2604.16021v2](http://arxiv.org/abs/2604.16021v2)
