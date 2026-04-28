---
source: arxiv
url: http://arxiv.org/abs/2604.13654v1
published_at: '2026-04-15T09:20:02'
authors:
- Hanxuan Chen
- Jie Zheng
- Siqi Yang
- Tianle Zeng
- Siwei Feng
- Songsheng Cheng
- Ruilong Ren
- Hanzhong Guo
- Shuai Yuan
- Xiangyue Wang
- Kangli Wang
- Ji Pei
topics:
- uav-vln
- vision-language-action
- world-models
- sim2real
- embodied-ai
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap

## Summary
## 概要
本文是一篇关于无人机视觉-语言导航的综述。它梳理了该领域，正式定义了任务，回顾了方法和基准，并指出了落地到真实世界的主要障碍。

## 问题
- UAV-VLN 要求无人机理解自然语言指令，并在复杂的三维环境中进行长距离导航。
- 这对搜救、基础设施巡检、野火监测以及无 GPS 场景下的作业很重要，因为人工控制或固定交互界面难以很好扩展。
- 与地面机器人相比，无人机面临更难的条件：连续三维控制、部分可观测性、语言歧义、室外感知分布变化，以及较大的 sim-to-real gap。

## 方法
- 论文将 UAV-VLN 表述为部分可观测马尔可夫决策过程（POMDP），其中包括隐藏的世界状态、多模态观测、语言指令，以及将观测历史映射到动作的策略。
- 它构建了一个跨三个阶段的方法分类：模块化和早期学习系统、长时程时空模型，以及由基础模型驱动的智能体系统。
- 综述追踪了方法从传统 SLAM/规划/控制流水线和 CNN-RNN 融合模型，演变到 transformer、视觉-语言地图、认知地图、VLM 规划器、VLA 策略，以及 world-model-plus-VLA 系统。
- 它还回顾了该领域的支撑层：模拟器、数据集和评估指标，例如 Success Rate (SR) 和 Success weighted by Path Length (SPL)。
- 路线图聚焦论文指出的四个部署限制：sim-to-real transfer、稳健的室外感知、在歧义语言下的推理，以及在受限机载硬件上运行大模型。

## 结果
- 这是一篇综述论文，不是提出新基准或新模型的论文。给出的摘录没有提供新的定量结果摘要，例如 SR、SPL 或胜率。
- 论文的主要结论是结构性的：它为无人机导航中的早期模块化方法到近期 VLM、VLA 和融合世界模型的智能体，提供了统一的分类框架。
- 它将 UAV-VLN 正式定义为 POMDP，并指出在多智能体场景下可扩展为 DEC-POMDP。
- 它按时间线列出了具体方法示例，包括 AerialVLN baselines (2023)、HAMT (2023)、VLMaps (2023)、FlightGPT (2024)、OpenVLA 7B (2024)、$\pi_{0}$ (2024)、GR00T N1 (2025) 和 Cosmos-Reason1 (2025)。
- 摘录包含了一些来自被引系统的具体实现细节，而不是基准性能提升：基于记忆的 DRL 以 60 Hz 运行，以及 GRaD-Nav++ 在机载实时控制下以 25 Hz 运行。
- 摘录中最明确的贡献是研究路线图：未来工作应聚焦世界模型引导的空中推理、更好的 sim-to-real transfer、更安全且更高效的机载部署，以及多智能体集群或空地协作。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13654v1](http://arxiv.org/abs/2604.13654v1)
