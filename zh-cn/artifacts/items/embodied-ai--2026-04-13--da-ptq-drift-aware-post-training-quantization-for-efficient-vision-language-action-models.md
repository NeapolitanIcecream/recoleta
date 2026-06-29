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
## 总结
DA-PTQ 是一种用于视觉-语言-动作模型的训练后量化方法，针对机器人控制中的一种常见失效模式：小的量化误差会随着时间推移累积成轨迹漂移。它加入接口级补偿和面向漂移的比特分配，让低比特 VLA 模型在资源受限机器人上更接近全精度模型的行为。

## 问题
- 视觉-语言-动作模型体量大，在机器人板载硬件上运行成本高，所以量化有助于降低内存和计算开销。
- 标准训练后量化对 VLA 的效果不好，因为动作误差会在控制步之间累积；视觉-语言到动作接口上的微小扰动会放大为运动学漂移。
- 现有的 VLA 量化方法主要优化静态重建或单步敏感度，没能处理序列控制中的长时程误差传播。

## 方法
- DA-PTQ 把量化当作序列控制问题，而不是层重建问题。目标是减少量化噪声造成的轨迹漂移。
- 第一部分 Cross-Space Representation Compensation 会度量量化如何改变视觉-语言-动作接口上的条件激活，然后用逐通道仿射校正和低秩跨通道变换，把量化后的激活对齐到全精度统计。
- 这些校正参数会在校准后折叠进量化权重，所以方法声称不会增加额外推理开销。
- 第二部分 Motion-Driven Mixed-Precision Allocation 会构建一个基于雅可比矩阵的代理，估计每个动作维度中的误差如何传播到末端执行器漂移，然后用漂移加权损失和层敏感度分数，把最容易受漂移影响的层保留为 BF16，其他层量化到 W4 等低精度。
- 整个流程不需要训练，使用少量校准数据，通过前向传递和轻量梯度累积完成。

## 结果
- 这段摘要没有给出定量表格或具体基准数字。
- 论文声称，和传统 PTQ 策略相比，DA-PTQ 在序列机器人控制中能“显著降低运动学漂移”。
- 它还声称，在低比特设置下，模型性能接近全精度模型，其中混合精度方案把敏感层保留为 BF16，其余部分用 W4。
- 论文声称，这种方法在把补偿折叠进模型权重后，不会带来额外运行时成本，因此可以让基于扩散的 VLA 模型在资源受限的机器人平台上实际部署。
- 该方法使用 7 维动作表示，并把漂移定义为在控制时域内累积的、经过雅可比加权的动作误差；但摘要没有给出与 AWQ、GPTQ、QuantVLA、QVLA 或 SQAP-VLA 等基线相比的成功率、延迟、内存或准确率数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11572v1](http://arxiv.org/abs/2604.11572v1)
