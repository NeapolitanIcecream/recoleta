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
## 摘要
SV-VLA 通过让大模型规划动作块、再由小型验证器在线检查，降低了 VLA 控制成本。目标是在保留开放环动作分块大部分速度优势的同时，补回一部分闭环控制的适应性。

## 问题
- 用于操作任务的 VLA 模型性能强，但如果在每个控制步都运行，成本很高。
- 动作分块通过一次预测多个未来动作来降低推理成本，但后续动作依赖过时观测，环境变化时容易偏移。
- 语言建模中的推测解码不能直接迁移到机器人场景，因为未来动作是否有效取决于未来观测，而这些观测只有在真实执行后才会出现。

## 方法
- SV-VLA 将重型 VLA 用作低频宏规划器。在规划边界处，它输出一个长度为 K 的动作块，以及一个来自内部 transformer 层的规划上下文特征。
- 轻量验证器在每个控制步基于最新观测运行，用小型视觉骨干网络（如 ViT-Tiny）编码图像，将该特征与保存的规划上下文融合，并预测一个参考动作。
- 系统用归一化 L1 距离比较计划动作与验证器的参考动作。如果距离低于阈值 \(\tau\)，就执行计划动作。
- 如果距离超过 \(\tau\)，系统就丢弃该动作块剩余部分，并再次调用重型 VLA，从当前状态重新规划。
- 在验证器训练期间，重型 VLA 保持冻结；只训练验证器，并使用针对真实动作的 L1 回归损失。这让该方法可以兼容预训练 VLA。

## 结果
- 论文报告了在 LIBERO 基准上的实验，并称 SV-VLA 相比开放环基线，在三个子任务上的平均成功率提高了 11.4 个百分点，从 79.5% 提升到 90.90%。
- 这段摘录没有给出三个子任务的名称、各任务分数、延迟数据、主结果使用的 chunk size，也没有与逐步闭环 VLA 比较。
- 该方法声称保留了分块控制的效率特征：在最好情况下，单步成本接近 \(C_{VLA}/K + C_{verify}\)；如果每一步都触发重规划，最坏情况下成本接近 \(C_{VLA}\)。
- 文中给了一个具体的分块示例，指出像 \(K=64\) 这样的长动作块会增加标准开放环执行中的漂移风险。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02965v1](http://arxiv.org/abs/2604.02965v1)
