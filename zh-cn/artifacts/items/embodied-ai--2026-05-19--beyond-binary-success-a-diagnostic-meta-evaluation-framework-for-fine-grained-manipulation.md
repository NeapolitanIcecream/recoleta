---
source: arxiv
url: https://arxiv.org/abs/2605.19986v1
published_at: '2026-05-19T15:25:13'
authors:
- He-Yang Xu
- Pengyuan Zhang
- Zongyuan Ge
- Xiaoshuai Hao
- Serge Belongie
- Xin Geng
- Yuxin Peng
- Xiu-Shen Wei
topics:
- vision-language-action
- robot-evaluation
- fine-grained-manipulation
- dexterous-manipulation
- spatial-perception
- sim2real
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Binary Success: A Diagnostic Meta-Evaluation Framework for Fine-Grained Manipulation

## Summary
## 摘要
MetaFine 是一个面向细粒度机器人操作的评估系统，把语言理解、空间感知和运动行为分开评估。它表明，二元成功率会高估 VLA 的操作能力，并掩盖失败来源。

## 问题
- 细粒度任务，比如抓取零件、插入槽位和受约束旋转，需要正确的局部语言对齐、精确的空间感知和受控运动。
- 标准具身 AI 基准通常只给出一个通过/失败分数，所以即使部件、接触、方向或顺序错误，也可能把粗粒度移动算作成功。
- 这很重要，因为 VLA 模型在表面指标上看起来能力不错，但在真实机器人灵巧操作所需的局部约束上会失败。

## 方法
- MetaFine 把任务重构为原子技能图，包括抓取部件、对齐、插入、按压部件、切换部件、沿着旋转和沿着滑动。
- 它通过在场景固定的情况下改变属性级指令来测试理解，例如把目标从瓶盖改成瓶身。
- 它用 3 个严重程度级别的几何和光照扰动测试感知，并报告成功率和成功曲线下面积。
- 它把长任务拆成多个阶段，测试行为，并衡量阶段成功率和轨迹平滑度。
- 它整合了 RoboTwin、CALVIN 和 LIBERO 中的任务，扩展到 431 个物体和 4,312 个抓取位姿，并用配对的真实-仿真 rollout 和 prediction-powered inference 做校准后的物理估计。

## 结果
- 常规评估会把细粒度能力高估最多 70%。物体级抓取通常超过 95%，但在部件级约束下，最佳策略在 Grasp Part 上只有 80%，在 Toggle Part 上 85%，在 Press Part 上 68%，在 Rotate Along 上只有 12%。
- 在严重光照扰动下，最好的 Grasp Part 策略从 80% 降到 15%；在视角扰动下保留 55%。在 Toggle Part 上，两种名义成功率相近的模型，85% 和 79%，在 L3 光照下分化为 83% 和 11% 的保留成功率。
- 在语义替换测试中，5 个受评 VLA 在修改后的指令上都得 0%。原始任务表现也下降：pi_0.5 降 31.2%，pi_0 降 34%，OpenVLA-OFT 降 10%，OpenVLA 降 6%，Octo 降 8%。
- 在 peg-in-hole 任务上，5 个 VLA 的总体成功率都接近于零，介于 0% 到 3%。阶段指标把失败拆开：OpenVLA-OFT 的抓取成功率是 47%，对齐成功率是 19%；pi_0.5 的抓取成功率是 39%，对齐成功率是 0%。
- 用多尺度交叉注意力编码器替换 pi_0.5 的 SigLIP 编码器，同时冻结 VLM 主干和动作头，把抓取成功率从 39% 提高到 67%，把对齐成功率从 0% 提高到 32%。
- 真实-仿真混合校准降低了估计方差。pi_0.5 的标准差从 11.5% 降到 2.6%；pi_0 从 5.8% 降到 2.9%。pi_0.5 仅硬件估计的 55% 被校正为 66%，接近 65.0% 的大样本真实参考值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19986v1](https://arxiv.org/abs/2605.19986v1)
