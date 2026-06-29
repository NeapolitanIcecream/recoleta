---
source: arxiv
url: https://arxiv.org/abs/2606.09827v1
published_at: '2026-06-08T17:59:53'
authors:
- Hao Shi
- Weiye Li
- Bin Xie
- Yulin Wang
- Renping Zhou
- Tiancai Wang
- Xiangyu Zhang
- Ping Luo
- Gao Huang
topics:
- vision-language-action
- robot-foundation-model
- temporal-modeling
- world-model
- long-horizon-manipulation
- robot-memory
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models

## Summary
## 摘要
MemoryVLA++ 为视觉-语言-动作机器人策略加入了长期记忆和潜在空间中的未来预测。它面向那些机器人需要记住早先交互或在行动前预判物体运动的操作任务。

## 问题
- 许多 VLA 策略，包括 OpenVLA 和 π0，主要使用当前图像，因此当当前视角没有暴露任务状态时，它们会失败。
- 按按钮需要记忆，因为按钮按下前后场景可能看起来很像；传送带抓取需要未来预测，因为物体运动会改变最佳抓取时机。
- 直接加入过去帧或预测的 RGB 视频成本高，还会带来冗余或与控制无关的视觉数据。

## 方法
- 一个 7B 的 Prismatic VLM 将当前 RGB 观测和语言指令编码为感知 token，用于视觉细节，并编码为一个认知 token，用于任务语义。
- 一个感知-认知记忆库保存过去的感知和认知 token，通过跨注意力检索相关历史，用可学习门控进行融合，并在记忆达到容量上限时合并相邻的相似条目。
- 一个 1.5B 的 Stable Video Diffusion 世界模型，在操作视频上适配后，通过部分去噪而不是解码未来 RGB 帧，在潜在空间中预测未来动态。
- 加入记忆的 token 引导想象未来潜变量的整合，生成把当前感知、过去记忆和未来线索结合起来的时间 token。
- 一个扩散动作专家使用这些 token 来预测单臂或双臂操作的动作序列。

## 结果
- 论文报告了在 5 个仿真基准和 3 类真实机器人任务上、跨 3 台机器人、共近 200 个任务的实验。
- 在仿真中，MemoryVLA++ 在 Libero 上达到 98.4% 成功率，在 SimplerEnv 上达到 74.0%，其中在 SimplerEnv 上相对基线的最高提升为 16.7 个百分点。
- 在长时序任务上，它在 Mikasa-Robo 上达到 44.4% 成功率，在 Calvin 上达到 4.29 分，Mikasa-Robo 上相对基线提升 15.0 个百分点。
- 在 Libero-Plus 上，它在任务和环境变化下达到 82.7% 成功率。
- 在真实机器人测试中，它在通用操作上得分 85%，在长时程、依赖记忆的任务上得分 83%，在长时程、依赖想象的任务上得分 77%。
- 文中报告的真实机器人相对基线提升在这三类任务上分别为 +9、+26 和 +28 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09827v1](https://arxiv.org/abs/2606.09827v1)
