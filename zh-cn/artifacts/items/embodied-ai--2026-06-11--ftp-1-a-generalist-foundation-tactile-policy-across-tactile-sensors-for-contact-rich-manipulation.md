---
source: arxiv
url: https://arxiv.org/abs/2606.13102v1
published_at: '2026-06-11T09:30:09'
authors:
- Chengbo Yuan
- Zicheng Zhang
- Mingjie Zhou
- Wendi Chen
- Yi Wang
- Zhuoyang Liu
- Dantong Niu
- Shuo Wang
- Hui Zhang
- Wenkang Zhang
- Yingdong Hu
- Yuanqing Gong
- Wanli Xing
- Chuan Wen
- Cewu Lu
- Kaifeng Zhang
- Yang Gao
topics:
- tactile-manipulation
- generalist-robot-policy
- sensor-transfer
- contact-rich-control
- robot-pretraining
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# FTP-1: A Generalist Foundation Tactile Policy Across Tactile Sensors for Contact-Rich Manipulation

## Summary
## 摘要
FTP-1 是一个通用触觉策略，用于接触丰富的机器人操作，能够在多种触觉传感器类型和机器人形态上训练。它之所以重要，是因为现有触觉策略通常绑定在单一传感器配置上，这限制了迁移和复用。

## 问题
- 触觉数据在不同传感器之间的模态、分辨率和形状差异很大，所以在一套配置上训练的策略往往在另一套配置上失效。
- 先前的触觉策略和触觉 VLA 方法仍然绑定固定形态，而视觉-语言-动作模型常常忽略触觉。
- 这篇论文要回答的是：一个预训练触觉策略能否在异构硬件上学习可复用的触觉技能，并迁移到未见过的触觉传感器。

## 方法
- 它构建了形态感知触觉令牌空间（Morphology-Aware Tactile Token Space, MTTS），把不同的触觉输入映射到基于 24 个功能区域的共享令牌集合。
- 它为图像、数组和状态类触觉输入使用各自的编码器，然后把它们投影到同一个潜在空间。
- 它加入了一个共享触觉 Transformer 专家，在与一个 \u0003c0_0.5 风格的视觉-语言-动作策略融合之前对触觉令牌建模。
- 它在 FTP-1-Dataset 上预训练，这个数据集来自 26 个来源，约 3,000 小时数据，覆盖 21 个触觉传感器，包括人类和机器人示教。
- 在微调阶段，它在已见和未见传感器上复用预训练的触觉组件。

## 结果
- 在 UniVTAC 仿真基准上，FTP-1 的平均成功率是 66.66%，如果去掉两个更容易的 lift 任务，则是 59.5%。
- 在 UniVTAC 上，次优方法的整体成绩是 49.16%，去掉 lift 后是 42%，所以 FTP-1 在这两个指标上都高出约 17.5 个百分点。
- 在使用已见传感器的真实机器人任务上，FTP-1 在 Sharpa North 和 Sharpa&Dexmate 上的平均成功率是 62.5%。
- 在未见过的传感器配置上，FTP-1 的平均成功率是 46.6%，而 FTP-\u0003c0_0.5 是 15.0%，提升了 31.6 个百分点。
- 论文还报告，FTP-1 在未见过的 FlexivXense 上比一个没有触觉预训练的对照方法高 37.5%，并用这一结果说明触觉分支学到了可迁移的知识。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13102v1](https://arxiv.org/abs/2606.13102v1)
