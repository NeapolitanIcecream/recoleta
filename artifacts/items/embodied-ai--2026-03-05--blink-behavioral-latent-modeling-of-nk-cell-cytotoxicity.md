---
source: arxiv
url: http://arxiv.org/abs/2603.05110v1
published_at: '2026-03-05T12:29:57'
authors:
- Iman Nematollahi
- Jose Francisco Villena-Ossa
- Alina Moter
- Kiana Farhadyar
- Gabriel Kalweit
- Abhinav Valada
- Toni Cathomen
- Evelyn Ullrich
- Maria Kalweit
topics:
- world-model
- cell-dynamics
- time-series-modeling
- fluorescence-microscopy
- latent-state-space
relevance_score: 0.28
run_id: materialize-outputs
---

# BLINK: Behavioral Latent Modeling of NK Cell Cytotoxicity

## Summary
BLINK提出了一个用于NK细胞杀伤肿瘤过程的潜在动力学模型，把细胞毒性预测从“单帧判别”改为“轨迹级状态推断”。它将世界模型思想引入时序荧光显微成像，用于更准确地估计和预测累积凋亡结果。

## Problem
- 要解决的是：如何从**时间分辨率显微镜序列**中估计NK细胞对肿瘤细胞造成的**累积细胞毒性结果**，而不是只在单帧上检测死亡事件。
- 这很重要，因为NK细胞杀伤是一个**随时间积累、依赖接触历史和隐含细胞状态**的过程；单帧分类会忽略迁移、接触、激活到凋亡诱导的动态链条。
- 传统人工轨迹检查和终点/群体测量扩展性差，难以揭示单细胞层面的行为异质性和时间结构。

## Approach
- 核心方法是一个**轨迹级 recurrent state-space model (RSSM)**，灵感来自DreamerV2：把每一帧NK-肿瘤交互裁剪图像编码成潜在状态，并结合NK在相邻帧间的2D位移作为“action”来建模隐含交互动力学。
- 模型同时学习：**后验潜变量**（看当前图像时的状态）和**先验动态模型**（不看未来图像时对下一状态的预测），因此不仅能拟合过去，还能做潜在空间中的未来rollout预测。
- 在潜在状态上接一个两层MLP，不直接回归总细胞毒性，而是预测每帧**非负凋亡增量**；再把这些增量累加成累积细胞毒性，从结构上保证预测是**单调递增**的。
- 训练目标联合三部分：图像重建、潜变量KL正则、以及累积细胞毒性监督（Huber loss），实现端到端学习。
- 作者还用潜在表示做无监督聚类，分析是否能形成可解释的行为模式和阶段转移。

## Results
- 在测试集轨迹级累积细胞毒性预测上，**BLINK优于所有基线**：MAE **0.60±0.07**、RMSE **0.81±0.08**、Pearson相关 **0.77±0.05**、落在**±1 outcome**内的比例 **80.7%±5.2%**、30帧未来预测误差 F-MAE30 **0.05±0.01**。
- 相比最强确定性基线 **GRU-monotone**，BLINK从 **MAE 0.74±0.09 → 0.60±0.07**，**RMSE 1.04±0.11 → 0.81±0.08**，**相关系数 0.57±0.04 → 0.77±0.05**，**±1 outcome命中率 71.9%±3.3% → 80.7%±5.2%**，**F-MAE30 0.22±0.04 → 0.05±0.01**。
- 相比**无action版本** BLINK-no-action，加入NK位移动作后也有提升：MAE **0.80±0.06 → 0.60±0.07**，RMSE **1.14±0.09 → 0.81±0.08**，相关 **0.61±0.04 → 0.77±0.05**，±1 outcome **69.4%±7.3% → 80.7%±5.2%**，F-MAE30 **0.09±0.01 → 0.05±0.01**。
- 单帧自编码基线 **FrameAE** 明显较弱（MAE **0.95±0.11**，相关 **0.32±0.07**），支持作者关于“**轨迹级时间建模比帧级方法更关键**”的论点。
- 作者声称该模型还能学到可解释行为模式：无监督聚类得到4类窗口状态——**High Cytotoxic**（平均outcome **0.56**，速度 **5.60**，占 **12.9%**）、**Motile**（**0.26**, **5.67**, **19.2%**）、**Low Cytotoxic**（**0.13**, **1.55**, **43.0%**）、**Quiescent**（**0.09**, **1.44**, **24.9%**）；测试轨迹显示从高杀伤向低杀伤/静息状态的结构化转移。

## Link
- [http://arxiv.org/abs/2603.05110v1](http://arxiv.org/abs/2603.05110v1)
