---
source: arxiv
url: http://arxiv.org/abs/2604.23609v1
published_at: '2026-04-26T08:48:26'
authors:
- Teng Xue
- Alberto Rigo
- Bingjian Huang
- Jiayi Shen
- Zhengtong Xu
- Nick Colonnese
- Amirhossein H. Memar
topics:
- contact-rich-manipulation
- visual-tactile-learning
- diffusion-policy
- reactive-control
- dexterous-manipulation
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation

## Summary
## 摘要
Tube Diffusion Policy（TDP）学习一种面向接触密集型任务的反应式视觉-触觉操作策略。它把扩散模型用于动作块起始时的动作生成，并结合一个学习得到的流式反馈流，让机器人能在每一步调整动作，而不是以开环方式执行整段动作块。

## 问题
- 现有许多用于操作任务的模仿学习方法通常会生成多步动作块，并在块内只使用有限反馈来执行。
- 这会影响接触密集型操作，因为物体几何、摩擦和接触事件都存在不确定性，而触觉传感以高频到达，需要快速更新动作。
- 扩散推理较慢也让每个时间步重新规划变得困难，从而降低了系统对扰动和模型失配的鲁棒性。

## 方法
- TDP 用 **action tube** 替代固定的 **action chunk**：前者由一个名义动作初始化和执行过程中的局部反馈修正组成。
- 在每个动作块时间范围开始时，扩散模型通过去噪生成一个初始动作，以处理非线性的接触动力学。
- 在执行过程中，一个根据观测条件学习得到的速度场会根据新的视觉和触觉观测持续生成后续动作，在动作块内部提供逐步修正。
- 该方法采用双时间设计：扩散时间用于去噪，轨迹时间用于实时动作演化。
- 其控制视角受到 tube MPC 启发，但 TDP 直接从示范中学习反馈流，不需要显式动力学模型。

## 结果
- 论文称，TDP 在 Push-T 基准以及另外 **三个** 视觉-触觉灵巧操作任务上，**持续优于当前最先进的模仿学习基线方法**。
- 论文报告了 **两个真实世界实验**，显示它在接触不确定性和外部扰动下有更强的反应能力。
- 论文还表示，action-tube 的逐步修正机制**减少了所需的去噪步数**，因此更适合**实时、高频**反馈控制。
- 当前提供的摘录**不包含定量数字**，例如成功率、误差指标、去噪步数，或与基线相比的具体优势幅度。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23609v1](http://arxiv.org/abs/2604.23609v1)
