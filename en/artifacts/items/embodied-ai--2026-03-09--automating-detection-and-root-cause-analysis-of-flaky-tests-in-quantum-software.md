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
- llm-for-se
- repository-mining
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Automating Detection and Root-Cause Analysis of Flaky Tests in Quantum Software

## Summary
This paper proposes an automated pipeline for quantum software to discover flaky tests (tests that randomly pass or fail without code changes) and analyze their root causes. It combines repository mining, vector-similarity retrieval, and multiple large language models to expand the dataset and automate defect triage.

## Problem
- The paper addresses the problem of **automatic detection and root-cause analysis of flaky tests in quantum software**; this matters because quantum programs are inherently probabilistic, making test results more unstable, which can mask real defects and waste developers' debugging time.
- Compared with classical software, quantum flaky tests are also affected by factors such as **randomness, quantum noise, and the high cost of reproducing on real hardware**; for example, the paper mentions that the IBM quantum platform can cost up to **$96 per minute**, making repeated test reruns expensive.
- Existing quantum flaky test datasets mainly rely on **keyword search and manual analysis**, which have limited recall and scale slowly, making it difficult to support large-scale automated maintenance.

## Approach
- Starting from the quantum flaky test dataset previously compiled by the authors, the method embeds GitHub issue/PR text from **12 open-source quantum software repositories** and computes **cosine similarity** against known flaky cases, then manually reviews high-similarity candidates to identify new cases.
- Multiple embedding models were compared, and the final choice was **mixedbread-ai/mxbai-embed-large-v1** because it more clearly separates flaky from non-flaky cases.
- In the detection and diagnosis stage, the authors evaluate FM/LLMs from several vendors (**OpenAI GPT, Meta LLaMA, Google Gemini, Anthropic Claude**), asking the models to use issue/PR descriptions plus additional code context to determine: **whether it is a flaky test** and **what the root-cause category is**.
- The method can be understood simply as: **first use “semantic retrieval” to find reports that resemble flaky cases, then use an LLM to read the text and code, decide whether it is flaky, and provide the most likely reason.**

## Results
- The pipeline newly discovers **25** previously unknown quantum flaky tests, increasing the original dataset size by **54%**; the final total is **71 flaky tests** from **12 repositories** and **8,628 closed issue/PRs**.
- By repository, the observed proportion of flaky reports is about **0.82% (71/8,628)**; there is substantial variation across repositories, for example **qiskit: 29/4,533 = 0.55%** and **Microsoft Quantum: 4/111 = 3.60%**.
- Root-cause analysis shows that the most common cause is **Randomness**, accounting for **19.2% (14/73 labels)**; the most common fix pattern is **Fix Seed**, accounting for **16.4% (12/73)** of all fix patterns. In addition, multithreading accounts for **13.7%**, software environment **11.0%**, and floating-point issues **9.6%**.
- For automatic classification, the best model, **Google Gemini 2.5 Flash**, achieves **flakiness detection F1 = 0.9420**.
- For root-cause identification, the same best model reaches **root-cause identification F1 = 0.9643**.
- The paper’s central breakthrough claim is that **LLMs can now provide practical support for triaging flaky reports and locating root causes in quantum software**, while also producing an expanded reusable dataset and an automated pipeline.

## Link
- [http://arxiv.org/abs/2603.09029v1](http://arxiv.org/abs/2603.09029v1)
