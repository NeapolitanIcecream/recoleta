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
---

# SEALing the Gap: A Reference Framework for LLM Inference Carbon Estimation via Multi-Benchmark Driven Embodiment

## Summary
本文提出一个面向LLM推理碳估算的“参考框架”，并给出早期实现SEAL，用多基准数据驱动的方式做细粒度、非侵入式的每条提示估算。核心贡献不在于部署级监控，而在于把推理碳估算重构为一个可标准化、可比较的基准学习问题。

## Problem
- 论文要解决的是：如何**准确、细粒度、非侵入式**地估算LLM在**推理阶段**的每条prompt碳排放/能耗；这很重要，因为LLM大规模使用下，**推理排放会很快超过训练排放**。
- 现有方法通常存在问题：过于粗粒度、只覆盖decode不覆盖prefill、依赖硬件遥测或部署环境访问、只适用于开源模型、或基于不全面的ground truth，因此难以用于真实生产场景和闭源API模型。
- 如果没有可靠的prompt级估算，开发者和组织就无法在性能、成本、延迟之外，把“可持续性”纳入RAG上下文长度、模型选择、推理配置等决策。

## Approach
- 作者先提出一个LLM推理碳估算的参考框架，给出7条指导原则：非侵入式、使用易获得属性、兼容开源与闭源模型、覆盖prefill+decode全生命周期、支持prompt级估算、基于标准且全面的ground truth、并要求高准确性。
- SEAL是这一框架的早期实现：它不直接监控GPU功耗，而是把**prompt属性和运行时可观测特征**输入到机器学习回归器中，预测推理能耗，再结合地区碳强度换算碳排放。
- 它通过合并两个公开基准构造训练集：LLM-Perf Leaderboard（3173条）和 Open LLM Leaderboard（2045条），按模型名和精度对齐后得到**3042条**样本，联合利用能耗/性能与质量信息。
- 训练时选用7个特征，包括输入/输出token数、模型大小、每输入/输出token延迟、GPU假设，以及BBH、MMLU-Pro等质量特征；共测试**13种回归算法**，并分别为**prefill**和**decode**训练模型。
- 为解决模型规模外推问题，作者分别训练**插值**模型（0–111B范围内）和**外推**模型（超出111B），最佳方法分别是XGBoost Regressor和Ridge Regressor。

## Results
- 10折交叉验证显示，**Decode / 插值**场景下，XGBoost达到 **MAPE 6.98% ± 0.56%**，**R² = 0.999**。
- **Prefill / 插值**场景下，XGBoost达到 **MAPE 5.36% ± 0.46%**，**R² = 0.995**。
- **Decode / 外推**场景下，Ridge达到 **MAPE 31.58% ± 2.78%**，**R² = 0.986**；**Prefill / 外推**场景下为 **MAPE 24.85% ± 1.77%**，**R² = 0.994**。
- 外部验证基于公开实测数据、prompt为**38个输入token + 64个输出token**：对 **LLaMA-2-7B**，实测 **349.96 J**，SEAL估计 **425.60 J**，误差 **19.51%**。
- 对 **LLaMA-2-13B**，实测 **602.27 J**，SEAL估计 **707.20 J**，误差 **16.02%**；两模型外部验证的平均误差为 **17.76%**。
- 论文声称的主要突破是：在无需底层遥测、可面向开源和闭源模型的前提下，实现了**prompt级、phase-aware（prefill+decode）**的早期高精度估算，并提出了一个可供后续工具对齐的标准化参考框架。

## Link
- [http://arxiv.org/abs/2603.02949v1](http://arxiv.org/abs/2603.02949v1)
