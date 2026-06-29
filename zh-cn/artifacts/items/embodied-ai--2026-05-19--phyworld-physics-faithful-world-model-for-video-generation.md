---
source: arxiv
url: https://arxiv.org/abs/2605.19242v1
published_at: '2026-05-19T01:28:52'
authors:
- Pu Zhao
- Juyi Lin
- Timothy Rupprecht
- Arash Akbari
- Chence Yang
- Rahul Chowdhury
- Elaheh Motamedi
- Arman Akbari
- Yumei He
- Chen Wang
- Geng Yuan
- Weiwei Chen
- Yanzhi Wang
topics:
- world-model
- video-generation
- physics-simulation
- preference-optimization
- physical-ai
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# PhyWorld: Physics-Faithful World Model for Video Generation

## Summary
## 摘要
PhyWorld 是一个视频生成世界模型，它在 Wan2.2-I2V-A14B 的基础上继续训练，让视频续写更稳定，也更符合物理规律。论文面向 Physical AI 仿真，但评估的是生成视频质量和物理得分，而不是机器人控制或动作条件策略学习。

## 问题
- Physical AI 需要安全、可扩展的模拟器，因为在真实世界里训练早期机器人策略可能很慢、成本高，也不安全。
- 大型视频生成器可以合成多样的未来画面，但它们在跨帧时常出现颜色、物体身份和运动速度漂移。
- 标准视频基准会漏掉很多物理错误，所以论文增加了按定律评分的评估，覆盖碰撞、流体、阴影、滚动、抛体运动及相关事件。

## 方法
- PhyWorld 以 Wan2.2-I2V-A14B 为起点，加入视频到视频的续写：输入片段先用 Wan-VAE 编码，二值掩码把保留帧和生成帧分开，最后一帧条件通过交叉注意力提供 CLIP 上下文。
- 第一阶段在过滤后的 OpenVid-1M 片段上用 flow matching 微调，使用 CLIP 帧相似度和 UniMatch 光流，去掉几乎静止、闪烁、突变或运动异常的视频。
- 第二阶段在物理偏好对上使用 Direct Preference Optimization。训练 LoRA adapter，基座去噪器保持冻结，作为参考模型。
- DPO 数据来自一个 250 个提示词的文本/图像到视频物理基准，包含 2,000 个预评分视频、约 350 名人工标注者、约 4,500 条清洗后的标注，以及从 2,202 对合格样本中抽取的 1,000 对训练子集。
- 评估同时使用标准视频质量评分，以及经过微调的 Qwen3.5-9B 视频语言裁判，对整体质量和逐条物理定律正确性打 1-5 分的李克特量表。

## 结果
- 在 VBench 上，PhyWorld 的平均分是 0.769；最先进基线的分数为 0.756 或更低。
- 在论文的物理忠实度基准上，PhyWorld 的平均分是 3.09；最强基线是 2.99。
- 这个基准包含 250 个提示词，并对碰撞/回弹、破坏/变形、流体/液体、阴影/反射、链式或多阶段事件、滚动/滑动、抛掷/弹道运动等物理类别评分。
- DPO 扫描显示，step 250 选定的设置是 beta=100；其 Spearman 为 +0.520，beta=30 为 +0.020，最终隐式奖励差值为 +0.200，对比 +0.075。
- 摘要没有报告机器人任务成功率、规划性能、sim-to-real 迁移，或动作条件控制指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19242v1](https://arxiv.org/abs/2605.19242v1)
