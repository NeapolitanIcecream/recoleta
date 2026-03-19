---
source: arxiv
url: http://arxiv.org/abs/2603.02949v1
published_at: '2026-03-03T12:57:27'
authors:
- Priyavanshi Pathania
- Rohit Mehra
- Vibhu Saujanya Sharma
- Vikrant Kaulgud
- Tiffani Nevels
- Sanjay Podder
- Adam P. Burden
topics:
- llm-inference
- carbon-estimation
- green-software
- benchmark-driven-modeling
- prompt-level-estimation
relevance_score: 0.69
run_id: materialize-outputs
language_code: en
---

# SEALing the Gap: A Reference Framework for LLM Inference Carbon Estimation via Multi-Benchmark Driven Embodiment

## Summary
This paper proposes a reference framework for carbon estimation in large language model inference and presents its early implementation, SEAL. The core idea is to transform per-prompt energy/carbon estimation into a supervised learning problem driven by multiple benchmarks, enabling more standardized, fine-grained, and non-intrusive sustainability assessment.

## Problem
- The paper aims to solve: **how to perform per-prompt, fine-grained, accurate, and non-intrusive carbon/energy estimation for the LLM inference stage**, because under high-frequency usage, inference emissions can quickly exceed training emissions.
- This matters because if developers, organizations, and policymakers cannot see the environmental cost of each prompt, they cannot make informed trade-offs among performance, cost, latency, and sustainability, and environmental debt remains hidden.
- Problems with existing methods include being too coarse-grained, relying on hardware telemetry or deployment-environment access, covering only the decode stage, being difficult to apply to closed-source models, and lacking standardized ground truth, which makes results unreliable and not comparable.

## Approach
- The authors first propose a **reference framework**, requiring future tools to satisfy seven categories of principles: non-intrusiveness, reliance on easily obtainable attributes, support for both open-source and closed-source models, coverage of the full inference lifecycle including prefill + decode, prompt-level estimation, use of standardized and comprehensive ground truth, and high accuracy.
- On this basis, they implement **SEAL**: instead of directly monitoring GPU power consumption, it treats energy estimation as a machine learning regression task, using only relatively accessible or approximable features to predict the energy consumption of each prompt, and then converts that into carbon emissions using regional carbon intensity.
- SEAL’s key mechanism is **multi-benchmark fusion**: it merges the LLM-Perf Leaderboard (3,173 entries, including per-prompt/per-token, stage-level performance and energy data) and the Open LLM Leaderboard (2,045 entries, including quality benchmarks) by model name and precision, producing a training set of **3,042 observations**.
- After cleaning and analysis, the authors select **7 features** for modeling, including input/output token counts, model size, latency per input/output token, the assumed underlying GPU, and quality features (such as BBH and MMLU-Pro); and they train separate models for **Prefill** and **Decode**.
- A total of **13 regression algorithms** are tested, and two generalization scenarios are distinguished: **interpolation** (within the 0–111B parameter range) and **extrapolation** (beyond 111B), because models that are good at interpolation are usually not good at extrapolation.

## Results
- In **10-fold cross-validation**, the best model for **Decode-interpolation** is **XGBoost Regressor**, achieving **MAPE 6.98% ± 0.56%** and **R² = 0.999**.
- In **10-fold cross-validation**, the best model for **Prefill-interpolation** is also **XGBoost Regressor**, achieving **MAPE 5.36% ± 0.46%** and **R² = 0.995**.
- In the more difficult **extrapolation** setting, the best model becomes **Ridge Regressor**: **Decode-extrapolation MAPE 31.58% ± 2.78%, R² = 0.986**; **Prefill-extrapolation MAPE 24.85% ± 1.77%, R² = 0.994**.
- External validation uses published measurement data and tests two models on the same prompt (**38 input tokens, 64 output tokens**): for **LLaMA-2-7B**, the measured value is **349.96 J**, SEAL estimates **425.60 J**, with **19.51%** error; for **LLaMA-2-13B**, the measured value is **602.27 J**, the estimate is **707.20 J**, with **16.02%** error.
- The **average error across the two external validation samples is 17.76%**. The paper positions this as an “early but promising” result rather than a final state-of-the-art solution.
- The paper’s main breakthrough claim is not just a single accuracy number, but the first systematic proposal of a **reference framework and prototype implementation applicable to both open-source and closed-source LLMs, covering prefill and decode, and based on multi-benchmark, prompt-level estimation**.

## Link
- [http://arxiv.org/abs/2603.02949v1](http://arxiv.org/abs/2603.02949v1)
