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
- software-effort-estimation
- story-point-estimation
- large-language-models
- few-shot-learning
- software-engineering
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Story Point Estimation Using Large Language Models

## Summary
This paper investigates whether large language models can perform story point estimation in agile development when there is little to no project-specific labeled data. The conclusion is: zero-shot LLMs already outperform supervised deep learning baselines that require 80% training data, and a small number of examples can further improve performance.

## Problem
- The goal is to automate **story point estimation in agile software development**: predicting development effort from a task’s title and description.
- This matters because manual estimation is subjective, time-consuming, and hard to scale; meanwhile, existing supervised models usually require **large amounts of labeled historical data from the same project**, making them impractical for new projects or cold-start scenarios.
- The paper also asks a related question: compared with directly assigning story points, is **pairwise comparison of which task requires more effort** easier for LLMs to learn, and can it serve as a less labor-intensive few-shot supervision signal.

## Approach
- The authors evaluate **4 off-the-shelf LLMs** across **16 real software projects** (Kimi, DeepSeek, Gemini Flash Lite, OpenAI GPT-5 Nano), using backlog item titles + descriptions as input.
- They design four types of experiments: **zero-shot story point prediction**, **few-shot story point prediction**, **zero-shot pairwise comparative judgment**, and **using a small number of pairwise comparison examples to assist story point prediction**.
- In the few-shot setting, each project is given only **5 examples**, and two sampling strategies are compared: sampling by frequent story point values (Count) and sampling to cover the numeric range (Scale).
- The main evaluation metrics are **Pearson correlation coefficient ρ** and **Spearman rank correlation rs** between predicted and ground-truth story points; the pairwise comparison task uses **accuracy**.
- On the output side, the system uses strict prompting + JSON parsing + regex fallback to stably extract integer story points or binary comparison decisions from LLM responses.

## Results
- **Zero-shot already outperforms supervised baselines**: averaged over 16 projects, the supervised baseline SBERT regression (trained on **80%** of project data) achieves **ρ=0.3175**; zero-shot **Kimi ρ=0.3735** and **DeepSeek ρ=0.4040** are both higher; Gemini is **0.2363**, and OpenAI is **0.2712**. The comparative-judgment baseline lists supervised comparative at **ρ=0.3337**, which DeepSeek and Kimi also exceed.
- On **Spearman rs**, the project-level results reported in the paper likewise show that Kimi/DeepSeek generally outperform traditional supervised baselines; for example, in the **clover** project, SBERT regression has **rs=0.4166**, Kimi **0.5043**, and DeepSeek **0.6358**.
- Looking at per-project **Pearson ρ**, DeepSeek leads substantially on several projects, for example **clover 0.8364 vs supervised regression 0.4403**, **bamboo 0.3479 vs 0.1768**, and **titanium 0.4038 vs 0.1861**, indicating that zero-shot LLMs can deliver large gains on some projects.
- The paper claims that **few-shot prompting further improves** zero-shot performance, with only a very small number of examples needed to better calibrate project-specific story point scales; and **comparative judgment examples can also improve story point prediction**. However, in the provided excerpt, the full quantitative tables for RQ2/RQ4 are not included, so the average improvement values cannot be listed item by item.
- On the question of whether “comparative judgments are easier,” the authors conclude that they are **not easier than directly estimating story points**; that is, LLMs show no clear inherent advantage on pairwise judgments.
- The strongest overall takeaway is: **LLMs can match or exceed traditional supervised methods without labeled data, and improve further with only a few examples**; this makes them especially suitable for software estimation in **data-scarce / cold-start** project settings.

## Link
- [http://arxiv.org/abs/2603.06276v1](http://arxiv.org/abs/2603.06276v1)
