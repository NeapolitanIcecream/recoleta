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
- benchmark-driven
- energy-modeling
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# SEALing the Gap: A Reference Framework for LLM Inference Carbon Estimation via Multi-Benchmark Driven Embodiment

## Summary
This paper proposes a “reference framework” for LLM inference carbon estimation and presents an early implementation, SEAL, which uses a multi-benchmark-driven approach to perform fine-grained, non-intrusive per-prompt estimation. The core contribution is not deployment-level monitoring, but rather reframing inference carbon estimation as a benchmark learning problem that can be standardized and compared.

## Problem
- The paper aims to solve how to **accurately, finely, and non-intrusively** estimate the carbon emissions/energy consumption of each prompt during the **inference stage** of LLMs; this matters because at large scale, **inference emissions can quickly exceed training emissions**.
- Existing methods usually have problems: they are too coarse-grained, cover only decode but not prefill, rely on hardware telemetry or access to deployment environments, apply only to open-source models, or are based on incomplete ground truth, making them difficult to use in real production settings and for closed-source API models.
- Without reliable prompt-level estimation, developers and organizations cannot incorporate “sustainability” into decisions such as RAG context length, model selection, and inference configuration, alongside performance, cost, and latency.

## Approach
- The authors first propose a reference framework for LLM inference carbon estimation, with 7 guiding principles: non-intrusive, using readily available attributes, compatible with both open-source and closed-source models, covering the full prefill+decode lifecycle, supporting prompt-level estimation, based on standardized and comprehensive ground truth, and requiring high accuracy.
- SEAL is an early implementation of this framework: instead of directly monitoring GPU power consumption, it feeds **prompt attributes and runtime-observable features** into machine learning regressors to predict inference energy consumption, and then converts that into carbon emissions using regional carbon intensity.
- It constructs the training set by combining two public benchmarks: LLM-Perf Leaderboard (3,173 entries) and Open LLM Leaderboard (2,045 entries). After aligning by model name and precision, it obtains **3,042** samples, jointly leveraging energy/performance and quality information.
- During training, 7 features are used, including input/output token counts, model size, per-input/output-token latency, GPU assumptions, and quality features such as BBH and MMLU-Pro; a total of **13 regression algorithms** are tested, and models are trained separately for **prefill** and **decode**.
- To address extrapolation across model scales, the authors separately train **interpolation** models (within the 0–111B range) and **extrapolation** models (beyond 111B). The best methods are XGBoost Regressor and Ridge Regressor, respectively.

## Results
- 10-fold cross-validation shows that in the **Decode / interpolation** setting, XGBoost achieves **MAPE 6.98% ± 0.56%**, **R² = 0.999**.
- In the **Prefill / interpolation** setting, XGBoost achieves **MAPE 5.36% ± 0.46%**, **R² = 0.995**.
- In the **Decode / extrapolation** setting, Ridge achieves **MAPE 31.58% ± 2.78%**, **R² = 0.986**; in the **Prefill / extrapolation** setting, it achieves **MAPE 24.85% ± 1.77%**, **R² = 0.994**.
- External validation is based on public measured data with prompts of **38 input tokens + 64 output tokens**: for **LLaMA-2-7B**, the measured value is **349.96 J**, SEAL estimates **425.60 J**, with an error of **19.51%**.
- For **LLaMA-2-13B**, the measured value is **602.27 J**, SEAL estimates **707.20 J**, with an error of **16.02%**; the average error across the two models in external validation is **17.76%**.
- The paper’s claimed main breakthrough is achieving early high-accuracy **prompt-level, phase-aware (prefill+decode)** estimation without requiring low-level telemetry and while being applicable to both open-source and closed-source models, while also proposing a standardized reference framework that future tools can align to.

## Link
- [http://arxiv.org/abs/2603.02949v1](http://arxiv.org/abs/2603.02949v1)
