---
source: arxiv
url: http://arxiv.org/abs/2603.07264v1
published_at: '2026-03-07T15:47:54'
authors:
- Jiazhuo Li
- Linjiang Cao
- Qi Liu
- Xi Xiong
topics:
- world-models
- autonomous-driving
- reinforcement-learning
- rssm
- kinematics-aware
- sample-efficiency
relevance_score: 0.35
run_id: materialize-outputs
language_code: zh-CN
---

# Kinematics-Aware Latent World Models for Data-Efficient Autonomous Driving

## Summary
本文提出一种面向自动驾驶的运动学感知潜在世界模型，在Dreamer/RSSM框架中显式注入车辆物理状态与几何监督，以提升数据效率和长时想象质量。核心价值在于让潜在动态更符合驾驶中的空间结构与物理运动，而不只是重建像素。

## Problem
- 自动驾驶中的强化学习数据成本高、真实交互有安全风险，而纯模型自由方法通常需要大量环境步数才能收敛。
- 现有像素驱动的世界模型虽然能做潜在空间想象，但往往缺少对车道几何、周车相对运动等关键驾驶结构的显式约束。
- 这会导致长时预测不稳定、潜在表示缺乏物理可解释性，进而影响闭环控制和策略优化。

## Approach
- 在RSSM世界模型的观测编码端，将前视相机图像与5维车辆物理量融合，包括速度、转向角、前一动作和横摆角速度，使潜在状态直接锚定到真实运动学信息。
- 在基础的重建、奖励、终止预测之外，增加两个仅训练期使用的辅助监督头：车道几何头预测左右车道边界距离与航向差，邻车头预测最多3辆周车的相对位置与速度状态（12维）。
- 用这些几何/交互相关辅助损失反向约束RSSM潜在状态，使其学习到对驾驶决策更关键的空间语义，而不是只关注像素重建。
- 之后沿用DreamerV3式的想象轨迹 actor-critic 学习，在潜在空间中做H=15步 rollout，用\(\lambda\)-return训练策略与价值函数，从而减少真实环境交互需求。

## Results
- 在MetaDrive仿真中，作者称其方法在**80,000个真实交互步**内即可达到接近**200 return**的稳定高回报；对比之下，**PPO**需要**300,000步**，且最终收敛水平**低于150**。
- 消融结果显示：从**ImgOnly**到加入车道/邻车监督的**Img+Head**，平均回报（MR）从**176.5**提升到**193.6**，成功率（SR）从**0.17**提升到**0.33**；文中总结为MR提升约**9.7%**、SR提升**16个百分点**。
- 完整模型**Img+Head+Phys**达到最佳结果：**MR = 217.2，SR = 0.49**；相对**Img+Head**进一步提升约**12.2%**，相对**ImgOnly**总提升约**23.1%**。
- 去掉奖励/终止头后（仍含图像、物理输入和lane/neigh监督），性能降到**MR = 172.6，SR = 0.18**，说明这些基础预测头对稳定学习也很关键。
- 定性结果方面，作者声称完整模型比纯图像模型产生更稳定、更物理一致的想象轨迹，能更好保持前车位置、车道线颜色/类型等语义；但这部分主要是图示说明，未给出额外量化指标。

## Link
- [http://arxiv.org/abs/2603.07264v1](http://arxiv.org/abs/2603.07264v1)
