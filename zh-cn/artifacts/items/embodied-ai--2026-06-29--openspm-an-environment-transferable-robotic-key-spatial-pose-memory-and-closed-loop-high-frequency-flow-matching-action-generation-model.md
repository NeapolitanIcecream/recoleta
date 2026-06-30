---
source: arxiv
url: https://arxiv.org/abs/2606.29936v1
published_at: '2026-06-29T08:12:58'
authors:
- Iok Tong Lei
- Qingchen Xie
- Yifan Wang
- Yap Ying Jie
- Zhidong Deng
topics:
- robot-manipulation
- vision-language-action
- spatial-pose-memory
- flow-matching-policy
- sim2real
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# OpenSPM: An Environment-Transferable Robotic Key Spatial Pose Memory and Closed-Loop High-Frequency Flow-Matching Action Generation Model

## Summary
## 概要
OpenSPM 从示教中存储相对于物体的关键位姿，并用这些位姿指导一个小型流匹配动作模型。论文称，与大型 VLA 基线相比，它在 LIBERO-GOAL 上取得了更高的结果，参数少得多，动作输出频率也高得多。

## 问题
- 开放环境中的桌面操作需要语言理解、物体级 6D 几何，以及用于抓取、放置、推动和其他接触阶段的快速控制。
- 大型 VLA 策略可以在语义上泛化，但它们需要大规模机器人数据集，并且通常缺少用于精细操作的相对物体位姿约束。
- 这个问题很重要，因为小的位姿误差会在动作片段之间累积，导致抓取失败、放置不准或碰撞。

## 方法
- OpenSPM 从人类示教中提取关键空间位姿，例如接近、抓取、抬起、预放置和释放。
- 每个关键位姿都存为末端执行器与物体坐标系之间的 SE(3) 相对变换，因此在估计目标物体位姿后，相同的局部几何可以迁移到新场景。
- 一个语义条件 3D 感知模块使用多视角掩码、3D 重建和卡尔曼滤波来估计连续的 6D 物体位姿。
- 推理时，系统根据语言指令检索一条记忆项，将存储的相对位姿迁移到当前场景，检查可行性，并在相邻位姿之间生成短动作块。
- 一个 240K 参数的条件流匹配模型输出长度为 H=5 的动作块，并在接近抓取和放置位姿时结合实时本体感知反馈和终端残差校正。

## 结果
- 在 10 个 LIBERO-GOAL 任务上，每个任务有 50 个初始状态，OpenSPM 报告在 500 个评估 episode 中达到 85.6% 的成功率。
- 它在成功率上超过了列出的基线：Diffusion Policy 68.3%、TraceVLA 75.1%、SpatialVLA 78.6%、OpenVLA 79.2%、WorldVLA 83.4% 和 Octo-Base 84.6%。
- 它报告的动作块生成延迟为 4.8 ms，在 H=5 时等效动作输出频率为 1033.3 Hz。
- 报告的频率高于 Diffusion Policy 14.2 Hz、TraceVLA 2.2 Hz、SpatialVLA 6.7 Hz、OpenVLA 4.9 Hz、WorldVLA 2.4 Hz 和 Octo-Base 54.7 Hz。
- 动作模型有 0.24M 参数；相比之下，Diffusion Policy 约为 260M，Octo-Base 为 200M，SpatialVLA 为 4B，TraceVLA、OpenVLA 和 WorldVLA 为 7B。
- 在 10 个任务中，相对于逐帧 SAM 3 + SAM 3D 视觉参考，卡尔曼位姿预测报告的平均误差为 5.8 mm 位置 MAE 和 2.12° 姿态 MAE。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.29936v1](https://arxiv.org/abs/2606.29936v1)
