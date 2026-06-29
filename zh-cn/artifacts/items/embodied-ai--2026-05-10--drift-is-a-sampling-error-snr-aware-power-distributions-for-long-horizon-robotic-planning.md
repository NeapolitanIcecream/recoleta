---
source: arxiv
url: https://arxiv.org/abs/2605.09537v1
published_at: '2026-05-10T13:49:56'
authors:
- Kewei Chen
- Yayu Long
- Mingsheng Shang
topics:
- vision-language-action
- robot-planning
- inference-time-scaling
- mcmc-sampling
- long-horizon-control
- robot-foundation-models
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning

## Summary
## 摘要
CAPS 是一种无需训练、在推理时运行的方法，用于 VLA 机器人策略。它在模型不确定性上升时，通过搜索未来的动作块来降低长时程指令漂移。它在 RoboTwin 和 Simpler-WindowX 上的成功率高于 π0、π0.5、TACO 以及多个 VLA 基线。

## 问题
- 长时程 VLA 策略可能选择局部上更可能的动作，但经过很多步后会丢失原始任务目标。
- 这很重要，因为在双臂操作或顺序操作中，一次错误动作就可能让任务无法恢复。
- 现有的提示和重排序方法依赖采样得到的候选集，不能对单条轨迹进行迭代修复。

## 方法
- CAPS 将漂移视为策略轨迹分布中的采样错误。
- 它从幂分布中采样，π(τ) ∝ pθ(τ|I,Ht)^α，这会给基础模型判为与指令和历史一致的轨迹更高权重。
- 它用相对于均匀动作分布的 KL 散度计算上下文 SNR；由于 SNR = log|A| - entropy，熵越高，SNR 越低。
- 当熵超过阈值 γ 时，CAPS 在动作块上运行 Metropolis-Hastings 搜索：保留前缀，重新采样后缀，然后用幂分布似然比接受或拒绝候选。
- 当熵保持在 γ 以下时，它使用贪婪执行以节省推理开销。

## 结果
- RoboTwin 1.0 配合 π0：CAPS 的平均成功率达到 47.4%，π0 为 32.2%，π0 + TACO 为 41.3%；相对 π0 提升 15.2 个百分点，相对 TACO 提升 6.1 个百分点。
- RoboTwin 的 “Dual Bottles Pick Hard”：成功率从 π0 的 48.0% 提升到 CAPS 的 61.0%；TACO 为 52.0%。
- Simpler-WindowX：CAPS 的平均成功率达到 60.5%，π0 为 48.0%，π0 + TACO 为 55.5%，SpatialVLA 为 42.7%，RoboVLM 为 31.3%，Octo 为 16.0%，RT-1-X 为 1.1%。
- Simpler-WindowX 的 “Carrot on Plate”：CAPS 得到 61.0%，π0 为 42.0%，π0 + TACO 为 52.0%。
- 理论部分声称，在 α = 2 且单步漂移 ε = 0.1 时，理想的幂分布采样会把有效时程扩展 10 倍；在有限次 MCMC 步数下，这个上界包含一个残余的 O(ρ^N) 采样偏差项。
- 摘要提到 CAPS 也在 Libero-long 上做了测试，但可见文本没有给出汇总的 Libero-long 数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09537v1](https://arxiv.org/abs/2605.09537v1)
