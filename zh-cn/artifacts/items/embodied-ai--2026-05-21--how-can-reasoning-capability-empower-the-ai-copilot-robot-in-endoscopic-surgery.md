---
source: arxiv
url: https://arxiv.org/abs/2605.22322v1
published_at: '2026-05-21T11:08:59'
authors:
- Guankun Wang
- Long Bai
- Hongliang Ren
topics:
- vision-language-action
- surgical-robotics
- endoscopic-surgery
- robot-copilot
- uncertainty-fusion
- deformable-tissue
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# How can reasoning capability empower the AI copilot robot in endoscopic surgery

## Summary
## 摘要
本文认为，具备推理能力的视觉-语言-行动模型，可以让内镜手术中的协作机器人在外科医生监督下更安全、更有用。这是一篇概念性论文，提出了架构方案和临床用例，没有新的实验。

## 问题
- 内镜手术的器械运动受限，可视范围不稳定或有限，组织会变形，还会遇到出血、烟雾和不同患者之间的大幅差异。
- 现有机器人助手能帮忙提高灵巧性和相机稳定性，但在组织状态估计、多器械协调以及不确定事件中的安全动作选择方面仍然吃力。
- 这个问题之所以重要，是因为 LoA 2-3 的手术协作机器人必须支持牵引、分离和止血等精细子任务，同时不能把任务层面的控制权从外科医生手里拿走。

## 方法
- 论文将 AI 协作机器人定义为自治等级 2-3 的系统：它可以生成方案、监测场景并执行受限的低层动作，而外科医生保留任务层面的选择、接管和最终决策权。
- 所提机制使用推理型 VLA 模型读取手术视频和语言意图，然后输出器械和组织的低层运动目标及定位信息。
- 第二个 VLA 风格的运动策略把这些目标连同多模态信号一起映射为运动学变化，例如位置、方向和速度。
- 协作机器人融合内镜视频与 CT/MRI 先验、EUS、OCT、形状传感、EM 跟踪和力的代理信号，并按不确定性给这些输入加权。
- 文中提出用类似思维链的推理来预判组织变形、选择更安全的动作约束、协调多器械配合，并判断何时需要更深层的推断。

## 结果
- 论文没有报告新的定量实验、基准测试、成功率、延迟测量或临床试验结果。
- 其最具体的主张是一个面向 LoA 2-3 的手术协作机器人设计，并对应 4 个自治功能：生成、执行、监测和选择。
- 论文认为推理能力可以改善一些具体子任务，包括对抗牵引与分离的协调、出血点定位、止血，以及对烟雾或血液遮挡的响应。
- 论文提出实际手术使用需要亚秒级响应，但没有给出实测运行时间。
- 论文呼吁未来建立基准，把融合质量、不确定性校准和安全关键结果联系起来，并按每个病例报告时间、资源和能耗。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22322v1](https://arxiv.org/abs/2605.22322v1)
