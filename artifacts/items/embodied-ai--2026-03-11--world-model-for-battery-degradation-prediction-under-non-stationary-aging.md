---
source: arxiv
url: http://arxiv.org/abs/2603.10527v1
published_at: '2026-03-11T08:30:15'
authors:
- Kai Chin Lim
- Khay Wai See
topics:
- battery-degradation
- world-model
- state-of-health
- time-series-forecasting
- physics-informed-learning
relevance_score: 0.18
run_id: materialize-outputs
---

# World Model for Battery Degradation Prediction Under Non-Stationary Aging

## Summary
本文将电池健康状态（SOH）长期预测表述为“世界模型”问题：先把每个循环的原始电压/电流/温度序列压缩成潜在状态，再通过学习到的动力学逐步向前滚动预测未来 80 个循环。核心结论是：这种迭代 rollout 明显优于直接回归，且物理约束主要帮助退化拐点附近的预测。

## Problem
- 目标是预测锂离子电池在未来多个循环中的 SOH 轨迹，而不只是当前时刻的单点估计。
- 现有数据驱动方法虽可直接回归整段轨迹，但缺少“把退化过程一步步往前推进”的机制，容易学成平均斜率，难以刻画非平稳老化。
- 这很重要，因为电池寿命管理、维护决策和安全评估都依赖对未来退化路径而非单点数值的可靠预报。

## Approach
- 将每个循环的原始 **V/I/T** 时间序列输入共享的 1D CNN，提取单循环嵌入；再用 PatchTST 在 30 个历史循环窗口上编码出一个潜在退化状态 `z(k)`。
- 用带残差的 MLP 动力学转移模块，将当前潜在状态和充电电流条件一起映射到下一循环潜在状态；重复迭代后 rollout 出未来 80 步潜在轨迹。
- 用同一个解码头把当前潜在状态和未来 rollout 状态都映射成 SOH，从而同时输出当前 SOH 和未来 SOH 序列。
- 加入物理约束损失作为软正则，包括 SOH 单调不增约束、内阻与 SOH 的一致性约束，以及电压一致性约束，以测试物理先验是否能改进学习到的动力学。
- 通过三种配置做消融：带物理约束的 world model（PIWM）、不带物理约束的 world model（WM）、以及去掉 rollout 改为直接回归的 CNN-PatchTST；另做 LSTM 和 EWC 持续学习控制实验。

## Results
- 在 Severson LFP 数据集的 **138 个电芯**上，world model 相比同编码器的直接回归在总体精度更好：**MAE 从 0.0078 降到 0.0063**，相对改善约 **24%**（CNN-PatchTST vs PIWM/WM）。
- 未来轨迹预测的关键结果：**h=5** 时，PIWM 的 MAE 为 **0.0067**，WM 为 **0.0065**，而直接回归 CNN-PatchTST 为 **0.0136**；即 rollout 在短期预测上将误差约 **减半**。
- rollout 模型的误差会随预测步长增加，符合真实迭代预测特征：PIWM 从 **h5=0.0067** 增至 **h50=0.0109**，WM 从 **0.0065** 增至 **0.0096**；而直接回归几乎恒定在 **0.0133–0.0136**，说明它更像在输出平均退化斜率。
- 物理约束**没有提升总体 MAE**：PIWM 与 WM 的整体 **MAE 都是 0.0063**；但在退化拐点阶段（Stage 2, SOH 0.95–0.90）有帮助，**Stage 2 MAE 从 0.0098 降到 0.0080**。
- 物理约束在更晚期退化阶段反而略差：Stage 3 中，WM 的 **MAE=0.0135**，优于 PIWM 的 **0.0185**；整体看它更像局部正则器，而非全局精度提升手段。
- 持续学习控制实验中，作者称 **EWC 的准确率比联合训练差 3.3 倍**；文中还指出若在收敛后计算 Fisher 信息，EWC 会几乎失效，需要在中期训练时计算 Fisher 才能激活该机制。论文摘录未给出完整测试表，但给出了 **test MAE=0.021** 的 EWC 结果示例。

## Link
- [http://arxiv.org/abs/2603.10527v1](http://arxiv.org/abs/2603.10527v1)
