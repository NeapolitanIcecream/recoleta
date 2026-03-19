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
language_code: zh-CN
---

# SEALing the Gap: A Reference Framework for LLM Inference Carbon Estimation via Multi-Benchmark Driven Embodiment

## Summary
本文提出了一个面向大语言模型推理碳估算的参考框架，并给出其早期实现 SEAL。核心思想是把逐提示词能耗/碳估算转化为一个由多基准驱动的监督学习问题，以支持更标准化、细粒度且非侵入式的可持续性评估。

## Problem
- 论文要解决的是：**如何对 LLM 推理阶段进行逐提示词、细粒度、准确且非侵入式的碳/能耗估算**，因为在高频使用下，推理排放很快会超过训练排放。
- 这很重要，因为开发者、组织和政策制定者若看不到每次 prompt 的环境代价，就无法在性能、成本、延迟与可持续性之间做出合理权衡，环境负债会被隐藏。
- 现有方法的问题包括：过于粗糙、依赖硬件遥测或部署环境访问、只覆盖 decode 阶段、难以支持闭源模型、缺乏标准化 ground truth，导致结果不可靠且不可比。

## Approach
- 作者先提出一个**参考框架**，要求未来工具满足七类原则：非侵入式、依赖易获取属性、同时支持开源/闭源模型、覆盖 prefill+decode 全推理生命周期、提供 prompt 级估算、基于标准且全面的 ground truth，并具备高准确性。
- 在此基础上实现 **SEAL**：不用直接监控 GPU 功耗，而是把能耗估算当作一个机器学习回归任务，只利用较容易获得或可近似的特征来预测每次 prompt 的能耗，再结合地区碳强度换算成碳排放。
- SEAL 的关键机制是**多基准融合**：将 LLM-Perf Leaderboard（3173 条，含逐 prompt/逐 token、分阶段性能与能耗）与 Open LLM Leaderboard（2045 条，含质量基准）按模型名和精度合并，得到 **3042 条观测**的训练集。
- 作者从清洗和分析后选取 **7 个特征**建模，包括输入/输出 token 数、模型规模、每输入/输出 token 延迟、假设的底层 GPU，以及质量特征（如 BBH、MMLU-Pro）；并分别为 **Prefill** 和 **Decode** 训练模型。
- 共测试 **13 种回归算法**，并区分两类泛化场景：**插值**（0–111B 参数范围内）与**外推**（超出 111B），因为适合插值的模型通常不擅长外推。

## Results
- 在 **10 折交叉验证**中，**Decode-插值**最优模型为 **XGBoost Regressor**，达到 **MAPE 6.98% ± 0.56%**，**R² = 0.999**。
- 在 **10 折交叉验证**中，**Prefill-插值**最优模型也为 **XGBoost Regressor**，达到 **MAPE 5.36% ± 0.46%**，**R² = 0.995**。
- 在更难的**外推**场景中，最优模型变为 **Ridge Regressor**：**Decode-外推 MAPE 31.58% ± 2.78%，R² = 0.986**；**Prefill-外推 MAPE 24.85% ± 1.77%，R² = 0.994**。
- 外部验证使用已发表实测数据、同一 prompt（**38 输入 token，64 输出 token**）测试两个模型：**LLaMA-2-7B** 实测 **349.96 J**，SEAL 估计 **425.60 J**，误差 **19.51%**；**LLaMA-2-13B** 实测 **602.27 J**，估计 **707.20 J**，误差 **16.02%**。
- 两个外部验证样本的**平均误差为 17.76%**。论文将其定位为“早期但有前景”的结果，而不是最终的最先进方案。
- 论文的主要突破性主张不只是单一精度数字，而是首次系统提出一个**适用于开源与闭源 LLM、覆盖 prefill 与 decode、基于多基准和 prompt 级估算的参考框架与实现雏形**。

## Link
- [http://arxiv.org/abs/2603.02949v1](http://arxiv.org/abs/2603.02949v1)
