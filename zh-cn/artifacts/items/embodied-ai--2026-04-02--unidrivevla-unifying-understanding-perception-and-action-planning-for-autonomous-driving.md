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
## 摘要
UniDriveVLA 是一个面向自动驾驶的统一视觉-语言-动作模型，它把理解、感知和规划拆分到不同的 transformer 专家中。论文称，这样可以避免空间感知与语言推理之间的相互干扰，并在 nuScenes 开环评估和 Bench2Drive 闭环评估上达到当前最优结果。

## 问题
- 现有自动驾驶 VLA 模型面临权衡：直接使用 2D 视觉语言模型可以保留语言推理能力，但缺少驾驶所需的空间结构信息。
- 把 3D 或空间 token 加入共享模型参数，可能会因表征相互干扰而削弱预训练视觉语言模型的推理能力。
- 这很重要，因为自动驾驶要做出安全规划，同时需要语义理解和精确的空间感知。

## 方法
- 该模型采用 Mixture-of-Transformers 设计，包含三个专家：驾驶理解专家、场景感知专家和动作规划专家。
- 理解、感知和动作的 token 会经过各自专家专用的投影层，因此这三个功能不会在同一个参数子空间中竞争。
- 一个带掩码的联合注意力层用于控制信息流：理解 token 保持因果掩码，感知 token 可以读取更早的理解 token，动作 token 可以同时读取语义和空间上下文。
- 感知分支使用基于稀疏查询的解码器，由多尺度 2D 视觉特征构成，而不是使用稠密 BEV 或稠密 3D 网格；它预测 3D 检测、地图构建、自车状态、运动和占用。
- 训练分为三个阶段：先进行多模态预训练以获得语义能力，再用 LoRA 和较低的 VLM 学习率对语言、感知、规划进行联合训练，最后在冻结 VLM 的情况下进行专家微调，并加入运动目标。

## 结果
- 论文称，在 **nuScenes** 开环评估和 **Bench2Drive** 闭环评估上都达到当前最优表现。
- 摘录中出现的基准指标包括开环规划的 **Avg. L2**，以及闭环评估的 **Driving Score / Success Rate / Efficiency / Comfortness**，但提供的文本里看不到 UniDriveVLA 对应的结果行，因此这里没有它的具体数值。
- 摘录给出了 Bench2Drive 上已有 VLA 方法的闭环基线结果：**AutoVLA** 达到 **78.84 Driving Score** 和 **57.73% Success Rate**；**SimLingo** 达到 **85.94 Driving Score** 和 **66.82% Success Rate**；**R2SE** 达到 **86.28 Driving Score** 和 **69.54% Success Rate**。
- 一个非 VLA 基线 **AD-MLP** 在开环上得到 **3.64 Avg. L2**，在闭环 Bench2Drive 上得到 **18.05 Driving Score** 和 **0.00% Success Rate**。
- 论文还称，在 **3D detection、online mapping、motion forecasting 和 driving-oriented VQA** 等任务上表现很强，并且还在 DriveBench 和若干通用 VQA 基准上进行了评估，但摘录没有给出这些任务的具体分数。
- 图 2 给出了一个定性机制结果：在共享权重解码器中，语言 token 与感知 token 的余弦相似度会升高并接近 **1**；而 MoT 设计会把这种相似度保持在较低水平。作者据此认为，这说明特征坍塌更少，任务分离更好。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02190v1](http://arxiv.org/abs/2604.02190v1)
