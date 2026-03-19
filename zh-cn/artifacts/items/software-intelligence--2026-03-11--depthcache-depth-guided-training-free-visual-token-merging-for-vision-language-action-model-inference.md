---
source: arxiv
url: http://arxiv.org/abs/2603.10469v1
published_at: '2026-03-11T06:40:44'
authors:
- Yuquan Li
- Lianjie Ma
- Han Ding
- Lijun Zhu
topics:
- vision-language-action
- robotic-manipulation
- token-merging
- depth-guided-compression
- inference-acceleration
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# DepthCache: Depth-Guided Training-Free Visual Token Merging for Vision-Language-Action Model Inference

## Summary
DepthCache提出一种**无需训练、无需改模型**的视觉token压缩方法，用深度信息指导VLA（Vision-Language-Action）模型在推理时更聪明地合并图像token，从而降低机器人控制延迟。它重点保留近处操作区域与关键边界，在多个VLA架构上实现了加速且几乎不损失任务成功率。

## Problem
- VLA模型在机器人操作中推理很慢，因为每帧图像会产生大量视觉token并送入大语言模型处理，难以满足闭环实时控制需求。
- 现有token pruning/merging方法通常**统一压缩整张图**或直接丢弃token，容易破坏抓取、对齐、放置所需的精细空间关系。
- 不同VLA架构使用不同视觉编码器，许多现有合并方法需要改模型内部实现，跨模型可移植性差。

## Approach
- 用**深度图作为结构先验**：按深度把未保护的图像patch分区，越远的区域合并比例越高，近处工作空间尽量保留细节。
- 用**双重保护机制**避免误压缩关键token：一部分来自语言模型跨注意力，保护任务相关目标；另一部分来自深度梯度边缘，保护物体边界和遮挡轮廓。
- 不在单帧内一次性做完合并，而是把合并**分摊到连续多帧**中逐步完成，以利用时序冗余并减少帧间不稳定。
- 监控深度变化；若某区域变动态则恢复该区域全分辨率并重新开始渐进合并。
- 对腕部相机增加**基于末端执行器运动的状态机**：运动中更激进压缩，精细抓取/释放时恢复完整视图。

## Results
- 在 **LIBERO** 基准、3个VLA模型上，DepthCache实现 **1.07×–1.28×** 推理加速，同时**平均成功率下降小于1%**。
- **OpenVLA**：基线平均成功率 **76.7%**；加入DepthCache后 **75.7%（-1.0）**，速度 **1.21×**，token保留率 **78.9%**。对比 **FastV**：**64.0%（-12.7）**、**1.39×**；**SP-VLA**：**71.9%（-4.8）**、**1.50×**。
- **π0.5**：基线 **97.9%**；DepthCache **97.6%（-0.3）**，速度 **1.28×**，token保留率 **68.2%**。对比 **FastV**：**77.6%（-20.3）**、**1.30×**；**ToSA**：**73.8%（-24.1）**、**0.94×**。
- **GR00T**：基线 **93.1%**；DepthCache **92.9%（-0.2）**，速度 **1.07×**，token保留率 **87.5%**。
- 双相机稳态下，token数从 **512** 降到约 **300**。
- 真实机械臂实验中（基于 **π0.5**），3项核心任务总成功数从 **55/60** 变为 **52/60**，平均延迟从 **191 ms** 降到 **143 ms**，速度提升 **1.33×**；作者还声称在延迟敏感场景中带来更快任务吞吐和更及时的闭环响应。

## Link
- [http://arxiv.org/abs/2603.10469v1](http://arxiv.org/abs/2603.10469v1)
