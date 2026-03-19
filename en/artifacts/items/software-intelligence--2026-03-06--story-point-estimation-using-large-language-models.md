---
source: arxiv
url: http://arxiv.org/abs/2603.06276v1
published_at: '2026-03-06T13:34:09'
authors:
- Pranam Prakash Shetty
- Adarsh Balakrishnan
- Mengqiao Xu
- Xiaoyin Xi
- Zhe Yu
topics:
- story-point-estimation
- large-language-models
- agile-software-development
- few-shot-learning
- comparative-judgment
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Story Point Estimation Using Large Language Models

## Summary
This paper studies whether large language models can perform story point estimation in agile development with almost no within-project labeled data. The conclusion is: zero-shot LLMs already outperform supervised deep learning baselines trained on 80% of the data, and a small number of examples can further improve performance.

## Problem
- The paper addresses the problem of **story point estimation for user stories/backlog items in software projects**, which directly affects sprint planning, resource allocation, and delivery predictability.
- Existing supervised methods usually require **a large amount of story point data labeled within the same project**, while new projects or data-scarce projects often cannot obtain these labels.
- The study also examines a less labor-intensive form of supervision: **comparative judgments** (which of two tasks requires more effort), asking whether this is easier for LLMs and whether it can replace a small number of story point labels.

## Approach
- Evaluated 4 off-the-shelf LLMs on 16 real software projects: Kimi, DeepSeek, Gemini Flash Lite, and OpenAI GPT-5 Nano, using backlog item titles and descriptions as input.
- Conducted **zero-shot story point prediction**: no training data provided, the model directly outputs story points, evaluated using Pearson correlation and Spearman rank correlation.
- Conducted **few-shot story point prediction**: only 5 labeled examples per project were provided, and two example selection strategies were compared: sampling by high-frequency story points (Count) and sampling by coverage of the story point scale (Scale).
- Conducted **comparative judgment experiments**: asked the LLM to directly judge which item in a pair requires more effort, to test whether this is easier than directly predicting story points.
- Conducted experiments using **comparative judgments as few-shot context**: gave the model a small number of examples like “task A is larger/smaller than task B,” then asked it to output story points, to see whether this helps calibrate the project-specific scale.

## Results
- **Zero-shot outperforms supervised baselines (average performance)**: across 16 projects, SBERT Regression (using **80% training data**) achieved average Pearson **0.3175**, and the Comparative baseline **0.3337**; among zero-shot LLMs, Kimi reached **0.3735** and DeepSeek **0.4040**, both higher; Gemini **0.2363** and OpenAI **0.2712** were weaker.
- **Zero-shot rank correlation is also stronger**: for average Spearman, traditional Regression scored **0.3037** and Comparative **0.3222**; in the paper’s table, Kimi and DeepSeek exceed these baselines on many projects, for example DeepSeek on appceleratorstudio **0.3885**, aptanastudio **0.4554**, bamboo **0.3784**, and clover **0.6358**.
- **Looking at single-project peaks**: DeepSeek achieved Pearson **0.8364** on clover, clearly higher than that project’s Regression **0.4403** and Comparative **0.4190**; on datamanagement, DeepSeek’s **0.4703** also exceeded Regression’s **0.3775**.
- **Few-shot prompting further improves performance**: the abstract explicitly states that with **only a small number of examples**, LLM story point prediction further improves over zero-shot; and comparative judgments can also serve as few-shot examples to improve prediction performance.
- **Comparative judgments are not easier**: the abstract explicitly states that for LLMs, **predicting comparative judgments is not easier than directly predicting story points**, which differs from the hypothesis that it is easier for humans.
- **Quantitative results are incomplete**: in the provided excerpt, the full numerical tables for RQ2/RQ3/RQ4 are not shown, so the complete average metrics for the few-shot and comparative judgment experiments cannot be listed; however, the paper’s strongest quantitative claim is: **zero-shot LLMs already outperform supervised deep learning models trained on 80% of the data, and few-shot prompting improves further.**

## Link
- [http://arxiv.org/abs/2603.06276v1](http://arxiv.org/abs/2603.06276v1)
