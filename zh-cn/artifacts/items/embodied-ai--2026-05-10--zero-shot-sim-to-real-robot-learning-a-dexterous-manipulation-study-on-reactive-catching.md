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
DRIS 用一组随机化的仿真物体实例训练一个策略，这些实例在同一动作下并行运动，然后将该策略部署到真实机器人上，不做微调。论文把这种方法用于平板反应式接球，这是一个接触密集的灵巧操作任务，几乎没有被动稳定机制。

## 问题
- 动态灵巧操作会因接触时机、摩擦、恢复系数、物体尺寸和感知中的小误差而失败，因此在仿真中训练的策略往往无法迁移到真实机器人。
- 标准域随机化在每次 rollout 中采样一个随机化实例，这使策略在单个动作序列中接触不确定动力学演化的机会有限。
- 这个任务有意义，因为平板接球不给机器人提供杯子、网或手部形状来托住球，所以策略必须快速反应并准确控制接触。

## 方法
- 核心方法是 Domain-Randomized Instance Set（DRIS）：每个仿真 episode 包含多个具有不同物理参数的物体版本，所有版本用同一个机器人动作同时推进。
- 策略接收来自集合编码器的固定大小潜向量，而不是可变长度的物体状态列表。在接球任务中，编码器是一个点云自编码器，并扩展到 6D 球位置和速度状态。
- 奖励在集合内的实例上取平均，因此 PPO 更新会偏向于在多种可能物体动力学下都有效的动作，而不是只适配一个采样物体。
- 在接球任务中，随机化参数包括球半径、静摩擦、动摩擦和恢复系数。动作命令包括平板位移和平板倾角。
- FiLM 条件化策略使用当前平板倾角来调制编码后的 DRIS 状态，然后由 MLP 输出下一步动作。

## 结果
- 摘录没有给出定量成功率、真实机器人试验次数或消融表。它声称相对于传统域随机化，DRIS 能可靠地实现零样本 sim-to-real 迁移，但所示文本没有提供成功指标或百分比。
- 摘要称，DRIS 可以用较少的实例数量减少对真实世界微调的需求，并以 10 个实例为例。
- 仿真设置使用了 128 个并行环境，每个 episode 最多 20 步，每个 episode 对应 1 秒仿真时间。
- DRIS 编码器数据集为每个 DRIS 使用 200 个球、50 个随机动作 episode，并在 128 个环境中记录了 128,000 个 DRIS 状态样本。
- 编码器训练运行 100 个 epoch，约 10 分钟；PPO 策略训练运行 1000 个 epoch，约 2 小时。
- 真实任务使用平坦、低摩擦的平板，而不是杯子、网或关节式手，因此其迁移结果针对的是比机械稳定接球器更难的接球设置。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09789v1](https://arxiv.org/abs/2605.09789v1)
