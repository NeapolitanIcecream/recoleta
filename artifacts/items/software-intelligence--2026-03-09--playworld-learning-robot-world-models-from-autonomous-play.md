---
source: arxiv
url: http://arxiv.org/abs/2603.09030v2
published_at: '2026-03-09T23:58:07'
authors:
- Tenny Yin
- Zhiting Mei
- Zhonghe Zheng
- Miyu Yamane
- David Wang
- Jade Sceats
- Samuel M. Bateman
- Lihan Zha
- Apurva Badithela
- Ola Shorinwa
- Anirudha Majumdar
topics:
- robot-world-models
- autonomous-play
- video-diffusion
- robot-manipulation
- policy-evaluation
relevance_score: 0.24
run_id: materialize-outputs
---

# PlayWorld: Learning Robot World Models from Autonomous Play

## Summary
PlayWorld提出一种从机器人自主玩耍数据中训练动作条件视频世界模型的框架，用来更真实地预测接触丰富的操控过程。核心思想是不用依赖成功偏置的人类示范，而是让机器人在无监督条件下持续探索并收集多样交互，再用这些数据训练高保真视频模拟器。

## Problem
- 现有机器人视频世界模型多训练于人类示范数据，数据分布偏向成功轨迹，导致模型难以覆盖失败、碰撞、打滑、形变等关键接触事件。
- 一旦测试时策略偏离训练分布，视频模型容易出现物体凭空出现/消失、重复、错误运动等物理不一致现象，这会削弱策略评估、规划和强化学习的可靠性。
- 这个问题重要，因为机器人操控恰恰依赖对接触动力学的准确建模；如果世界模型在关键接触瞬间失真，下游自动评估和策略改进都会失效。

## Approach
- PlayWorld用一个**VLM任务提出器**根据当前场景图像自动生成多样化自然语言指令，再由预训练**VLA执行器**去执行，从而形成无监督机器人自主演化式“玩耍”数据。
- 它通过指令扰动和自然变化的初始状态来诱发更多行为模式，不靠奖励设计或简单动作噪声，而是用“语义上不同的任务意图”来扩大状态-动作覆盖。
- 为支持长期无人值守采集，系统加入轻量安全过滤与基于VLM的场景重置机制，可连续自主运行最长约8小时，甚至夜间收集数据。
- 世界模型采用预训练稳定视频扩散骨干，联合预测3个相机视角，并在DROID预训练权重上微调，以学习更细粒度的动作到视频动态映射。
- 为缓解玩耍数据中的冗余与长尾分布，作者设计了基于CLIP“距成功轨迹距离”的课程学习：先学常见、容易的过渡，再逐步加入更罕见、更困难的交互样本。

## Results
- 在交互中心基准上，**Robot Play (6h)**相较**Human Demo (6h)**在多个接触场景都有更好感知指标，例如：成功场景LPIPS **0.082 vs 0.084**、SSIM **0.870 vs 0.867**； missed grasp为**0.066/0.883 vs 0.080/0.875**；slide为**0.077/0.865 vs 0.090/0.850**；slip为**0.078/0.871 vs 0.090/0.865**；collision为**0.074/0.888 vs 0.086/0.852**。
- 扩展到**Robot Play (30h)**后继续提升，例如成功场景LPIPS降到**0.071**，slide为**0.073/0.876**，slip为**0.072/0.879**，说明自主玩耍数据在更大规模下仍能带来收益，而人类示范数据更早饱和。
- 加入课程学习后达到最好结果之一：成功场景**LPIPS 0.070 / SSIM 0.880**，slide **0.071 / 0.890**，slip **0.070 / 0.884**，collision **0.072 / 0.893**，表明长尾交互的训练次序也很关键。
- 论文声称PlayWorld在策略评估与失败预测上，相比人类收集数据**最高提升40%**。
- 论文进一步声称，在世界模型内进行强化学习微调后，真实机器人部署的策略成功率相比预训练策略**提升65%**。
- 数据采集方面，系统可在现有DROID平台上进行**最长8小时连续全自主收集**，并支持夜间无人监督采集，体现出较强可扩展性。

## Link
- [http://arxiv.org/abs/2603.09030v2](http://arxiv.org/abs/2603.09030v2)
