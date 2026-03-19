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
- multi-agent-video-generation
- shared-world-modeling
- world-models
- video-diffusion
- carla-simulation
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# ShareVerse: Multi-Agent Consistent Video Generation for Shared World Modeling

## Summary
ShareVerse提出了一个面向多智能体共享世界建模的视频生成框架，让多个独立智能体生成彼此一致的同一世界视频。它结合了大视频模型、CARLA仿真数据集、多视角拼接和跨智能体注意力，以支持较大时空范围的协同生成。

## Problem
- 现有世界模型和视频生成方法大多面向**单智能体或单视角**，难以保证多个智能体生成的是**同一个一致的物理世界**。
- 多智能体场景需要同时满足：**单个智能体内部多视角几何一致性**，以及**不同智能体之间在重叠区域的世界一致性**与在非重叠区域的合理补全。
- 这很重要，因为共享世界建模是**多人游戏、多机器人协作、无人机群体系统**等应用的基础能力。

## Approach
- 构建了一个基于**CARLA**的大规模多智能体交互数据集：两智能体、每个智能体4个相机视角（前/后/左/右）、3种天气、10多个场景、6类交互轨迹，最终得到**55,000对视频**。
- 将每个智能体的4视角视频做**空间拼接**，让模型一次性看到该智能体的更完整360°环境，从而更容易保持该智能体内部的多视角几何一致性。
- 把相机内参与位姿转换为**raymap嵌入**，作为轨迹/动作条件注入视频扩散模型，使生成过程受相机运动控制。
- 在预训练CogVideoX中加入**cross-agent attention**：把两个智能体的时空特征拼接后做注意力交互，让它们交换位置和场景信息，以保持共享世界一致。
- 框架支持基于首帧条件生成**49帧**未来视频，并联合训练基础模型与新增模块。

## Results
- 在共享世界一致性相关重建指标上，方法达到：**PSNR 20.76、SSIM 0.6656、LPIPS 0.2791**；论文未给出与具体基线方法的数值对比表，因此无法报告相对提升百分比。
- 在**VBench**上，生成质量得分为：**Aesthetic 0.4480、Imaging 0.6468、Temporal Flickering 0.9490、Motion Smoothness 0.9745、Subject Consistency 0.8913、Background Consistency 0.9312**。
- 数据与生成规模方面：数据集包含**55,000对视频**；原始视频约**250帧**，切成**49帧**片段训练；生成分辨率为**480×720**；模型支持**49帧大尺度视频生成**。
- 定性结果声称：模型能同时保持**单智能体四视角内部一致**与**双智能体共享世界一致**，并能较准确感知和生成其他智能体的动态位置。
- 消融实验声称：**四视角训练优于单视角**、**raymap优于直接原始相机值**、**cross-agent attention对交互生成很关键**；但摘录中未提供这些消融的具体数值。

## Link
- [http://arxiv.org/abs/2603.02697v1](http://arxiv.org/abs/2603.02697v1)
