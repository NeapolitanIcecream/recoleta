---
source: arxiv
url: https://arxiv.org/abs/2607.18709v1
published_at: '2026-07-21T05:05:01'
authors:
- Ziqin Wang
- Hao Li
- Weijun Wang
- Junhao Cai
- Jia Zeng
- Yilun Chen
- Jiangmiao Pang
- Si Liu
topics:
- robot-foundation-model
- embodied-world-model
- vision-language-action
- robot-data-scaling
- robotic-manipulation
relevance_score: 0.99
run_id: materialize-outputs
language_code: zh-CN
---

# RoboInter1.5: A Holistic Intermediate Representation Suite for Embodied World Modeling and Robotic Manipulation

## Summary
## 摘要
RoboInter1.5 提出了一套统一的数据集、基准和模型体系，利用密集的中间表示连接具身推理、机器人操作与世界建模。其核心资源包含超过 230,000 个操作回合，并配有同步的空间、时间和物理标注。

## 问题
- 机器人数据集采集成本高、与具体具身平台绑定，通常只将观测与指令和底层动作配对，缺少实现可泛化规划、控制和仿真所需的细粒度结构。
- 稀疏语言或原始电机动作无法提供充分的空间和物理约束，导致定位能力较弱，并在长时域世界模型展开中累积误差。

## 方法
- RoboInter-Data 为操作视频标注了超过 10 种中间表示，包括子任务、原子技能、物体与夹爪定位、分割、可供性、抓取姿态、接触点、放置提议和运动轨迹。
- RoboInter-VQA 将这些标注转化为空间与时间理解和生成任务，并使用共享的 RoboInter-VLM Planner 预测中间表示。
- RoboInter-VLA 将这些表示用于隐式、显式以及模块化的先规划后执行动作生成。
- RoboInter-World 以渲染的物体点和夹爪轨迹控制视频为条件进行未来视觉预测，为长时域仿真提供结构化的空间信号。

## 结果
- RoboInter-Data 包含来自 571 个场景和 6 种机器人机械臂的超过 230,000 个回合，涵盖 15 种原子技能，并提供逐帧密集标注。
- 该数据集包含近 6,100 万帧物体定位标注、约 7,000 万帧夹爪轨迹、190,000 条可供性与放置标注，以及近 760,000 条语言片段标注。
- RoboInter-VQA 包含约 100 万条空间生成样本、172,000 条空间理解样本、131,000 条时间生成样本和 935,000 条时间理解样本；其中 7,246 个视频用于构建评测池。
- RoboInter-CV 包含来自 16,900 个操作回合的 65,000 个片段样本，覆盖 DROID 和 RH20T，并对齐控制视频、动作、语言、观测和未来状态。
- 摘要称规划器推理、VLA 性能与泛化能力得到提升，长时域世界模型预测也更加可靠；但未提供下游指标值或与基线方法的数值比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18709v1](https://arxiv.org/abs/2607.18709v1)
