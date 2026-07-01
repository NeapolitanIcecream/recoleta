---
source: arxiv
url: https://arxiv.org/abs/2606.31993v1
published_at: '2026-06-30T17:30:05'
authors:
- Arnav Balaji
- Arpit Bahety
- Sriniket Ambatipudi
- Daniel Lam
- Junhong Xu
- "Roberto Mart\xEDn-Mart\xEDn"
topics:
- robot-safety
- manipulation-benchmark
- damage-aware-simulation
- household-manipulation
- sim2real
- vision-language-action
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# OopsieVerse: A Safety Benchmark with Damage-Aware Simulation for Robot Manipulation

## Summary
## 摘要
OopsieVerse 为家用机器人仿真加入明确的损伤跟踪，使策略评估同时覆盖任务完成情况和物理损害。它将 DamageSim 与 OopsieBench 结合；OopsieBench 是一个包含 32 个任务的基准，覆盖 OmniGibson 和 RoboCasa。

## 问题
- 家庭操作基准通常给目标完成情况打分，但不测量物体破损、机器人损伤、热损伤或液体损伤。
- 当失败会损坏机器人或家庭环境时，真实世界训练和评估可能成本高且不安全。
- 现有安全成本通常需要任务特定约束，这使跨任务比较变得困难。

## 方法
- DamageSim 用每个物体和每个连杆的健康值扩展 POMDP；健康值按 0 到 100 的尺度初始化，并在损伤评估器触发时降低。
- 机械损伤使用仿真器接触力和连杆加速度来估计冲击载荷和持续载荷；当载荷超过特定物体阈值时扣减健康值。
- 热损伤在物体温度超过高温或低温阈值时扣减健康值；摘录称该功能只在 OmniGibson 中实现，因为它需要温度状态。
- 液体损伤在液体接触超过阈值时扣减健康值；摘录称该功能只在 OmniGibson 中实现，因为它需要流体粒子。
- OopsieBench 提供带有不安全捷径和更安全替代方案的家庭任务，因此用户可以分别测量成功率和损伤。

## 结果
- OopsieBench 包含 32 个任务实例、21 个独特任务设计、17 个 OmniGibson 任务和 15 个 RoboCasa 任务。
- DamageSim 在 2 个物理栈中实现：基于 Nvidia Omniverse 的 OmniGibson，以及基于 MuJoCo 的 RoboCasa/Robosuite。
- 损伤模型覆盖 3 个主要损伤类别：机械、热和液体；机械损伤包括冲击、压缩和拉伸示例。
- 摘录称实时损伤反馈让人类遥操作演示更安全，但没有给出确切指标或百分比。
- 摘录称有损伤条件模仿学习、损伤感知强化学习、VLA 策略基准测试和 sim-to-real 安全性提升，但所提供文本没有给出定量策略结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31993v1](https://arxiv.org/abs/2606.31993v1)
