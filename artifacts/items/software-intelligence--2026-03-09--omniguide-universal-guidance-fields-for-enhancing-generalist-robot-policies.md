---
source: arxiv
url: http://arxiv.org/abs/2603.10052v1
published_at: '2026-03-09T17:18:13'
authors:
- Yunzhou Song
- Long Le
- Yong-Hyun Park
- Jie Wang
- Junyao Shi
- Lingjie Liu
- Jiatao Gu
- Eric Eaton
- Dinesh Jayaraman
- Kostas Daniilidis
topics:
- robotics
- vision-language-action
- test-time-guidance
- flow-matching
- collision-avoidance
- semantic-grounding
relevance_score: 0.16
run_id: materialize-outputs
---

# OmniGuide: Universal Guidance Fields for Enhancing Generalist Robot Policies

## Summary
OmniGuide 是一个在推理时增强通用机器人策略的统一框架，用外部感知/基础模型提供的 3D 引导场来“推”或“拉”动作采样。它不需要额外机器人数据或重新训练，就能提升 VLA 在复杂操作、避障和精细语义定位任务上的表现。

## Problem
- 现有视觉-语言-动作（VLA）模型虽然覆盖任务广，但在复杂空间理解、拥挤环境操作、精细 manipulation 和安全避障上常出现“最后一公里”失败。
- 传统补救方式通常依赖目标环境中的额外高质量机器人数据和后训练/微调，成本高且稀缺。
- 不同外部能力来源（3D 几何、VLM 语义推理、人类演示）很强，但缺少一种统一、可组合、无需重训的方式去实时指导 VLA。

## Approach
- 核心思想：把各种外部指导统一表示为定义在 3D 空间中的**可微能量函数**，其中目标点产生吸引场、障碍物产生排斥场，再把这些梯度反传到动作生成过程中。
- 对 flow-matching / diffusion 类 VLA，在每个去噪步骤先估计“干净动作”，再通过可微运动学/动力学把动作映射成机器人笛卡尔轨迹，计算任务能量，并用其梯度修正原始生成向量场。
- 该框架支持多种指导源：基于 SDF 的碰撞规避、VLM+深度回投得到的语义目标定位、以及由手部姿态估计提取的一次性人类演示轨迹吸引。
- 还可在初始噪声分布上做能量筛选，与中间去噪引导结合，以更好地在“动作自然性先验”和“任务/安全约束”之间折中。

## Results
- 论文声称在仿真和真实环境、跨多类指导源、跨两个 SOTA 通用策略（如 **π0.5**、**GR00T N1.6**）上都能显著提升表现。
- 文中给出的最强定量结果是：**成功率从 24.2% 提升到 92.4%**，以及**避碰/安全率从 7.0% 提升到 93.5%**；同时声明**没有显著执行延迟**，且**无需重新训练**。
- 作者还声称该统一框架在效果上**达到或超过**先前为特定指导源单独设计的方法，但在提供的摘录中没有看到更细的数据表、具体任务拆分、误差条或显著性检验数值。
- 仿真实验基于 **RoboCasa**，并以 **NVIDIA GR00T N1.6-3B** 作为主干策略之一；摘录说明还做了真实机器人实验，但未给出更完整的逐任务量化结果。

## Link
- [http://arxiv.org/abs/2603.10052v1](http://arxiv.org/abs/2603.10052v1)
