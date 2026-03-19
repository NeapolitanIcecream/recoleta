---
source: arxiv
url: http://arxiv.org/abs/2603.01441v1
published_at: '2026-03-02T04:41:10'
authors:
- Xinyang Wang
- Qian Liu
- Wenjie Ding
- Zhao Yang
- Wei Li
- Chang Liu
- Bailin Li
- Kun Zhan
- Xianpeng Lang
- Wei Chen
topics:
- autonomous-driving
- vision-language-action
- language-action-alignment
- shared-tokenization
- coarse-to-fine-decoding
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Unifying Language-Action Understanding and Generation for Autonomous Driving

## Summary
LinkVLA 是一个面向自动驾驶的视觉-语言-动作模型，试图同时解决“语言指令和实际轨迹不一致”以及“自回归动作生成太慢”这两个关键问题。它通过共享语言/动作离散词表、加入动作到文本的反向理解任务，以及两阶段粗到细解码，在闭环驾驶与指令跟随上都取得提升。

## Problem
- 现有自动驾驶 VLA 模型常出现**语言-动作错位**：模型能“说对”指令含义，但生成的驾驶轨迹并不真正执行该指令，这直接影响安全性、可控性和用户信任。
- 常见动作生成依赖**逐步自回归解码**，长轨迹需要多个串行前向过程，导致推理延迟高，不利于实际部署。
- 仅靠数据增强、后处理强化学习或隐式潜空间对齐，往往没有把语言与动作的双向联系直接嵌入监督学习主干中。

## Approach
- 将**语言 token 与动作 token 统一到一个共享离散 codebook** 中：把连续轨迹量化为 BEV 网格上的动作 token，并与文本词表合并，让单个多模态模型在同一 token 空间里处理理解与生成。
- 为动作离散化加入两个细化设计：**对数坐标变换**提高近场控制分辨率，**空间软标签**用高斯分布替代硬 one-hot，显式利用动作网格的空间邻接关系。
- 在常规“语言/视觉到动作”的生成目标之外，再加入**动作理解目标**：给定视觉与动作序列，反向生成语言描述，相当于让模型学习“这条轨迹在做什么”，从而形成双向语言-动作绑定。
- 用**粗到细（C2F）两步解码**替代逐点自回归：先一次性预测终点，再线性插值得到粗轨迹，最后并行细化所有 waypoint，以降低延迟。

## Results
- 在 **Bench2Drive** 闭环评测中，LinkVLA 取得 **DS 91.01**、**SR 74.55%**，优于 **SimLingo** 的 **DS 85.07 / SR 67.27%**，也高于 **Orion** 的 **DS 77.74 / SR 54.62%**。
- 多能力平均分（Bench2Drive Multi-Ability Mean）达到 **73.40%**，高于 **SimLingo 67.28%**、**Orion 54.72%**、**DriveTransformer 38.60%**。分项上，LinkVLA 在 **Merging 60.00%**、**Overtake 80.00%**、**Brake 93.33%**、**Traffic-Sign 83.68%** 表现突出。
- 延迟对比中，作者的纯自回归版本为 **361ms/step**，改为 **C2F 后降至 48ms/step**，相当于节省约 **86% 推理时间**；同时驾驶分数还从 **90.66** 小幅升至 **91.01**。
- 与其他方法相比，C2F 版本延迟接近 **SimLingo 的 34ms**，但驾驶分数更高（**91.01 vs 85.07**）；也快于 **Orion 的 65ms**，且性能更高（**91.01 vs 77.74**）。
- 论文摘要还声称在**指令跟随准确率**和整体驾驶性能上持续提升，但给定摘录中未提供 Action Dreaming 或 VQA/commentary 的具体数值。

## Link
- [http://arxiv.org/abs/2603.01441v1](http://arxiv.org/abs/2603.01441v1)
