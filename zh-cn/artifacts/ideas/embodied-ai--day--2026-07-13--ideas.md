---
kind: ideas
granularity: day
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-14T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- world models
- action representations
- spatial grounding
- data efficiency
tags:
- recoleta/ideas
- topic/robot-learning
- topic/world-models
- topic/action-representations
- topic/spatial-grounding
- topic/data-efficiency
language_code: zh-CN
---

# 用于机器人策略训练的坐标对齐监督

## 摘要
机器人学习团队可以在与控制对齐的坐标系中表达未来变化，用明确的多视角几何检查合成轨迹，并利用无动作视频塑造灵巧操作中的残差强化学习，从而提高预测性监督的作用。

## 面向视角稳健 VLA 的机器人坐标系未来变化量训练
整合不同相机设置下示范数据的 VLA 团队需要能够预测物理后果的策略，同时避免重新学习相机坐标系到机器人坐标系的变换。WALA 通过语义和几何未来变化监督，在 RoboCasa 上提升了 21 个百分点；以机器人为中心的点图让 π₀.₅ 提升了 7.6 个百分点，并在未见过的相机位置下扩大了优势。这些结果表明，应在潜在动作训练前，先用机器人坐标系表达未来几何变化。

增加一个解码器，预测以当前末端执行器为中心的机器人中心点图或其变化量。保留 WALA 的语义目标，并让动作头在同一坐标系下训练。这样，预测的场景变化就能直接对应可执行动作。

进行低数据量测试：使用固定相机训练，在未见过的相机位置下评估。比较深度变化量、相机坐标系点图变化量和机器人坐标系点图变化量三种目标。设定试验决策阈值：如果机器人坐标系目标使未见相机位置下的成功率提升不足 5 个百分点，或使固定相机下的成功率下降超过 3 个百分点，就停止采用该目标。

### 资料来源
- [WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos](../Inbox/2026-07-13--wala-learning-executable-latent-actions-from-action-labeled-demonstrations-and-action-free-videos.md): WALA 从语义和几何未来变化中学习可执行的潜在动作，并报告了显著的策略性能提升。
- [See like a Robot: Robot-Centric Pointmaps for Vision-Language-Action Models](../Inbox/2026-07-13--see-like-a-robot-robot-centric-pointmaps-for-vision-language-action-models.md): 以机器人为中心的点图将密集场景几何与机器人的动作坐标系对齐，并提升了视角泛化能力。

## 合成操作视频的多视角几何验收测试
生成机器人训练视频的团队需要一种低成本方法，排除视觉上合理但违反相机标定或夹爪运动学的轨迹。Xiaomi-Robotics-U0 报告称，使用生成数据后，真实策略的分布外成功率从 36.9% 提升到 63.2%；Pix2Act 则表明，位于两个图像平面中的连续夹爪关键点路径可以通过三角测量恢复为精确的 3D 动作。

为每个生成视角附加投影后的夹爪关键点，逐帧进行三角测量，并排除恢复出的位姿在不同视角间不一致、超过关节限制或破坏时间连续性的片段。同样的路径还可以作为生成条件，为模型提供明确的几何控制信号，并为每个合成片段生成审查分数。

生成一批通过检查和未通过检查的匹配数据，训练规模相同的策略，然后在未见过的场景和相机姿态下评估。设定试验决策阈值：如果该检查排除的片段少于 10%，同时使分布外成功率提升不足 3 个百分点，或者通过检查的片段的标定误差仍比真实示范高出 25% 以上，就取消该检查。

### 资料来源
- [Xiaomi-Robotics-U0: Unified Embodied Synthesis with World Foundation Model](../Inbox/2026-07-13--xiaomi-robotics-u0-unified-embodied-synthesis-with-world-foundation-model.md): Xiaomi-Robotics-U0 使用生成的具身数据，提高了下游操作任务的分布外成功率。
- [Pix2Act: Image-Space Manipulation Policies with Equivariant Augmentation](../Inbox/2026-07-13--pix2act-image-space-manipulation-policies-with-equivariant-augmentation.md): Pix2Act 将夹爪运动表示为连续的多视角关键点路径，并通过三角测量恢复 3D 动作。

## 用于单示范灵巧学习的视频派生残差奖励
将工具技能迁移到新机械手的灵巧机器人团队需要超越单条重定向轨迹的奖励信号。Regrind 从一次人类示范中保留手与物体的关系，并通过残差强化学习优化动作。WALA 表明，无动作视频可以提供语义和基于深度的未来变化监督；在标注机器人数据稀缺时，这种监督也能带来较大收益。

在相同工具交互的普通视频上预训练未来变化量编码器。在 Regrind 仿真过程中，除了以物体为中心的关键点跟踪奖励，还根据轨迹与预测的物体运动和接触区域变化的一致性对其评分。这样可以扩大有用的重启状态分布，而不必为每个人类示范都提供电机动作标注。

使用相同的重定向和仿真预算，测试一个剪刀或螺丝刀技能。测量物体姿态受扰动时的成功率、跟踪误差和硬件完成率。设定试验决策阈值：如果基于视频的奖励使受扰动姿态下的成功率提升不足 5 个百分点，使物体跟踪误差增加超过 2 mm，或使硬件完成率低于仅使用关键点奖励的结果，就停止使用该奖励。

### 资料来源
- [A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation](../Inbox/2026-07-13--a-minimalist-retargeting-guided-reinforcement-learning-recipe-for-dexterous-manipulation.md): Regrind 将一次人类示范中的交互关系保持型重定向与残差强化学习结合，用于灵巧工具操作。
- [WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos](../Inbox/2026-07-13--wala-learning-executable-latent-actions-from-action-labeled-demonstrations-and-action-free-videos.md): WALA 从无动作视频中提取语义和几何未来变化，用于可执行策略学习。
