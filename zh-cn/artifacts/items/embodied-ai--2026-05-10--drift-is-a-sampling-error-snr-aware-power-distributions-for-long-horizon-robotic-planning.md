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
CAPS 是一种用于 VLA 机器人策略的无训练推理时方法。当模型不确定性上升时，它通过搜索未来动作块来减少长时程指令漂移。论文报告称，在 RoboTwin 和 Simpler-WindowX 上，CAPS 的成功率高于 π0、π0.5、TACO 和多个 VLA 基线。

## 问题
- 长时程 VLA 策略可能选择局部概率高的动作，在多步之后丢失原始任务目标。
- 这一点很关键，因为在双臂操作或序列操作中，一个错误动作可能让任务无法恢复。
- 现有提示和重排序方法依赖已采样的候选集合，不能对单条轨迹进行迭代修复。

## 方法
- CAPS 将漂移视为策略轨迹分布中的采样误差。
- 它从幂分布 π(τ) ∝ pθ(τ|I,Ht)^α 中采样，让基础模型判定为更符合指令和历史的轨迹获得更高权重。
- 它使用相对于均匀动作分布的 KL 散度来计算上下文 SNR；由于 SNR = log|A| - entropy，高熵意味着低 SNR。
- 当熵超过阈值 γ 时，CAPS 在动作块上运行 Metropolis-Hastings 搜索：保留前缀，重新采样后缀，然后用幂分布似然比接受或拒绝候选。
- 当熵保持低于 γ 时，它使用贪心执行来节省推理成本。

## 结果
- 在使用 π0 的 RoboTwin 1.0 上，CAPS 的平均成功率达到 47.4%，相比之下 π0 为 32.2%，π0 + TACO 为 41.3%；相对 π0 提高 +15.2 个百分点，相对 TACO 提高 +6.1 个百分点。
- 在 RoboTwin “Dual Bottles Pick Hard” 上，成功率从 π0 的 48.0% 升至 CAPS 的 61.0%；TACO 达到 52.0%。
- 在 Simpler-WindowX 上，CAPS 的平均成功率达到 60.5%，相比之下 π0 为 48.0%，π0 + TACO 为 55.5%，SpatialVLA 为 42.7%，RoboVLM 为 31.3%，Octo 为 16.0%，RT-1-X 为 1.1%。
- 在 Simpler-WindowX “Carrot on Plate” 上，CAPS 得分为 61.0%，相比之下 π0 为 42.0%，π0 + TACO 为 52.0%。
- 理论部分称，当 α = 2 且单步漂移 ε = 0.1 时，理想的幂分布采样可带来 10× 的有效时程扩展；在 MCMC 步数有限时，该界包含一个残余 O(ρ^N) 采样偏差项。
- 摘录称 CAPS 也在 Libero-long 上进行了测试，但可见文本没有提供 Libero-long 的汇总数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09537v1](https://arxiv.org/abs/2605.09537v1)
