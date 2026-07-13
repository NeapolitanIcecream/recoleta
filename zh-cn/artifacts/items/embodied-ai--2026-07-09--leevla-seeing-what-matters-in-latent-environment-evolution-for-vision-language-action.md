---
source: arxiv
url: https://arxiv.org/abs/2607.08182v1
published_at: '2026-07-09T07:28:21'
authors:
- Qi Lyu
- Baicheng Liu
- Xudong Wang
- Jiahua Dong
- Lianqing Liu
- Zhi Han
topics:
- vision-language-action
- robot-foundation-model
- latent-world-model
- robot-data-scaling
- generalist-robot-policy
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# LEEVLA: Seeing What Matters in Latent Environment Evolution for Vision-Language-Action

## Summary
## 总结
LEEVLA 训练视觉-语言-动作策略，使其关注与任务相关的视觉区域，并预测动作执行后这些区域的潜在特征如何变化。在 LIBERO 和 CALVIN 上，该方法取得了当前最佳结果，同时不增加推理阶段的记忆或计算开销。

## 问题
- VLA 模型常常对每个视觉图像块赋予近似相同的训练权重，使静态背景和无关物体削弱监督信号。
- 依赖人工选择线索的方法，例如深度、分割结果或子目标图像，限制了策略自主发现相关因素的能力，也需要额外处理。
- 对长时域操作、物体外观变化、局部遮挡和多样化场景布局而言，更好的任务相关感知与未来状态推理十分重要。

## 方法
- 漂移引导的动态优先级分配结合相邻时间步之间的特征变化与语言-图像相似度。它提高执行过程中发生变化、并向指令相关语义移动的区域的训练权重。
- 结构化特征流生成在潜在空间中预测未来视觉特征，无需重建像素或生成未来视频。
- 原型到外围预测会对未来特征进行聚类，并从每个簇的质心向外围成员预测各个特征，从而保留局部空间结构和语义结构。
- 互邻域对比损失选择彼此邻近的特征作为正样本对，减少聚类和弱标注演示造成的噪声连接。
- 动作损失、未来特征预测损失和对比损失共同训练策略；优先级分配模块与特征流模块只在训练阶段使用。

## 结果
- 在 LIBERO 上，LEEVLA-large 在 Spatial、Object、Goal 和 Long 四类任务上的平均成功率达到 98.2%，OpenVLA-OFT 和 π0.5 分别为 97.1% 和 97.5%。LEEVLA-large 的四类任务得分分别为 98.8%、99.0%、98.6% 和 96.4%。
- 在 LIBERO 上，拥有 0.5B 参数的 LEEVLA-mini 平均成功率达到 97.5%，四类任务得分分别为 98.6%、99.0%、97.0% 和 95.5%。
- 在 CALVIN ABC-D 上，LEEVLA-large 的平均序列长度达到 4.34，高于 OpenVLA-OFT 的 4.10 和 π0.5 的 4.02。序列长度为 1 至 5 时，其成功率分别为 98.8%、94.5%、87.3%、80.6% 和 72.7%。
- 摘要称，真实世界测试使用 UR5 机械臂完成三个操作任务，每个任务进行 20 次试验，LEEVLA 的表现优于 OpenVLA；所提供的文本没有列出真实世界的具体成功率。
- 报告中的增益支持以下结论：任务引导的区域加权和结构化潜在未来预测能够提升 VLA 的泛化能力与长时域推理能力，同时不增加推理开销。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08182v1](https://arxiv.org/abs/2607.08182v1)
