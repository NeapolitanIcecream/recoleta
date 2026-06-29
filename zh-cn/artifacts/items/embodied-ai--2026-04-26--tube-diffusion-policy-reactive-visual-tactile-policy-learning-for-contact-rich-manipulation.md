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
## 概要
Tube Diffusion Policy（TDP）学习一种用于接触丰富任务的反应式视觉-触觉操作策略。它把扩散模型用于块起始动作生成，并结合一个学习得到的流式反馈流，这样机器人就能在每一步调整动作，而不是执行一个开放环的动作块。

## 问题
- 现有的操作模仿学习方法常常生成多步动作块，并在块内以有限反馈执行。
- 这会影响接触丰富操作，因为物体几何、摩擦和接触事件都存在不确定性，而触觉信号又是高频到达，需要快速更新动作。
- 扩散推理速度较慢，也让按时间步重规划变得困难，从而降低了对扰动和模型失配的鲁棒性。

## 方法
- TDP 用一个 **action tube** 替代固定的 **action chunk**：先给出一个名义动作初始化，再在执行过程中加入局部反馈修正。
- 在每个块时域开始时，扩散模型先去噪，生成一个考虑非线性接触动力学的初始动作。
- 在执行阶段，一个学习得到的、由观测条件化的速度场会根据新的视觉和触觉观测流式生成后续动作，在块内提供逐步修正。
- 该方法采用双时间设计：扩散时间用于去噪，轨迹时间用于实时动作演化。
- 这个控制视角受 tube MPC 启发，但 TDP 直接从示范中学习反馈流，不需要显式动力学模型。

## 结果
- 论文称，TDP 在 Push-T 基准和 **另外三个** 视觉-触觉灵巧操作任务上，都**持续优于**当前最先进的模仿学习基线。
- 文中报告了 **两项真实世界实验**，显示它在接触不确定性和外部扰动下有更强的反应能力。
- 论文还指出，action-tube 的逐步修正**减少了所需的去噪步数**，从而更适合**实时、高频**反馈控制。
- 这段摘要**没有给出**成功率、误差指标、去噪步数或确切基线差距等定量数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23609v1](http://arxiv.org/abs/2604.23609v1)
