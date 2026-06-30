---
source: arxiv
url: https://arxiv.org/abs/2606.29948v1
published_at: '2026-06-29T08:24:38'
authors:
- Jianxin Bi
- Qiang Wang
- Jayaram Reddy
- Kelvin Lin
- Soibkhon Khajikhanov
- Ruihan Gao
- Harold Soh
topics:
- tactile-representation-learning
- heterogeneous-tactile-sensors
- self-supervised-pretraining
- robot-manipulation
- contact-rich-control
- robot-data-scaling
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Heterogeneous Tactile Transformer

## Summary
## 摘要
HTT 使用成对的自监督数据，在光学和阵列式触觉传感器上训练一个统一的触觉骨干网络。它面向接触密集型感知和操作任务；在这类任务中，按传感器单独训练的触觉模型难以跨硬件迁移。

## 问题
- 触觉传感器输出不同的数据类型：GelSight Mini 和 9DTact 输出图像，Xela 和 TAC-02 输出时序 taxel 信号，因此在一种传感器上训练的模型不能直接读取另一种传感器的数据。
- 这限制了跨硬件扩展触觉数据的能力，也会影响需要力、滑移和空间接触线索的机器人策略。
- 现有触觉预训练主要面向光学触觉传感器，可能遗漏阵列式传感器提供的力敏感线索。

## 方法
- HPT 数据集包含来自 GelSight Mini、9DTact、Xela 和 TAC-02 的 160 万个同步成对触觉帧，使用 UMI 装置采集，覆盖按压、扭转和滑动交互。
- HTT 使用传感器专用编码器：光学触觉图像使用 ViT 风格的空间 patch，阵列式触觉时间序列使用时间 patch。
- 共享 transformer 主干将所有传感器嵌入映射到同一个潜在空间，传感器专用解码器则重建被遮蔽的输入 patch。
- 跨传感器预测器学习根据成对传感器和可见目标 token 来预测某个传感器被遮蔽的嵌入，并使用 stop-gradient 目标，且将对齐权重逐步升至 0.1。
- 预训练后，解码器和预测器会被移除；下游任务使用对应的传感器编码器和共享主干。

## 结果
- 在 20 类物体分类上，HTT 的整体 top-1 准确率达到 66.20%，Scratch 为 47.54%，仅 MAE 预训练为 65.38%。在光学传感器上，HTT 在 9DTact 上达到 94.84%，在 GSMini 上达到 91.35%；SITR 分别为 81.34% 和 74.31%。
- 在力估计上，HTT 报告的整体 3D MAE 为 0.636 N，低于 Scratch 的 1.111 N 和仅 MAE 的 0.664 N。
- 在滑移检测上，HTT 报告的整体 macro-F1 为 56.35%，高于 Scratch 的 31.14% 和仅 MAE 的 51.62%。列出的最大对齐增益出现在 TAC-02：HTT 的 macro-F1 为 45.45%，仅 MAE 为 33.45%。
- 在使用未见过的 Sharpa 指尖传感器进行真实世界无相机操作时，HTT 在 toy screw 上达到 95% 成功率，在 grasp tofu 上达到 55%。qpos-only 在两个任务上均为 5%，wrench 输入在 screw 上为 50%，在 tofu 上为 35%。
- 在 ManiFeel 仿真中，HTT(FF) 在 Peg Insertion 上达到 0.48 成功率，高于 tacRGB 的 0.21、T3 的 0.23 和 SITR 的 0.35。在 Bulb Installation 上，HTT(RGB) 达到 0.77，与 SITR 的 0.77 持平，高于 tacRGB 的 0.72 和 T3 的 0.73。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.29948v1](https://arxiv.org/abs/2606.29948v1)
