---
source: arxiv
url: http://arxiv.org/abs/2603.04177v1
published_at: '2026-03-04T15:34:18'
authors:
- Alex Thillen
- "Niels M\xFCndler"
- Veselin Raychev
- Martin Vechev
topics:
- code-refactoring
- llm-agents
- benchmarking
- code-intelligence
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# CodeTaste: Can LLMs Generate Human-Level Code Refactorings?

## Summary
This paper introduces **CODETASTE**, a large-scale code refactoring benchmark for real open-source repositories, designed to measure whether LLMs can not only “execute” refactorings but also autonomously discover refactoring choices consistent with those made by human developers. The conclusion is: current frontier models can perform refactorings reasonably well when given detailed instructions, but when only provided with a vague improvement direction, their alignment with human refactoring preferences remains very weak.

## Problem
- Existing LLM coding agents can generate runnable code, but they tend to accumulate complexity, duplicated code, and architectural debt, leading to poor long-term maintainability.
- Existing refactoring benchmarks are mostly small-scope, low-difficulty tasks and cannot measure whether models can **autonomously identify** what refactoring should be done in real multi-file codebases.
- This problem matters because if automated software production cannot continuously improve code structure, agent-generated codebases will gradually become difficult to extend and maintain, limiting adoption in real engineering settings.

## Approach
- Build **CODETASTE**: mine **100** real large-scale multi-file refactorings performed by human developers from GitHub, covering **87 repositories and 6 languages**.
- For each task, create a reproducible container environment, run the repository test suite, and generate static analysis rules to check whether “bad patterns are removed and good patterns are introduced.” These rules support semantic matching based on ASTs and intra-file data flow.
- Design two evaluation tracks: the **Instructed track** provides detailed refactoring instructions to measure “executing as requested”; the **Open track** provides only a vague improvement focus to measure “whether the model can discover the refactoring humans actually chose.”
- Propose the core metric **alignment score = PASS × IFR**: only when tests pass is adherence to the refactoring intent rewarded; precision is also measured to check whether irrelevant modifications are introduced.
- In the Open track, further test **Direct / Plan / Oracle Multiplan** modes to verify whether “propose first, then implement” better matches human refactoring decisions.

## Results
- The benchmark is large in scale: on average, each task requires modifying **91.52 files** and **2605.39 lines of code**; the most complex task reaches **290 files** and **18821 changed lines**. Each instance runs an average of **1638.53 tests** and checks **93.07** static rules.
- In the **Instructed track**, GPT-5.2 is the strongest, with average alignment of **69.6%**; SONNET 4.5 achieves **32.4%**, GPT-5.1 CODEX MINI **34.6%**, and QWEN3 **11.8%**. This shows that when the required refactoring is known, frontier models can already execute large-scale refactorings fairly well.
- In the same track, GPT-5.2 achieves **76.0%** PASS, significantly higher than SONNET 4.5 at **47.0%** and GPT-5.1 M at **43.0%**; however, all three still have relatively high IFR, at **89.3% / 69.2% / 72.2%** respectively, indicating that the main gap lies in preserving functional correctness rather than understanding the instructions.
- Precision in the Instructed track is close to human performance: SONNET 4.5 at **58.9%**, GPT-5.1 M at **58.5%**, GPT-5.2 at **56.2%**, while humans achieve **57.5%**. This suggests that under clear task specifications, models can generally keep modifications within the relevant scope.
- In the **Open track**, models achieve only very low alignment: the best Direct mode result is just **7.7%** (GPT-5.2), and the paper also summarizes that overall alignment is **below 8% without specific refactoring instructions**, showing that models struggle to independently identify refactoring decisions consistent with humans.
- “Propose first, then implement” helps: in the Open track, GPT-5.2 improves from **7.7%** in Direct mode to **14.1%** in Plan mode; Oracle Multiplan further raises this to **19.4%**. The paper also states that the average improvement is close to **3 percentage points**, with a **relative gain above 50%**, and in some cases IFR relative improvement can reach **72%**. However, broader-scope changes may also reduce PASS by as much as **24%**.

## Link
- [http://arxiv.org/abs/2603.04177v1](http://arxiv.org/abs/2603.04177v1)
