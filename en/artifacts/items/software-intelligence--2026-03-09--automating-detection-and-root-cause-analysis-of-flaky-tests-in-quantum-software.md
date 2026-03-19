---
source: arxiv
url: http://arxiv.org/abs/2603.09029v1
published_at: '2026-03-09T23:57:55'
authors:
- Janakan Sivaloganathan
- Ainaz Jamshidi
- Andriy Miranskyy
- Lei Zhang
topics:
- quantum-software
- flaky-test-detection
- root-cause-analysis
- large-language-models
- software-maintenance
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# Automating Detection and Root-Cause Analysis of Flaky Tests in Quantum Software

## Summary
This paper proposes an automated pipeline for quantum software that detects flaky tests from repository issues/PRs and further uses large language models for root-cause analysis. Its importance lies in the inherently probabilistic nature of quantum programs, which makes traditional testing more prone to cases where “the same code sometimes passes and sometimes fails,” affecting quality assurance and maintenance efficiency.

## Problem
- The paper addresses the problem of **automated detection and root-cause localization of flaky tests in quantum software**: tests may still randomly pass or fail even when the code has not changed, easily masking real defects and misleading developers.
- This problem is more important in the quantum setting because quantum programs themselves are probabilistic, and rerunning on real hardware is costly, noisy, and difficult to reproduce.
- Existing datasets of quantum flaky tests are small, and discovery methods rely on keywords and manual analysis, limiting recall and scalability.

## Approach
- Starting with an existing dataset of quantum flaky tests as seeds, the authors encode GitHub issue/PR text into vectors and use **embedding + cosine similarity** to retrieve new candidate reports that are semantically similar to known flaky cases.
- High-similarity candidates are then manually cross-validated over two iterations, expanding the set of flaky tests and supplementing it with **root-cause categories, faulty code, and fix information**.
- They then evaluate multiple foundation models/large language models (OpenAI GPT, Meta LLaMA, Google Gemini, Anthropic Claude) on two tasks: **classifying whether a report is related to a flaky test**, and **identifying the root cause**.
- The core idea can be understood simply as: first use semantic similarity to “find reports that look like flaky ones,” then let the LLM read the issue description and code context to decide “whether it is flaky” and “why it is flaky.”

## Results
- The pipeline discovered **25 previously unknown flaky tests**, increasing the original dataset size by **54%**; the dataset expanded from **46** to **71** flaky tests.
- The final dataset covers **12 open-source quantum software repositories** and **8,628** closed issues/PRs; the observed proportion of flaky reports is about **0.82% (71/8,628)**.
- In the root-cause statistics, the most common cause is **Randomness**, accounting for **19.2% (14/73 labels)**; the most common fix pattern is **Fix Seed**, accounting for **16.4% (12/73)**.
- The best-performing model is **Google Gemini 2.5 Flash**: **F1-score = 0.9420** for flakiness detection and **F1-score = 0.9643** for root-cause identification.
- The paper claims that these results show LLMs can already provide **practical support** for triaging flaky reports and understanding root causes in quantum software, while also providing a reusable expanded dataset and automated pipeline.

## Link
- [http://arxiv.org/abs/2603.09029v1](http://arxiv.org/abs/2603.09029v1)
