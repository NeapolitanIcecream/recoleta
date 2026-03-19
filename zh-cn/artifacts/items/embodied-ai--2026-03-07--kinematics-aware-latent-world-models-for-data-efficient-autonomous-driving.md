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
- autonomous-driving
- world-model
- rssm
- model-based-rl
- kinematics-aware
relevance_score: 0.58
run_id: materialize-outputs
language_code: zh-CN
---

# Kinematics-Aware Latent World Models for Data-Efficient Autonomous Driving

## Summary
本文提出一种面向自动驾驶的运动学感知潜在世界模型，在Dreamer/RSSM式世界模型中显式注入车辆物理状态与几何监督，以提高数据效率和长时想象质量。核心思想是让潜在状态不仅重建像素，还要编码对驾驶决策关键的车道与邻车结构。

## Problem
- 自动驾驶中的强化学习数据成本高、真实交互有安全风险，而纯模型自由方法通常需要大量环境步数才能收敛。
- 现有像素驱动世界模型虽然能做潜在空间想象，但常缺少对空间几何和车辆运动学的显式约束，导致长时预测不稳定、物理一致性不足。
- 这很重要，因为闭环驾驶决策依赖对车道边界、相对朝向、邻车位置与速度的准确表征，而这些关键信息在图像中只占很小部分。

## Approach
- 基于RSSM/DreamerV3构建世界模型：输入前视相机图像和5维车辆物理量（速度、转角、历史动作、横摆率），分别经CNN和MLP编码后拼接成观测嵌入。
- 用RSSM学习潜在动力学，在潜在空间中同时预测重建、奖励和继续信号，并通过想象轨迹训练actor-critic策略，无需每步都与真实环境交互。
- 加入车道监督头，预测左右车道边界距离和相对车道航向角；加入邻车监督头，预测最多3辆周围车辆的相对位置与相对速度。
- 这些辅助头只在训练时使用，其梯度反向约束潜在状态，使潜在表示更符合几何结构和交互语义，而不是只优化像素重建。

## Results
- 在MetaDrive仿真中，作者方法在**80,000真实交互步**内达到接近**200 return**的稳定高回报；对比PPO需要**300,000步**，且收敛水平仍**低于150**。
- 消融中，**ImgOnly**的平均回报/成功率为**176.5 / 0.17**；加入车道和邻车监督后（**Img+Head**）提升到**193.6 / 0.33**，即平均回报约提升**9.7%**、成功率提升**16个百分点**。
- 完整模型**Img+Head+Phys**达到**217.2 / 0.49**；相对Img+Head平均回报再提升约**12.2%**，相对ImgOnly总提升约**23.1%**。
- 去掉奖励/继续头但保留物理输入和几何头时，性能降到**172.6 / 0.18**，说明奖励与终止建模对策略学习也很关键。
- 定性结果显示，ImgOnly会产生模糊邻车位置和错误车道线类型；完整模型可生成更稳定、物理合理的想象轨迹，并更好保留邻车与车道语义。

## Link
- [http://arxiv.org/abs/2603.07264v1](http://arxiv.org/abs/2603.07264v1)
