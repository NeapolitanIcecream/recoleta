---
kind: trend
trend_doc_id: 861
granularity: day
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-14T00:00:00'
topics:
- robot learning
- world models
- action representations
- spatial grounding
- data efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-861
tags:
- recoleta/trend
- topic/robot-learning
- topic/world-models
- topic/action-representations
- topic/spatial-grounding
- topic/data-efficiency
language_code: zh-CN
---

# 机器人学习通过预测后果和对齐控制坐标获得提升

## 概览
上一個有数据的日窗口强调了对稀缺动作信号的高效利用。今天的论文延续了这一关注点，并进一步强调预测性监督和显式几何。生成的未来场景、无动作标签视频以及坐标对齐的输入都带来了可测量的策略增益。VIA还表明，能力较强的通用智能体可以通过精心设计的视觉界面控制机器人，无需针对机器人进行专门微调。

## 研究发现

### 预测性监督
未来场景变化正成为控制的直接训练目标。Xiaomi-Robotics-U0生成具身观测和操作视频；加入其合成数据后，策略在分布外任务上的成功率从36.9%升至63.2%。WALA从无动作标签视频中学习语义和几何上的未来变化，再将这些潜在变化连接到可执行动作。在RoboCasa上，它的平均成功率达到75.2%，而基础策略为54.2%。Lumo-2采用相同的设计思路，在生成动作块前先预测与动作相关的潜在动力学，但其节选未提供数值化的基准差距。

#### 资料来源
- [Xiaomi-Robotics-U0: Unified Embodied Synthesis with World Foundation Model](../Inbox/2026-07-13--xiaomi-robotics-u0-unified-embodied-synthesis-with-world-foundation-model.md): 报告了使用生成的具身数据后下游策略取得的改进。
- [WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos](../Inbox/2026-07-13--wala-learning-executable-latent-actions-from-action-labeled-demonstrations-and-action-free-videos.md): 描述了如何从无动作标签的未来观测中学习语义几何潜在动作。
- [Towards Predictive, Aligned, and Scalable Robot Learning](../Inbox/2026-07-13--towards-predictive-aligned-and-scalable-robot-learning.md): 将潜在世界动力学定义为动作生成前使用的中间表示。

### 坐标对齐的感知与动作
两种方法减少了隐式学习相机到动作几何关系的负担。以机器人为中心的点图将机器人坐标系中的XYZ坐标附加到图像网格上。在24项RoboCasa任务中，它将π₀.₅的成功率从55.3%提高到62.9%，在未见过的相机位置下增益更大。Pix2Act则在两个图像平面中预测连续的夹爪关键点轨迹，再通过三角测量将其转换为3D动作。在十项MimicGen任务中，它的平均成功率达到75.2%，比报告中的最强基线高12.1个百分点。这两项结果表明，显式空间定位是提高视角容忍度的实用途径。

#### 资料来源
- [See like a Robot: Robot-Centric Pointmaps for Vision-Language-Action Models](../Inbox/2026-07-13--see-like-a-robot-robot-centric-pointmaps-for-vision-language-action-models.md): 定义了相机坐标系与机器人坐标系之间的不匹配，并介绍了点图解决方案。
- [Pix2Act: Image-Space Manipulation Policies with Equivariant Augmentation](../Inbox/2026-07-13--pix2act-image-space-manipulation-policies-with-equivariant-augmentation.md): 描述了连续图像空间关键点预测，以及通过三角测量恢复末端执行器位姿。

### 机器人监督最少的人类数据
在人类示范的帮助下，机器人数据进入训练流程前就能获得有用的结构。WALA从不含电机动作标签的视频中提取与动作相关的场景变化；只使用10%的带标签示范时，其成功率达到53.9%，而基础策略为18.1%。Regrind从一次人类示范开始，在重定向过程中保持手与物体的接触关系，并使用残差强化学习进行物理优化。在两种机器人手和两项工具使用任务中，仿真成功率为98.7%至99.8%；论文声称可以零样本迁移到硬件，但所检查的节选没有给出数值结果。

#### 资料来源
- [WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos](../Inbox/2026-07-13--wala-learning-executable-latent-actions-from-action-labeled-demonstrations-and-action-free-videos.md): 展示了无标签人类视频如何提供语义和几何动作目标。
- [A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation](../Inbox/2026-07-13--a-minimalist-retargeting-guided-reinforcement-learning-recipe-for-dexterous-manipulation.md): 描述了如何从一次人类示范中学习接触丰富的操作任务。
