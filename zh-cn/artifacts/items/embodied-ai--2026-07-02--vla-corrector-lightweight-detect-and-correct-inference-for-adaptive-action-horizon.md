---
source: arxiv
url: https://arxiv.org/abs/2607.01804v1
published_at: '2026-07-02T07:18:53'
authors:
- Yi Pan
- Miao Pan
- Qi Lu
- Jiaming Huang
- Man Zhang
- Siteng Huang
- Xin Li
- Jie Zhang
- Yongliang Shen
- Xuhong Zhang
- Wenqi Zhang
topics:
- vision-language-action
- robot-policy
- adaptive-action-horizon
- inference-time-correction
- latent-dynamics
- embodied-ai
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon

## Summary
## 摘要
VLA-Corrector 为采用动作块的视觉-语言-动作策略加入推理时监测和纠正。它会截断过时的动作块，并引导下一次重规划，从而提高任务成功率，且通常减少策略调用次数。

## 问题
- 采用动作块的 VLA 策略会以开环方式执行多个预测动作，因此新的相机观测要等到当前动作块结束后才会影响控制。
- 更长的动作时域会降低策略调用成本，但也给接触误差、位姿漂移和滑移留下更多时间，使它们累积成任务失败。
- 固定时域很难调节，因为最佳取值会随任务难度、动力学和仿真到真实环境的差异而变化。

## 方法
- 冻结的 VLA 主干仍然生成动作块；VLA-Corrector 额外加入一个 40M 参数的潜在动力学 MLP，并用示范轨迹训练。
- 潜在空间视觉监测器会根据已执行动作预测预期的视觉潜变量变化，并将其与新相机帧得到的实际潜变量变化进行比较。
- 滑动窗口中位数和 MAD 阈值用于检测持续不匹配；当漂移持续数步时，系统会丢弃当前动作队列中的剩余部分。
- 中断后，在线梯度引导（Online Gradient Guidance）会修改流匹配去噪步骤，使下一个动作块指向潜在纠正方向。
- 这形成了自适应时域：当视觉动力学保持在预期轨道上时，动作块运行更久；当执行开始漂移时，动作块缩短。

## 结果
- 在 MetaWorld 上，pi0.5 的平均成功率从 48.70% 升至 64.35%（+15.65 个百分点）；其 Very Hard 划分从 41.0% 升至 65.0%（+24.0 个百分点）。
- 在 MetaWorld 上，SmolVLA 从 61.90% 提升至 66.65%（+4.75 个百分点），X-VLA 从 55.55% 提升至 59.60%（+4.05 个百分点）。
- 在 LIBERO 上，少样本 pi0.5 加 VLA-Corrector 的平均成功率从 94.00% 提升至 97.80%（+3.80 个百分点），高于完全微调的 pi0.5 基线 96.95%。
- 对于时域为 50 的 pi0.5，成功率从 48.72% 提升至 58.70%，平均策略调用次数从 5.15 降至 4.98，单位调用成功效率提升 24.6%。
- 对于时域为 10 的 SmolVLA，成功率从 61.90% 提升至 73.00%，策略调用次数从 19.27 降至 15.64，单位调用成功效率提升 45.3%。
- Corrector 训练能有效利用有限数据：在 MetaWorld 上、时域为 50 时，使用完整的留出后 corrector 训练划分使平均成功率从 48.72% 提升至 54.32%，而 r=0.6 达到 52.20%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01804v1](https://arxiv.org/abs/2607.01804v1)
