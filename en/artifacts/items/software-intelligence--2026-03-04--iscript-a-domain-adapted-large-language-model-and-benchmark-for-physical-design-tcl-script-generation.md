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
- tcl-script-generation
- domain-adaptation
- benchmarking
- code-generation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# iScript: A Domain-Adapted Large Language Model and Benchmark for Physical Design Tcl Script Generation

## Summary
This paper presents iScript, a domain-adapted large language model for physical design Innovus Tcl script generation, as well as the first corresponding benchmark, iScript-Bench. The core contribution is improving the usability and evaluability of EDA script generation through data synthesis, continued domain pretraining, and two-stage verification.

## Problem
- Physical design flows rely heavily on Tcl scripts, but general LLMs have rarely seen Innovus commands, parameters, and semantic constraints, so their generated results are often unreliable.
- There is very little public PD script data, which means both training data and standardized evaluation are lacking, making fair comparison between models difficult.
- Functional verification with real commercial EDA tools is expensive and hard to reproduce, while syntax checking alone is insufficient to determine whether a script satisfies the design intent.

## Approach
- Domain adaptation is performed based on Qwen3-8B using a two-stage training process: first, continued pretraining targeting Innovus Tcl; then supervised fine-tuning with CoT to learn the mapping from "requirement → script."
- A multi-stage data synthesis pipeline is designed: commands and examples are extracted from manuals, user guides, forums, and communities; scripts are compositionally generated and filtered through static linting; then GPT-4.1 infers requirements in reverse and generates reasoning traces, ultimately producing **10,000** `(requirement, CoT, script)` tuples.
- iScript-Bench is constructed to cover **5** main task categories, **25** subcategories, and **3** difficulty levels, for a total of **116** evaluation samples; the difficulty distribution is L1 **54**, L2 **36**, L3 **26**.
- A two-step verification framework is proposed: first, static syntax checking is performed in a lightweight Innovus-style sandbox; then an LLM with command-knowledge-augmented prompting conducts functional evaluation, replacing expensive real tool execution.

## Results
- On iScript-Bench overall, iScript achieves **Pass@1** of: syntax **59.48%**, function **18.97%**; Gemini achieves **31.03% / 14.66%**, Claude **18.97% / 10.34%**, GPT **7.76% / 2.59%**, and DeepSeek **11.21% / 2.59%**.
- On overall **Pass@5**, iScript reaches: syntax **91.38%**, function **46.55%**; Gemini achieves **73.28% / 39.66%**, Claude **35.34% / 23.28%**, GPT **26.72% / 9.48%**, and DeepSeek **29.31% / 8.62%**.
- By category, iScript reaches **Pass@5** of **100.00%** syntax and **71.43%** function on DIQA; **95.45%** syntax and **40.91%** function on FA; and **100.00%** syntax and **33.33%** function on PAO.
- By difficulty, iScript achieves **Pass@1/Pass@5 syntax** of **66.67%/94.44%** on L1, and still reaches **61.54%/88.46%** on the hardest L3; L3 functional correctness is **11.54%/19.23%**, higher than the near-**0%** levels of Claude and DeepSeek.
- Regarding evaluator reliability, the authors randomly sampled **100** out of **784** syntax-passing samples for engineer review; the LLM judged **39** as correct, humans judged **42** as correct, and the set judged correct by the LLM was a subset of the set judged correct by humans, indicating that the automated functional evaluation is conservative and has almost no false positives.

## Link
- [http://arxiv.org/abs/2603.04476v1](http://arxiv.org/abs/2603.04476v1)
