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
## 摘要
这篇论文是关于无人机视觉-语言导航的综述。它对该领域进行梳理，正式定义任务，回顾方法和基准，并列出走向真实部署的主要障碍。

## 问题
- UAV-VLN 要求无人机遵循自然语言指令，在复杂的三维环境中长距离导航。
- 这对搜索与救援、基础设施巡检、野火监测，以及 GPS 受限环境下的运行都很重要，因为人工控制或固定交互界面都难以扩展。
- 与地面机器人相比，无人机面临更难的条件：连续三维控制、部分可观测性、语言歧义、户外感知变化，以及很大的仿真到现实差距。

## 方法
- 论文将 UAV-VLN 表述为部分可观测马尔可夫决策过程（POMDP），包含隐藏的世界状态、多模态观测、语言指令，以及把观测历史映射到动作的策略。
- 它按三个阶段建立方法分类：模块化和早期学习系统、长时程时空模型、以及由基础模型驱动的智能体系统。
- 综述追踪了该领域从经典的 SLAM/规划/控制流水线和 CNN-RNN 融合模型，转向 Transformer、视觉-语言地图、认知地图、VLM 规划器、VLA 策略，以及世界模型加 VLA 系统的过程。
- 它也回顾了支撑该领域的基础资源：模拟器、数据集和评估指标，例如成功率（SR）和按路径长度加权的成功率（SPL）。
- 路线图聚焦论文中提出的四个部署限制：仿真到现实迁移、稳健的户外感知、对含糊语言的推理，以及在受限机载硬件上运行大模型。

## 结果
- 这是一篇综述论文，不是新的基准或模型论文。所给摘录没有提供新的量化主结果，例如 SR、SPL 或胜率。
- 论文的主要主张是结构性的：它给出了一套统一分类，覆盖从早期模块化方法到近期用于无人机导航的 VLM、VLA 和世界模型集成智能体。
- 它把 UAV-VLN 形式化为 POMDP，并指出在多智能体场景下可扩展为 DEC-POMDP。
- 它列出了时间线上的一些具体方法例子，包括 AerialVLN baselines（2023）、HAMT（2023）、VLMaps（2023）、FlightGPT（2024）、OpenVLA 7B（2024）、$\pi_{0}$（2024）、GR00T N1（2025）和 Cosmos-Reason1（2025）。
- 摘录中给出了一些来自被引系统的具体实现细节，而不是基准提升：基于记忆的 DRL 以 60 Hz 运行，以及 GRaD-Nav++ 的机载实时控制以 25 Hz 运行。
- 摘录中最明确的贡献是研究路线图：未来工作应聚焦世界模型引导的空中推理、更好的仿真到现实迁移、更安全且更高效的机载部署，以及多智能体群体协同或空地协作。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13654v1](http://arxiv.org/abs/2604.13654v1)
