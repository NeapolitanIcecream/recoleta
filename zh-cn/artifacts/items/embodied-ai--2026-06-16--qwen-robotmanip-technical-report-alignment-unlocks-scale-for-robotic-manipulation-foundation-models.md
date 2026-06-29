---
source: arxiv
url: https://arxiv.org/abs/2606.17846v1
published_at: '2026-06-16T12:14:39'
authors:
- Haoqi Yuan
- Zhixuan Liang
- Anzhe Chen
- Ye Wang
- Haoyang Li
- Pei Lin
- Yiyang Huang
- Zixing Lei
- Tong Zhang
- Jiazhao Zhang
- Jie Zhang
- Jingyang Fan
- Gengze Zhou
- Qihang Peng
- Chenxu Lv
- Xiaoyue Chen
- An Yang
- Fei Huang
- Junyang Lin
- Dayiheng Liu
- Jingren Zhou
- Chenfei Wu
- Xiong-Hui Chen
topics:
- vision-language-action
- robot-foundation-model
- cross-embodiment
- robot-data-scaling
- human-to-robot-synthesis
- ood-evaluation
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models

## Summary
## 摘要
Qwen-RobotManip 是一个基于 Qwen-VL 的操作用视觉-语言-动作模型，目标是实现机器人在分布外场景中的泛化。报告称，跨本体对齐让模型能够在一个 38,100 小时的多来源操作语料库上训练，并在 OOD 测试中超过此前的 VLA 系统。

## 问题
- 机器人操作数据会因机器人身体、摄像头、坐标系、动作空间和任务设置而不同，因此在信号相互冲突时，加入更多数据可能损害训练。
- 现有 VLA 基准常常测试狭窄的域内行为，因此高分可能掩盖模型向新机器人、新指令、新布局和扰动迁移时的弱点。
- 这一点很重要，因为通用机器人策略需要理解语言指令、从错误中恢复，并在不同本体之间迁移技能，而无需为每种机器人重新收集一个大型数据集。

## 方法
- 该模型使用 Qwen-VL 作为视觉-语言基础模型，并在机器人观测、指令、状态和动作上训练动作策略。
- 它把不同机器人映射到一个规范化的状态-动作模板，并使用按维度设置的二进制掩码，使关节和夹爪不同的机器人能够共享训练数据。
- 它预测摄像头坐标系下的末端执行器增量位姿，使视觉上相似的运动在不同坐标系中具有相近的动作值。
- 它使用单个 episode 内近期执行历史作为当前机器人身体的隐式线索，帮助策略根据本体调整动作。
- 它通过人到机器人的合成流水线扩展数据：将第一视角手部轨迹转换为机器人末端执行器运动，渲染到清理后的视频背景上，并为 15 种双臂机器人平台生成数据。

## 结果
- 预训练语料库包含约 38,100 小时的操作数据：3,808 小时单臂机器人数据、6,744 小时双臂机器人数据、868 小时移动和人形机器人数据、1,933 小时人类第一视角数据，以及 24,808 小时人到机器人合成数据。
- 人到机器人流水线将每个人类演示渲染为 15 种双手机器人配置，包括 Panda、UR5e、ARX-L5、xArm7、Sawyer、Kinova Gen3、IIWA、Jaco、FR3、UR10e、ViperX、WidowX、Piper、YAM 和 AgileX ALOHA。
- 训练还使用约 28M 个视觉-语言数据点，以在 VLA 训练期间保留视觉理解、空间推理、OCR、指令跟随和具身推理能力。
- 在 RoboChallenge Table30-v1 通用赛道上，Qwen-RobotManip 排名第 1，相比摘录中报告的此前结果相对提升 20%。
- 报告称，Qwen-RobotManip 在 RoboCasa365、LIBERO-Plus、EBench、RoboTwin-Clean2Rand、RoboTwin-IF 和 RoboTwin-XE 等 OOD 设置中表现优于包括 π0.5 和 GR00T-N1.7 在内的此前 VLA 模型，但摘录没有给出这些基准的准确成功率。
- 真实机器人验证覆盖 4 个平台系列：AgileX ALOHA、Franka、UR 和 ARX，涵盖域内使用、OOD 使用、少样本适应和零样本跨本体迁移。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17846v1](https://arxiv.org/abs/2606.17846v1)
