---
source: arxiv
url: http://arxiv.org/abs/2604.02190v1
published_at: '2026-04-02T15:48:45'
authors:
- Yongkang Li
- Lijun Zhou
- Sixu Yan
- Bencheng Liao
- Tianyi Yan
- Kaixin Xiong
- Long Chen
- Hongwei Xie
- Bing Wang
- Guang Chen
- Hangjun Ye
- Wenyu Liu
- Haiyang Sun
- Xinggang Wang
topics:
- autonomous-driving
- vision-language-action
- mixture-of-transformers
- driving-planning
- 3d-perception
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving

## Summary
## 总结
UniDriveVLA 是一个面向自动驾驶的统一视觉-语言-行动模型，把理解、感知和规划分到不同的 Transformer 专家中。论文声称，这样可以避免空间感知和语言推理之间的干扰，并在 nuScenes 的开放环评估和 Bench2Drive 的闭环评估上取得最先进结果。

## 问题
- 现有驾驶 VLA 模型面临取舍：直接使用 2D 视觉语言模型能保住语言推理能力，但缺少驾驶所需的空间结构。
- 在共享参数里加入 3D 或空间 token，可能通过表示干扰损害预训练视觉语言模型的推理能力。
- 这很关键，因为自动驾驶既需要语义理解，也需要精确的空间感知，才能做出安全规划。

## 方法
- 该模型采用 Mixture-of-Transformers 设计，包含三个专家：驾驶理解专家、场景感知专家和行动规划专家。
- 理解、感知和行动 token 经过各自专用的专家投影，因此三项功能不会在同一个参数子空间里竞争。
- 一个带掩码的联合注意力层控制信息流：理解 token 保持因果掩码，感知 token 可以读取更早的理解 token，行动 token 可以同时读取语义和空间上下文。
- 感知分支使用基于稀疏查询的解码器，由多尺度 2D 视觉特征构建，不用密集 BEV 或密集 3D 网格；它预测 3D 检测、地图构建、自车状态、运动和占用。
- 训练分三阶段进行：先做多模态预训练，建立语义能力；再联合训练语言、感知和规划，并使用 LoRA 和更低的 VLM 学习率；最后冻结 VLM，对各专家做微调，并加入运动目标。

## 结果
- 论文声称在 **nuScenes** 的开放环评估和 **Bench2Drive** 的闭环评估上都达到了最先进表现。
- 摘要中给出的基准指标包括开放环评估中的 **Avg. L2**，以及闭环评估中的 **Driving Score / Success Rate / Efficiency / Comfortness**，但提供的文本里看不到 UniDriveVLA 这一行，所以这里无法给出它的具体数值。
- 摘要给出了 Bench2Drive 上先前 VLA 方法的闭环基线：**AutoVLA** 达到 **78.84 Driving Score** 和 **57.73% Success Rate**；**SimLingo** 达到 **85.94 Driving Score** 和 **66.82% Success Rate**；**R2SE** 达到 **86.28 Driving Score** 和 **69.54% Success Rate**。
- 一个非 VLA 基线 **AD-MLP** 在开放环上得到 **3.64 Avg. L2**，在闭环 Bench2Drive 上得到 **18.05 Driving Score** 和 **0.00% Success Rate**。
- 论文还声称在 **3D detection、online mapping、motion forecasting** 和 **driving-oriented VQA** 上表现很强，并在 DriveBench 和多个通用 VQA 基准上做了评估，但摘要没有给出这些任务的具体分数。
- 图 2 给出一个定性机制结果：在共享权重解码器里，语言 token 和感知 token 的余弦相似度会升到 **1**；而 MoT 设计会保持较低相似度。作者把这当作特征塌缩减少、任务分离更好的证据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02190v1](http://arxiv.org/abs/2604.02190v1)
