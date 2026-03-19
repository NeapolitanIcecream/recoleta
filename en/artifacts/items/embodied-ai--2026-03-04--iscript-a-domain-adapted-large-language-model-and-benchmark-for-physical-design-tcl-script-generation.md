---
source: arxiv
url: http://arxiv.org/abs/2603.04476v1
published_at: '2026-03-04T15:20:35'
authors:
- Ning Xu
- Zhaoyang Zhang
- Senlin Shu
- Lei Qi
- Jiaqi Lv
- Wensuo Wang
- Tianhao Zhao
- Chao Zhang
- Zhaoliang Yang
- Xiangyu Li
- Zhaorui Su
- Jingshan Li
- Xin Geng
topics:
- eda-llm
- tcl-generation
- domain-adaptation
- benchmarking
- code-generation
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# iScript: A Domain-Adapted Large Language Model and Benchmark for Physical Design Tcl Script Generation

## Summary
This paper proposes iScript, a domain-adapted model for physical design Tcl script generation, along with the first corresponding benchmark, iScript-Bench. The core contribution is the construction of a fully reproducible pipeline for data synthesis, training, and evaluation in the EDA setting, where public data is scarce and real execution-based verification is difficult.

## Problem
- Physical design flows rely heavily on Innovus Tcl scripts, but general large language models are weak at generating this type of **tool-specific, semantically tightly coupled, and highly fault-intolerant** script.
- There is very little publicly available PD Tcl data, resulting in a lack of both training data and a unified benchmark, making fair comparison between models difficult.
- Real functional verification typically requires execution with commercial EDA tools, which is costly and not reproducible; syntax checking alone is insufficient to determine whether a script satisfies the design intent.

## Approach
- Based on **Qwen3-8B**, the authors perform domain adaptation and propose iScript. Training uses two stages: first **continued pretraining (CPT)** to learn Innovus Tcl syntax and vocabulary, then **supervised fine-tuning (SFT)** with **Chain-of-Thought** to learn the mapping from “requirement → script.”
- They design a multi-stage data synthesis pipeline: collect seed data from user guides, command manuals, forums, and communities; extract commands and parameter combinations to generate scripts; filter them through **static linting**; then use **GPT-4.1** to infer requirements backward and generate CoT, ultimately producing **10,000** `(requirement, CoT, script)` samples.
- They build **iScript-Bench**: covering **5** main task categories, **25** subcategories, and **3** difficulty levels, for a total of **116** test tasks, to systematically evaluate natural-language-to-PD-Tcl capability.
- They propose a two-step verification framework: first perform **static syntax verification** in a lightweight sandbox, then use an LLM with prompts enhanced by official command knowledge to perform **functional evaluation**, replacing expensive execution with commercial tools.

## Results
- On **iScript-Bench (116 tasks)**, iScript’s overall **Pass@1** scores are: **syntax 59.48% / function 18.97%**. Compared with the second-best **Gemini** at **31.03% / 14.66%**, this is an improvement of **28.45** and **4.31** percentage points, respectively.
- At **Pass@5**, iScript achieves **syntax 91.38% / function 46.55%** overall. Compared with **Gemini 73.28% / 39.66%**, this is an improvement of **18.10** and **6.89** percentage points, respectively.
- By category, iScript reaches **Pass@5 syntax 100.00%, function 71.43%** on **DIQA**; **95.45% / 40.91%** on **FA**; and **100.00% / 33.33%** on **PAO**. However, on **NIAA Pass@1 function**, it achieves only **10.00%**, weaker than **Gemini/Claude’s 30.00%**, indicating that it does not lead comprehensively on every subtask.
- By difficulty, iScript’s **Pass@1/5 syntax** on **L1** is **66.67% / 94.44%**, and even on the hardest **L3** it still reaches **61.54% / 88.46%**. The corresponding **Pass@1/5 function** is **11.54% / 19.23%**, showing that functional correctness under complex logic remains difficult, though its robustness is better than that of most general-purpose models.
- To validate the reliability of LLM-based functional evaluation, the authors randomly sampled **100** out of **784** syntactically correct scripts for engineer review: the LLM judged **39** as correct, humans judged **42** as correct, and **all 39 scripts judged correct by the LLM were included in the human-correct set**, indicating that the automatic evaluation has near-perfect precision and almost no false positives.

## Link
- [http://arxiv.org/abs/2603.04476v1](http://arxiv.org/abs/2603.04476v1)
