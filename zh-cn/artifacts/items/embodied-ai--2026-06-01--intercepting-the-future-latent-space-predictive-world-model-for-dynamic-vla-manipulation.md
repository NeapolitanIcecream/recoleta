---
source: arxiv
url: https://arxiv.org/abs/2606.02486v1
published_at: '2026-06-01T16:55:38'
authors:
- Shahram Najam Syed
- Arthur Jakobsson
- Haoran Hao
- Jeffrey Ichnowski
topics:
- vision-language-action
- robot-foundation-model
- world-model
- dynamic-manipulation
- sim2real
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Intercepting the Future: Latent-Space Predictive World Model for Dynamic VLA Manipulation

## Summary
## 摘要
AHEAD 是一个包装器，用于冻结的 VLA 机器人策略；它会先预测与任务相关的未来视觉 token，再交给动作解码器。论文声称，在动态目标操作任务上，它在仿真和 UFactory xArm 7 上都带来了大幅提升，而且不需要重新训练 7B 的 OpenVLA 基座模型。

## 问题
- 现有 VLA 策略根据最新的相机帧做动作，因此当物体在执行过程中移动时，动作瞄准的是已经过时的位置。
- 这在传送带抓取、滚动球、抛接、交接以及其他依赖拦截窗口的任务中会出问题，因为只靠反应式控制会错过可行动作时间。
- 目标是在保持预训练的 VLA 视觉编码器、语言编码器和动作解码器冻结的前提下，实现实时动态操作。

## 方法
- AHEAD 在冻结的 7B OpenVLA 外围加入了一个 490 万参数的潜空间世界模型。
- RAFT 光流从最近帧估计每个 patch 的速度和加速度。
- 语言与运动掩码只选择与任务相关或在移动的 patch token，通常是 196 个中的 30 到 60 个。
- 一个条件 flow-matching 模型在潜空间中预测未来的 VLA 特征 token，并用恒加速度更新来做运动条件化。
- 当样本方差超过不确定性阈值时，rollout 停止；配置为 Kmax=10、S=5 个样本、5 次 Euler 步，实际常见预测时长为 3 到 5 步。

## 结果
- 在 20 个动态仿真场景中，AHEAD 的成功率为 79% 到 97%；最强基线为 31% 到 58%。
- 在恒速和加速/减速仿真任务中，AHEAD 的成功率为 87.7% 到 97.3%；DreamVLA 的成功率因任务不同为 30.7% 到 58.3%。
- 在 0 到 40 cm/s 的传送带速度扫描中，AHEAD 保持在 95.4% 到 97.6% 的成功率；DreamVLA 从 0 cm/s 时的 96.8% 降到 40 cm/s 时的 47.2%。
- 在 8 个复杂仿真任务上，AHEAD 的成功率为 79.4% 到 95.8%；最好的基线最高只有 60.2%。
- 在遮挡仿真任务中，AHEAD 的成功率为 79.4%；DreamVLA、Open-loop VLA、Retargeting VLA、VLA + Fast Replan 和 Streaming Diffusion Policy 都是 0.0%。
- 在实体 xArm 7 任务上，AHEAD 在三个传送带或滚动球任务中达到 29/30 到 30/30，在拍板拦截任务中达到 23/30，在抛射物接球任务中达到 19/30；这些任务里所有基线都是 0/30。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.02486v1](https://arxiv.org/abs/2606.02486v1)
