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
## 摘要
AT-VLA 为预训练的视觉-语言-动作机器人策略加入了门控触觉反馈，使它能处理接触密集的操作，同时不损害接触前的视觉对齐。它使用慢速的视觉-语言流和快速的触觉流，在 0.04 s 内对触碰作出反应。

## 问题
- 预训练的 VLA 模型在需要依靠力和接触形状来决定下一步动作的任务中，常常失败，例如拉开袋子拉链、盖章、擦拭弧面花瓶、拧开瓶盖。
- 大规模机器人预训练数据集中很少有触觉数据，在微调时加入触觉 token 会把注意力从目标物体上拉开。
- 标准 VLA 的推理速度太慢，无法在接触过程中的闭环控制里进行高频触觉修正。

## 方法
- 该模型基于 GO-1 构建。GO-1 使用 InternVL-2B 和一个 DiT 动作专家；在此基础上，模型加入了一个轻量级 MLP 触觉编码器，用于 3D 法向力和 3D 切向力信号。
- 一个学习得到的触觉门控根据触觉 token 预测接触与非接触状态，用人工标注的接触状态做二元交叉熵训练；阈值 0.5 时激活触觉输入。
- 自适应交叉注意力在没有接触时保留原始状态 token 查询，在接触时把查询切换为触觉 token，同时保持动作专家的形状不变。
- 双流设计让视觉-语言推理以低频运行，让触觉动作修正以高频运行；推理时快流与慢流的比例为 3:1。
- 训练使用动作损失，加上 0.01 倍的触觉门控损失。

## 结果
- 真实机器人测试使用 AgiBot Genie1，每个任务有 30-50 个示范，在四个接触密集任务和两个非接触任务上，每个任务进行 15 次试验。
- 在接触密集任务上，总体成功率优于 GO-1 和 pi_0.5：Unzip Bag 为 0.33，对比 0.20 和 0.00；Stamp 为 0.46，对比 0.13 和 0.20；Wipe Vase 为 0.67，对比 0.07 和 0.33；Unscrew Lid 为 0.53，对比 0.27 和 0.46。
- 在接触阶段表现上，和触觉基线相比，AT-VLA 在 Unzip Full 上达到 0.33，对比 VTLA 的 0.00 和 RDP 的 0.06；在 Wipe Full 上达到 0.67，对比 0.60 和 0.33；在 Stamp Place 上达到 0.46，对比 0.13 和 0.40。
- 在 Unscrew Rotate 上，AT-VLA 得分为 0.53，低于 VTLA 的 0.80 和 RDP 的 0.87；论文说，这两个基线从理想的手动设定抓取开始，而 AT-VLA 必须完成整个任务。
- 在模态缺失测试中，不输入触觉时，同一组 AT-VLA 权重在 Pick Place 上得分 1.0，在 Open Drawer 上得分 0.93，在 Stamp 上得分 0.20，平均 0.70；输入触觉后，Stamp 得分 0.46，平均 0.79。
- 论文报告闭环触觉反应时间在 0.04 s 以内。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07308v2](https://arxiv.org/abs/2605.07308v2)
