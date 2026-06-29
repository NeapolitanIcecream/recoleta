---
source: arxiv
url: http://arxiv.org/abs/2604.02965v1
published_at: '2026-04-03T10:55:51'
authors:
- Zihua Wang
- Zhitao Lin
- Ruibo Li
- Yu Zhang
- Xu Yang
- Siya Mi
- Xiu-Shen Wei
topics:
- vision-language-action
- robot-control
- action-chunking
- closed-loop-verification
- libero
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA

## Summary
## 总结
SV-VLA 通过用大模型规划动作块、再用小型验证器在线检查，降低了 VLA 控制成本。目标是在保留开放环分块带来的大部分速度的同时，补回一部分闭环控制的适应性。

## 问题
- 用于操作任务的 VLA 模型性能强，但每个控制步都运行一次，开销很高。
- 动作分块可以一次预测多个未来动作，从而降低推理成本，但后续动作依赖过时观测；环境变化时，这些动作容易偏离。
- 语言模型里的 speculative decoding 不能直接迁移到机器人控制，因为未来动作是否有效取决于未来观测，而这些观测只有在真实执行后才会出现。

## 方法
- SV-VLA 把重型 VLA 当作低频宏规划器。在规划边界，它输出长度为 K 的动作块，以及来自内部 transformer 层的规划上下文特征。
- 轻量验证器在每个控制步基于最新观测运行，用 ViT-Tiny 这类小型视觉主干编码图像，再把该特征与保存的规划上下文融合，预测参考动作。
- 系统用归一化 L1 距离比较规划动作和验证器的参考动作。如果距离低于阈值 \(\tau\)，就执行规划动作。
- 如果距离超过 \(\tau\)，系统丢弃当前动作块的剩余部分，并再次调用重型 VLA，从当前状态重新规划。
- 训练验证器时，重型 VLA 保持冻结；只有验证器用与真实动作之间的 L1 回归损失训练，这让方法可以直接配合预训练 VLA 使用。

## 结果
- 论文在 LIBERO 基准上做了实验，并说明 SV-VLA 在三个子任务上的平均成功率比开放环基线提高了 11.4 个百分点，从 79.5% 提升到 90.90%。
- 摘要没有给出这三个子任务的名称、各任务分数、延迟数据、主结果使用的分块大小，也没有给出与逐步闭环 VLA 的对比。
- 该方法声称可以保留分块控制的效率特征：在最好情况下，每步成本接近 \(C_{VLA}/K + C_{verify}\)；在最坏情况下，如果每一步都触发重新规划，每步成本接近 \(C_{VLA}\)。
- 文中给了一个具体分块例子，指出像 \(K=64\) 这样的长分块会让标准开放环执行更容易受漂移影响。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02965v1](http://arxiv.org/abs/2604.02965v1)
