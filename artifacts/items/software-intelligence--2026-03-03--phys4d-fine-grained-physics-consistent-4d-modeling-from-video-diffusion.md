---
source: arxiv
url: http://arxiv.org/abs/2603.03485v2
published_at: '2026-03-03T20:01:43'
authors:
- Haoran Lu
- Shang Wu
- Jianshu Zhang
- Maojiang Su
- Guo Ye
- Chenwei Xu
- Lie Lu
- Pranav Maneriker
- Fan Du
- Manling Li
- Zhaoran Wang
- Han Liu
topics:
- video-diffusion
- 4d-world-model
- physics-consistency
- simulation-supervision
- reinforcement-learning
relevance_score: 0.18
run_id: materialize-outputs
---

# Phys4D: Fine-Grained Physics-Consistent 4D Modeling from Video Diffusion

## Summary
Phys4D把预训练视频扩散模型逐步提升为带显式几何与运动表示的4D世界模型，目标是生成不仅“看起来对”，而且在时间上更符合物理规律的视频。它结合伪监督、仿真监督和强化学习来提升细粒度物理一致性，并提出了对应的4D评测方案。

## Problem
- 现有视频扩散模型大多按外观匹配训练，常出现局部几何不一致、物体运动不稳定、长期动态不符合因果或物理规律的问题。
- 训练物理一致的4D世界模型缺少可规模化的真实监督，尤其是密集、时间对齐的深度与运动真值很难从真实视频中获取。
- 仅靠外观指标无法判断模型是否真正学到了“世界如何演化”，因此需要世界级的4D一致性评测。

## Approach
- 采用**三阶段训练**：先用伪标签大规模预训练几何/运动头，再用物理仿真数据做监督微调，最后用仿真支撑的强化学习修正残余物理错误。
- 在预训练视频扩散骨干上增加轻量**depth head**和**motion head**，输出每帧深度与相邻帧光流，把纯2D视频生成扩展为显式RGB-D-运动建模。
- 第二阶段引入基于仿真的**warp consistency loss**，要求把时刻t的深度按预测运动场变换后，应与t+1的深度一致，从而显式耦合几何与运动。
- 第三阶段把生成结果提升为4D时空点云，并用与仿真真值之间的**4D Chamfer Distance**作为奖励；将去噪过程视为随机策略，用PPO优化，使长时程轨迹更物理合理。
- 构建大规模仿真数据管线：约**250,000**个环境、**1,250,000**个视频、总计**20,800小时**、**9**类物理现象、**15 TB+**标注，用于几何、运动和奖励监督。

## Results
- 在**Physics-IQ**基准上，**CogVideoX + Phys4D**总分从**18.8**提升到**30.2**（+**11.4**）；同时**MSE**从**0.013**降到**0.009**，**ST-IoU**从**0.116**升到**0.169**，**S-IoU**从**0.222**升到**0.252**，**WS-IoU**从**0.142**升到**0.157**。
- 对**WAN2.2**，Phys4D把总分从**16.8**提升到**25.6**（+**8.8**）；**MSE**从**0.016**降到**0.014**，**ST-IoU**从**0.088**升到**0.107**，**S-IoU**从**0.150**升到**0.214**，**WS-IoU**从**0.105**升到**0.122**。
- 对**Open-Sora V1.2**，总分从**14.5**提升到**22.4**（+**7.9**）；**MSE**从**0.021**降到**0.016**，**ST-IoU**从**0.072**升到**0.098**，**S-IoU**从**0.135**升到**0.195**，**WS-IoU**从**0.092**升到**0.112**。
- 论文还声称在保持强生成质量的同时，显著改善了细粒度时空一致性和物理合理性；评测覆盖**198**个测试场景、**3**个视角、**2**个变体，共**1,188**个测试视频。

## Link
- [http://arxiv.org/abs/2603.03485v2](http://arxiv.org/abs/2603.03485v2)
