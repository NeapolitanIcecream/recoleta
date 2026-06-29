---
source: arxiv
url: https://arxiv.org/abs/2606.23686v1
published_at: '2026-06-22T17:59:53'
authors:
- Rongxu Cui
- Zongzheng Zhang
- Jingrui Pang
- Haohan Chi
- Jinbang Guo
- Saining Zhang
- Shaoxuan Xie
- Xin Jin
- Yao Mu
- Jiaolong Yang
- Guocai Yao
- Xianyuan Zhan
- Ya-Qin Zhang
- Hao Zhao
topics:
- vision-language-action
- robot-safety-benchmark
- collision-avoidance
- semantic-safety
- robot-data-generation
- human-robot-interaction
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models

## Summary
## 概要
LIBERO-Safety 是一个基准和数据集，用于测试 VLA 机器人策略能否在不发生不安全接触、也不执行不安全指令的情况下完成操作任务。它加入了参数化安全场景、生成的无碰撞演示，以及跨模型评测；评测显示，当前 VLA 在安全约束下仍经常失败。

## 问题
- 现有 VLA 基准更侧重任务完成，而不是安全执行。因此，一个策略可能看起来能力很强，同时却会与杂物、人手或手持物体发生碰撞。
- 这很重要，因为在人附近部署机器人需要控制碰撞、安全处理手与物体的交互，并拒绝有害命令。
- 人工遥操作限制了数据规模；论文报告遥操作每个任务需要 7.4 分钟，这会拖慢安全数据收集。

## 方法
- 该基准用 UBDDL 定义安全任务。UBDDL 是 BDDL 的扩展，会采样场景布局、物体位姿、相机设置、视觉变化、传感器噪声、动态实体和安全谓词。
- 它把安全分为 5 个套件：感知可供性的抓取、人机交互、桌面空间避障、自由空间中的手-物体避障，以及语义安全推理。每个套件有 3 个级别，L0-L2。
- 人类提供稀疏的、以物体为中心的关键位姿。CuRobo 将这些关键位姿转换为完整机器人动作，并在每个时间步检查碰撞。
- 数据生成器为每个关键位姿创建多个空间变体并采样组合，因此一份人工关键位姿脚本可以生成许多演示。

## 结果
- 该基准包含 75 个任务：5 个套件 × 3 个级别 × 5 个任务。生成的场景包括 7,603 个唯一场景、953 个物体和 462 对手-物体组合。
- 数据集包含 19,664 条经过人工筛查的无碰撞演示，覆盖 40 个物理安全训练任务。作者从训练中去除了所有 L2 任务和语义推理套件，以保持这些测试未被见过。
- 与表 2 中的人工遥操作相比，数据收集时间从每个任务 7.4 分钟降至 1.8 分钟，并用规划器碰撞检查取代依赖人工的安全检查。
- 评测覆盖 8 个用于物理安全的 VLA 策略，以及 2 个用于语义拒绝的具身基础模型；物理 rollout 对每个任务使用 10 次试验和 3 个随机种子。
- OpenVLA-OFT 在 AAG-L1 上达到 79.3% SR，在 HRI-L1 上达到 80.0%，在 TSA-L1 上达到 41.3%，在 FSHOA-L1 上达到 50.7%，但在 AAG-L2 上降至 1.3%，在 FSHOA-L2 上降至 42.7%。
- pi0.5 是所示表格中最强的具名基线：HRI-L0 上 SR 为 84.7%，HRI-L1 上为 88.7%，HRI-L2 上为 83.3%，FSHOA-L2 上为 51.3%。它在困难物理安全任务上仍有很大差距，包括 AAG-L2 上的 35.3%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23686v1](https://arxiv.org/abs/2606.23686v1)
