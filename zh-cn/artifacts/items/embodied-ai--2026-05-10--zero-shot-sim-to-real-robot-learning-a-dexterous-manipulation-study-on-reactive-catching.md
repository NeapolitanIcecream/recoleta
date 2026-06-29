---
source: arxiv
url: https://arxiv.org/abs/2605.09789v1
published_at: '2026-05-10T22:20:20'
authors:
- Kejia Ren
- Gaotian Wang
- Andrew S. Morgan
- Kaiyu Hang
topics:
- sim2real
- dexterous-manipulation
- domain-randomization
- reactive-catching
- reinforcement-learning
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Zero-Shot Sim-to-Real Robot Learning: A Dexterous Manipulation Study on Reactive Catching

## Summary
## 摘要
DRIS 在一组随机化的模拟物体实例上训练单一策略，这些实例在同一动作下并行运动，然后将该策略直接部署到真实机器人上，无需微调。论文把它用于平板反应式接球，这是一个接触丰富、被动稳定性很弱的灵巧操作任务。

## 问题
- 动态灵巧操作对接触时序、摩擦、恢复系数、物体尺寸和传感中的微小误差都很敏感，所以在仿真中训练的策略往往无法迁移到真实机器人。
- 标准领域随机化在每次 rollout 中只采样一个随机实例，这让策略在单次动作序列里接触不确定动力学演化方式的机会很有限。
- 这个任务之所以重要，是因为平板接球没有杯状结构、网兜或手形外壳来托住球，所以策略必须快速反应并准确控制接触。

## 方法
- 核心方法是 Domain-Randomized Instance Set（DRIS）：每个模拟 episode 包含同一物体的多个版本，它们具有不同的物理参数，并且都用同一个机器人动作同时推进。
- 策略接收来自集合编码器的固定长度潜在向量，而不是可变长度的物体状态列表。在接球任务中，编码器是一个点云自编码器，并扩展到 6D 球位置和速度状态。
- 奖励对集合中的实例取平均，因此 PPO 更新更偏向于在多种可能的物体动力学下都有效的动作，而不是只适用于一个采样物体的动作。
- 对接球任务，随机化参数包括球半径、静摩擦、动摩擦和恢复系数。动作控制平板位移和倾角。
- 一个 FiLM 条件化策略使用当前平板倾角来调制编码后的 DRIS 状态，然后由 MLP 输出下一步动作。

## 结果
- 摘要没有给出定量成功率、真实机器人试验次数或消融表。它声称相较于传统领域随机化，DRIS 可以实现可靠的零样本仿真到真实迁移，但展示的文本没有提供成功指标或百分比。
- 摘要称，DRIS 在实例数量不多时也能减少真实世界微调的需求，并以 10 个实例为例。
- 仿真设置使用了 128 个并行环境，每个 episode 最多 20 步，每个 episode 对应 1 秒仿真时间。
- DRIS 编码器数据集使用了每个 DRIS 200 个球、50 个随机动作 episode，以及跨 128 个环境记录的 128,000 条 DRIS 状态样本。
- 编码器训练运行 100 个 epoch，约 10 分钟；PPO 策略训练运行 1000 个 epoch，约 2 小时。
- 真实任务使用的是平坦、低摩擦的平板，而不是杯子、网兜或关节式手，所以这个迁移结果针对的是比机械稳定接球器更难的接球设置。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09789v1](https://arxiv.org/abs/2605.09789v1)
