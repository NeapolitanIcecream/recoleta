---
source: arxiv
url: https://arxiv.org/abs/2605.26282v1
published_at: '2026-05-25T19:06:51'
authors:
- Xiaoyuan Cheng
- Wenxuan Yuan
- Zhancun Mu
- Yuanzhao Zhang
- Yiming Yang
- Hai Wang
- Zhuo Sun
- Che Liu
topics:
- world-model-rl
- diffusion-policy
- model-based-rl
- policy-optimization
- offline-to-online-rl
- robot-policy-scaling
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Scaling World-Model Reinforcement Learning Through Diffusion Policy Optimization

## Summary
## 总结
MBDPO 在潜在世界模型内部训练一个扩散动作策略，让策略搜索和策略学习使用同一分布。论文声称，这解决了模型式强化学习中的一个扩展瓶颈，并且在离线、在线和离线到在线设置中都优于 TD-MPC2。

## 问题
- 现有的世界模型强化学习通常先用非搜索策略产生的动作训练价值函数，再用单独的搜索策略改进行为。这种不一致会让价值函数在搜索到的动作上变得不可靠。
- 搜索会利用分布外动作区域里被高估的价值，这会损害长时程控制，也会削弱更大世界模型带来的扩展效果。
- 这个问题之所以重要，是因为预训练世界模型只有在更大模型和更多数据带来更好策略时才有用。

## 方法
- MBDPO 把策略表示成动作序列上的扩散过程，然后用滚动时域方式执行动作。
- 潜在世界模型对采样得到的动作序列进行展开，并用预测奖励加终止价值进行打分。
- 该方法从这些想象中的展开轨迹中估计扩散 score 场，让去噪步骤把动作序列推向更高回报的动作。
- 一个学习得到的隐式能量函数从回放数据中估计行为策略密度，并加入类似 KL 的信任域，把优化后的策略保持在接近数据分布的位置。
- 世界模型、价值函数、能量函数和扩散策略一起训练，用于离线预训练、在线学习和离线到在线微调。

## 结果
- 在多任务离线预训练中，MBDPO 的表现高于 TD-MPC2，并且模型规模从 1.7M 增加到 340M 参数时，性能单调上升。
- 在从零开始的在线实验中，论文报告它在 4 个基准套件、共 121 个任务上表现更好或具有竞争力。
- 论文在 8 个在线任务上评估了动作漂移和跨 TD 误差；MBDPO 的漂移低于 TD-MPC2，而 η=0.1 的对比版本最接近基础策略。
- 理论部分给出一个价值迭代间隔上界：γ‖Q̂‖∞√(2D_KL^max(π‖β))，把搜索策略漂移和价值误差联系起来。
- 摘要没有给出精确的回报、成功率或归一化得分数值，所以最强的数值结论是 1.7M 到 340M 的扩展范围、4 个基准、121 个任务、8 个任务的漂移研究，以及 η=0.1 版本的比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26282v1](https://arxiv.org/abs/2605.26282v1)
