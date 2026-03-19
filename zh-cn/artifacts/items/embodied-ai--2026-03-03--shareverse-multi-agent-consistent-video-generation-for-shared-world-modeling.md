---
source: arxiv
url: http://arxiv.org/abs/2603.02697v1
published_at: '2026-03-03T07:41:12'
authors:
- Jiayi Zhu
- Jianing Zhang
- Yiying Yang
- Wei Cheng
- Xiaoyun Yuan
topics:
- world-model
- multi-agent-video-generation
- shared-world-modeling
- video-diffusion
- carla-simulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# ShareVerse: Multi-Agent Consistent Video Generation for Shared World Modeling

## Summary
ShareVerse提出一种面向多智能体共享世界建模的视频生成框架，让多个独立体从各自视角生成彼此一致的同一世界。它结合CARLA构建的新数据集、四视角拼接和跨智能体注意力，在视频层面实现多视角几何一致与跨智能体世界一致。

## Problem
- 现有视频世界模型大多只处理**单智能体/单视角**，难以保证多个智能体生成的是**同一个共享物理世界**。
- 多智能体场景要求同时满足：**每个智能体内部多视角几何一致**，以及**不同智能体之间在重叠区域内容一致、在非重叠区域也能合理推断**。
- 这很重要，因为共享世界建模是**多机器人协作、多人游戏、无人机集群**等系统的基础能力，但现有公开数据与方法都不足以支持该任务。

## Approach
- 基于CARLA构建大规模双智能体同步数据集：每个智能体有前/后/左/右四个相机，覆盖多场景、多天气、六类交互轨迹，最终得到**55,000对视频**，并把长视频切成**49帧**训练片段。
- 把每个智能体的四路视频做**空间拼接**，相当于让模型一次看到该智能体的360°环境，从而更容易保持该智能体内部的多视角几何一致性。
- 将相机内参与位姿转成**raymap嵌入**，作为相机轨迹条件输入视频扩散模型，使生成受控于相机运动而不是只依赖首帧。
- 在预训练CogVideoX中加入**cross-agent attention**：把两个智能体的视频特征拼接后做注意力交互，让它们交换时空与位置信息，从而在重叠区域保持一致，并在非重叠区域根据历史信息合理生成。
- 整体模型支持**49帧、480×720**的视频生成，训练于**CogVideoX-5B-I2V**基础上。

## Results
- 在作者构建的未见场景验证集上，方法达到：**PSNR 20.76**、**SSIM 0.6656**、**LPIPS 0.2791**，用于评估与真值配对帧的一致性与重建质量。
- 在**VBench**上报告的生成质量指标为：**Aesthetic 0.4480**、**Imaging 0.6468**、**Temporal Flickering 0.9490**、**Motion Smoothness 0.9745**、**Subject Consistency 0.8913**、**Background Consistency 0.9312**。
- 论文没有提供与现有公开基线方法的直接数值对比表；更强的具体主张是：其方法能在**双智能体共享世界**中同时保持**单体四视角内部一致**和**跨智能体场景一致**。
- 定性结果声称模型能准确感知其他智能体的动态位置；当改变另一智能体轨迹或修改地图建筑时，生成结果会随之同步变化，表明存在跨智能体信息共享。
- 消融实验的结论是：**四视角训练优于单视角**、**raymap优于直接使用原始相机参数**、**cross-agent attention对交互生成至关重要**，但摘要摘录中未给出对应消融数值。

## Link
- [http://arxiv.org/abs/2603.02697v1](http://arxiv.org/abs/2603.02697v1)
