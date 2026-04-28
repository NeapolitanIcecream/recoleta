---
source: arxiv
url: http://arxiv.org/abs/2604.11572v1
published_at: '2026-04-13T14:51:43'
authors:
- Siyuan Xu
- Tianshi Wang
- Fengling Li
- Lei Zhu
- Heng Tao Shen
topics:
- vision-language-action
- post-training-quantization
- robot-efficiency
- mixed-precision
- sequential-control
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# DA-PTQ: Drift-Aware Post-Training Quantization for Efficient Vision-Language-Action Models

## Summary
## 摘要
DA-PTQ 是一种用于视觉-语言-动作模型的训练后量化方法，针对机器人控制中的一个常见失效模式：细小的量化误差会随时间累积为轨迹漂移。它加入了接口级补偿和漂移感知的比特分配，使低比特 VLA 模型在资源受限的机器人上更接近全精度模型的行为。

## 问题
- 视觉-语言-动作模型体量大，在机器人板载硬件上运行的成本高，因此量化有助于降低内存占用和计算量。
- 标准训练后量化在 VLA 上效果较差，因为动作误差会在控制步骤间累积；视觉-语言到动作接口处的微小扰动可能扩大为运动学漂移。
- 现有 VLA 量化方法主要优化静态重建或单步敏感性，这会忽略序列控制中的长时程误差传播。

## 方法
- DA-PTQ 将量化视为一个序列控制问题，而不是层重建问题。目标是减少量化噪声导致的轨迹漂移。
- 其第一部分 Cross-Space Representation Compensation 会度量量化如何改变视觉-语言到动作接口处的条件激活，然后使用逐通道仿射校正和低秩跨通道变换，使量化后的激活与全精度统计量对齐。
- 这些校正参数会在校准后折叠进量化权重，因此该方法声称不会带来额外推理开销。
- 其第二部分 Motion-Driven Mixed-Precision Allocation 为每个动作维度中的误差如何传播为末端执行器漂移建立基于雅可比矩阵的代理，然后使用漂移加权损失和层敏感性分数，将对漂移最敏感的层保留为 BF16，同时把其他层量化为 W4 等低精度。
- 整个流程不需要训练，只使用一个小型校准数据集，配合前向传播和轻量级梯度累积。

## 结果
- 摘要中没有给出定量表格或确切的基准测试数字。
- 论文声称，与传统 PTQ 策略相比，DA-PTQ 在序列机器人控制中“显著减少了运动学漂移”。
- 它声称在低比特设置下取得了与全精度模型相当的性能，其中混合精度方案对敏感层使用 BF16，其余层使用 W4。
- 它声称，该方法在将补偿折叠进模型权重后，不增加额外运行时成本，就能让基于扩散的 VLA 模型在资源受限的机器人平台上实现实际部署。
- 该方法使用 7 维动作表述，并将漂移定义为控制时域内按雅可比矩阵加权后累积的动作误差，但摘要中没有给出相对于 AWQ、GPTQ、QuantVLA、QVLA 或 SQAP-VLA 等基线的成功率、延迟、内存或准确率数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11572v1](http://arxiv.org/abs/2604.11572v1)
