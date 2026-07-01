---
source: arxiv
url: https://arxiv.org/abs/2606.31836v1
published_at: '2026-06-30T15:39:29'
authors:
- Xinyi Wang
- Donghan Li
- Zi'Ang Chen
- Chong Yu
- Chen Xin
- Peng Ye
- Yingkai Sun
- Tao Chen
topics:
- humanoid-manipulation
- dexterous-manipulation
- visual-tactile-data
- robot-data-scaling
- imitation-learning
- vision-language-action
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# RoboTacDex: A Dexterous Visual-Tactile-Action Dataset for Humanoid Manipulation

## Summary
## 摘要
RoboTacDex 是一个面向人形机器人操作的数据集，包含 6k 条用于双臂、灵巧手任务的视觉-触觉-动作轨迹。它的主要价值在于数据：在 Unitree G1 上同步采集的多视角 RGB-D、触觉信号、关节状态、动作和任务标注。

## 问题
- 人形机器人操作数据集很少，尤其缺少带触觉感知和多视角深度信息的双臂灵巧手数据集。
- 固定机械臂数据集无法覆盖人形机器人上半身操作所需的高自由度动作空间、双手协调和富接触任务。
- 这一点很关键，因为模仿学习和 VLA 策略需要真实演示，并且需要对齐的观测、动作和接触反馈，才能学习翻页、插书和拧开瓶盖等任务。

## 方法
- 作者使用 Meta Horizon VR 头显遥操作 Unitree G1 人形机器人，并记录由 14-DOF 双臂和 12-DOF Brainco 灵巧手完成的上半身操作。
- 每条轨迹记录 4 个 640x480 RGB-D 相机视角、手臂和手部关节状态、手臂和手指动作，以及双手触觉信号。
- 系统在多相机之间使用硬件和软件同步，以 30 Hz 录制；触觉和手部关节消息以 100 Hz 发布，并与其他模态一起以 30 Hz 记录。
- 数据集覆盖为双臂和灵巧手设计的任务，包括基础操作、关节类操作、双臂协作操作、精细操作和人形交互操作。
- 论文在选定任务上评估 ACT、Diffusion Policy 和 GROOT N1.5，用于测试该数据集能否训练模仿策略。

## 结果
- RoboTacDex 包含 6k 条轨迹，约 25 小时数据，覆盖 19 个任务、23 项技能和 22 个物体。
- 数据集包含 4 个相机视角：头部视角、2 个腕部视角和第三人称视角；大多数任务在 4 种场景设置下采集，由 2 个桌面距离（5 cm 和 15 cm）与 2 种桌面背景组合而成。
- 在每个任务 10 次试验的评估中，GROOT N1.5 平均成功 6/10 次，ACT 为 3/10，Diffusion Policy 为 3/10。
- 在 PickAndPlacePear 上，GROOT N1.5 达到 9/10 成功率，Diffusion Policy 为 3/10，ACT 为 0/10。
- 在更难的任务上，GROOT N1.5 在 TurnPage、InsertBook 和 UnscrewBottle 上分别得到 6/10、4/10 和 6/10；ACT 分别得到 6/10、4/10 和 3/10，Diffusion Policy 分别得到 5/10、3/10 和 2/10。
- 多视角输入没有让受测模型的成功率出现明确提升；触觉输入也没有提高 Diffusion Policy 在 UnscrewBottle 上的成功率，但它将失败模式从空转转向抓握调整失败，说明触觉信号影响了接触行为。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31836v1](https://arxiv.org/abs/2606.31836v1)
