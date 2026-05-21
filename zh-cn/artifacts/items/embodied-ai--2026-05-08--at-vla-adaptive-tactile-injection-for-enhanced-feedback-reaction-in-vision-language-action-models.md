---
source: arxiv
url: https://arxiv.org/abs/2605.07308v2
published_at: '2026-05-08T06:17:08'
authors:
- Xiaoqi Li
- Muhe Cai
- Jiadong Xu
- Juan Zhu
- Hongwei Fan
- Yan Shen
- Guangrui Ren
- Hao Dong
topics:
- vision-language-action
- tactile-feedback
- contact-rich-manipulation
- robot-foundation-model
- closed-loop-control
- dexterous-manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models

## Summary
## 概要
AT-VLA 在预训练的视觉-语言-动作机器人策略中加入带门控的触觉反馈，使其能处理接触密集的操作任务，同时避免削弱接触前的视觉定位能力。它使用慢速视觉-语言流和快速触觉流，在 0.04 s 内对触摸作出反应。

## 问题
- 预训练 VLA 模型在力和接触会决定下一步动作的任务中常常失败，例如拉开包的拉链、盖章、擦拭弯曲花瓶和拧开盖子。
- 大型机器人预训练数据集中很少有触觉数据，微调时加入触觉 token 可能会把注意力从目标物体上移开。
- 标准 VLA 推理速度太慢，难以在闭环接触过程中进行高频触觉修正。

## 方法
- 该模型基于 GO-1 构建。GO-1 是一个使用 InternVL-2B 和 DiT 动作专家的预训练 VLA；AT-VLA 增加了一个轻量级 MLP 触觉编码器，用于处理 3D 法向力和 3D 切向力信号。
- 学习得到的触觉门控根据触觉 token 预测接触或非接触状态，使用人工标注的接触状态以二元交叉熵训练；0.5 阈值用于激活触觉输入。
- 自适应交叉注意力在无接触时保留原始 state-token query，在接触时将 query 切换为触觉 token，同时保持动作专家的形状不变。
- 双流设计以低频运行视觉-语言推理，以高频运行触觉动作修正；推理使用 3:1 的快慢频率比。
- 训练使用动作损失加上 0.01 倍的触觉门控损失。

## 结果
- 真实机器人测试使用 AgiBot Genie1，每个任务有 30-50 次演示，并在四个接触密集任务和两个非接触任务上分别进行每任务 15 次试验。
- 在接触密集任务上，整体成功率高于 GO-1 和 pi_0.5：Unzip Bag 为 0.33，对比 0.20 和 0.00；Stamp 为 0.46，对比 0.13 和 0.20；Wipe Vase 为 0.67，对比 0.07 和 0.33；Unscrew Lid 为 0.53，对比 0.27 和 0.46。
- 在接触阶段性能上与触觉基线相比，AT-VLA 的 Unzip Full 达到 0.33，对比 VTLA 0.00 和 RDP 0.06；Wipe Full 达到 0.67，对比 0.60 和 0.33；Stamp Place 达到 0.46，对比 0.13 和 0.40。
- 在 Unscrew Rotate 上，AT-VLA 得分为 0.53，低于 VTLA 的 0.80 和 RDP 的 0.87；论文称这些基线从理想的人工设定抓取状态开始，而 AT-VLA 必须完成完整任务。
- 在模态缺失测试中，同一组 AT-VLA 权重在没有触觉输入时，Pick Place 得分为 1.0，Open Drawer 为 0.93，Stamp 为 0.20，平均为 0.70；有触觉输入时，Stamp 得分为 0.46，平均为 0.79。
- 论文报告闭环触觉反应时间在 0.04 s 内。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07308v2](https://arxiv.org/abs/2605.07308v2)
