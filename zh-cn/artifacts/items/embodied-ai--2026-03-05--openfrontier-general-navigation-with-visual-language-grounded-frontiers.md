---
source: arxiv
url: http://arxiv.org/abs/2603.05377v1
published_at: '2026-03-05T17:02:22'
authors:
- Esteban Padilla
- Boyang Sun
- Marc Pollefeys
- Hermann Blum
topics:
- open-world-navigation
- vision-language-models
- frontier-based-exploration
- zero-shot-navigation
- object-goal-navigation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# OpenFrontier: General Navigation with Visual-Language Grounded Frontiers

## Summary
OpenFrontier提出一种**免训练**的开放世界导航框架，把“前沿点（frontiers）”作为视觉-语言语义与可执行导航之间的桥梁。它不依赖稠密3D语义地图、策略训练或微调，却在多项ObjNav基准上取得很强的零样本表现，并展示了真实机器人部署能力。

## Problem
- 机器人在开放环境中导航时，需要同时理解**语言目标的语义**和**实际可到达的几何位置**；传统方法常依赖稠密3D建图和手工目标指标，泛化差、系统重。
- 端到端VLN/VLA方法虽然能用自然语言控制，但通常需要**大量交互训练、数据收集或任务微调**，并且难把高层语义稳定地落到度量空间中的导航决策上。
- 论文要解决的是：**如何在不训练导航策略、不构建稠密语义地图的前提下，实现开放词汇、零样本、可落地的语言条件导航**；这很重要，因为它降低部署成本并提升跨环境泛化能力。

## Approach
- 将导航重写为**稀疏子目标识别与到达**问题：先从当前RGB图像中检测视觉前沿点，而不是先做完整3D重建。
- 用VLM对图像中的每个前沿点做**set-of-marks**打分：把前沿位置标在图像上，结合语言目标，让模型输出该前沿“通向目标”的概率 \(p_i\)。
- 将语义概率与探索收益结合，得到前沿效用：\(g_i = p_i \cdot \hat{g}_i\)，其中 \(\hat{g}_i\) 是前沿本身的信息增益；再结合距离得到全局效用 \(u_i = g_i / \|p_r - p_i\|\)，优先走“既相关又近”的前沿。
- 前沿在图像空间被评估、在3D空间被回投和管理：系统维护全局前沿集合，持续更新、合并、清理，并交给低层PointNav/规划器执行。
- 当开放词汇分割检测到疑似目标时，系统会插入一个高优先级“视点前沿”，移动到更好的观察位姿，再用同一VLM做目标确认与终止判断。

## Results
- 在 **HM3D ObjNav Val** 上，OpenFrontier达到 **77.3% SR / 35.6% SPL**；对比零样本基线：BeliefMapNav为 **61.4 / 30.6**，InstructNav为 **58.0 / 20.9**，VLFM为 **52.5 / 30.4**，OpenFMNav为 **52.5 / 24.1**。其SR比BeliefMapNav高 **15.9** 个点，比InstructNav高 **19.3** 个点。
- 在 **MP3D ObjNav Val** 上，OpenFrontier为 **40.7% SR / 17.8% SPL**；略低于UniGoal的 **41.0 / 16.4** 在SR上低 **0.3** 点，但SPL更高 **1.4** 点；也高于BeliefMapNav的 **37.3 / 17.6** 和VLFM的 **36.4 / 17.5**。
- 在 **OVON Val Unseen** 开放词汇基准上，OpenFrontier达到 **39.0% SR / 20.1% SPL**；优于VLFM的 **35.2 / 19.6** 和DAgRL+OD的 **37.1 / 19.9**，与非零样本Uni-NaVid的 **39.5 / 19.8** 接近：SR低 **0.5** 点，但SPL高 **0.3** 点。
- 论文强调这些结果是在**零样本、无稠密语义地图、无策略训练/微调**条件下取得的，而一些对比方法需要稠密语义地图或并非零样本。
- 实验配置上，系统使用 **Gemini-2.5-flash** 做VLM推理，前沿检测每 **6步** 运行一次，且整套实验可在 **单张RTX 4090 24GB** 上完成，支持其“轻量级系统设计”的主张。
- 真实世界方面，论文展示了移动机器人在大规模室内环境中寻找**fire extinguisher**的成功案例，但摘录中**未提供真实机定量指标**；最强具体结论是其在实机上表现出有效、鲁棒的开放世界导航能力。

## Link
- [http://arxiv.org/abs/2603.05377v1](http://arxiv.org/abs/2603.05377v1)
