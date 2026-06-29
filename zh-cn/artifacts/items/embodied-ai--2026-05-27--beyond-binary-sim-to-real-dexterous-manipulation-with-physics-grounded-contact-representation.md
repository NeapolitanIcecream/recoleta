---
source: arxiv
url: https://arxiv.org/abs/2605.28812v1
published_at: '2026-05-27T17:59:02'
authors:
- Jiahe Pan
- Stelian Coros
- Jitendra Malik
- Toru Lin
topics:
- sim2real
- dexterous-manipulation
- tactile-sensing
- contact-representation
- robot-hands
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation

## Summary
## 摘要
CoP 是一种用于零样本仿真到现实灵巧操控的触觉接触表示。它把密集的 taxel 读数转成紧凑的接触力和接触位置，让策略在不依赖真实任务数据训练的情况下使用触觉。

## 问题
- 接触丰富的灵巧操控需要触觉反馈，但真实机器人的数据采集成本很高。
- 原始触觉信号很难在仿真中复现，也很难和硬件对齐，而二值接触信号会丢掉精确控制所需的力和位置细节。
- 论文针对的是视觉帮助很有限的盲操控任务：16-DOF Allegro 手配合 XELA uSkin 传感器完成插销入孔和球平衡。

## 方法
- 该方法使用压力中心（Center-of-Pressure, CoP）：每个触觉感知区域对应一个三维接触力向量和一个三维接触位置。
- 原始 taxel 力通过一个可微的应力分布模型映射到 CoP，这个模型考虑了力在柔顺传感器表面的扩散。
- 反向映射通过在激活 taxel 上求解带正则项的最小二乘问题来估计 CoP 力。
- taxel 方向的标定不需要真实力标签，而是通过在静力平衡下将触觉推断出的外部力矩与测得的关节力矩匹配来完成。
- 策略在 IsaacLab 中训练，使用非对称 actor-critic PPO、循环网络、域随机化、执行器系统辨识和实测的触觉传感器延迟。

## 结果
- 在真实的插销入孔任务中，CoP 的总体成功率为 0.78，覆盖六种形状；对比结果分别是仅力向量 0.67、仅力大小 0.55、二值接触 0.53、仅接触位置 0.50、原始 taxel 0.48、仅本体感觉 0.43。
- 在插销入孔的分布外初始状态下，CoP 的成功率为 0.63；对比结果分别是仅力向量 0.42、仅位置 0.28、原始 taxel 0.27、力大小 0.27、二值接触 0.20、仅本体感觉 0.17。
- 在遮挡的插销入孔实验中，CoP 的成功率为 0.62；对比结果分别是仅力向量 0.57、二值接触 0.52、力大小 0.48、仅位置 0.48、原始 taxel 0.30。
- 按形状看，CoP 的成功率分别是：圆形 1.0、菱形 0.6、椭圆 0.6、六边形 1.0、正方形 0.9、三角形 0.6；每种条件做了 10 次试验。
- 论文声称在插销入孔和球平衡两项任务上都实现了零样本仿真到现实迁移，并且 CoP 在两项任务上都优于二值接触和原始 taxel 基线；摘要片段没有给出球平衡的具体数值。
- 文中报告，学到的 CoP 条件策略状态会编码与任务相关的物理属性，比如物体质量，但摘要片段没有给出质量估计的数值结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28812v1](https://arxiv.org/abs/2605.28812v1)
