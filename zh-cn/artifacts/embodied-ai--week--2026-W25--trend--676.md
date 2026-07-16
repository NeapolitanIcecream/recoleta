---
kind: trend
trend_doc_id: 676
granularity: week
period_start: '2026-06-15T00:00:00'
period_end: '2026-06-22T00:00:00'
topics:
- robot VLA
- robotic manipulation
- world models
- cross-embodiment learning
- robot safety
run_id: materialize-outputs
aliases:
- recoleta-trend-676
tags:
- recoleta/trend
- topic/robot-vla
- topic/robotic-manipulation
- topic/world-models
- topic/cross-embodiment-learning
- topic/robot-safety
language_code: zh-CN
---

# 机器人 VLA 研究正在用真实控制失效模式来评判

## 概览
本周最强的信号是可部署的机器人操作。视觉-语言-动作（VLA）论文关注共享机器人数据、动作检查和可直接上硬件的动作头。Qwen-RobotManip、DREAM-Chunk 和 EquiVLA 显示出同一优先级：策略必须能处理新的机器人本体、扰动和旋转场景。

## 研究发现

### 跨本体数据与自适应感知
规模声明取决于机器人本体和传感器选择之间的对齐。Qwen-RobotManip 将不同机器人映射到一个共同的状态-动作模板，对缺失维度使用二值掩码，并预测相机坐标系下的末端执行器增量。论文报告的语料约为 38,100 小时，包括覆盖 15 种双手机器人配置的合成人到机器人数据，并在 AgileX ALOHA、Franka、UR 和 ARX 上做了真实机器人验证。

MuseVLA 处理另一类泛化缺口。它根据指令和场景选择热成像、声学、mmWave 或 RGB 感知，再把选中的信号转换成接地的传感器图像。在真实灵巧手任务上，使用合成预训练的版本报告已见任务平均成功率为 80.6%，未见任务为 66.7%。

#### 资料来源
- [Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models](../Inbox/2026-06-16--qwen-robotmanip-technical-report-alignment-unlocks-scale-for-robotic-manipulation-foundation-models.md): Qwen-RobotManip 摘要给出了语料规模、对齐方法、OOD 声明和真实机器人验证。
- [MuseVLA: An Adaptive Multimodal Sensing Vision-Language-Action Model for Robotic Manipulation](../Inbox/2026-06-16--musevla-an-adaptive-multimodal-sensing-vision-language-action-model-for-robotic-manipulation.md): MuseVLA 摘要给出了自适应传感器选择方法和报告的任务成功率。

### 用于运行时校正和策略测试的世界模型
多篇论文在执行期间或接近执行时使用预测模型。DREAM-Chunk 从冻结的 VLA 策略中采样候选动作块，预测它们的潜在未来，并选择预测状态与机器人观测状态匹配的动作。在外部扰动下的精密插入任务中，它报告成功率为 65%，开环 π0.5 为 10%。

Mem-World 使用基于几何的腕部视角记忆，让长程 rollout 保持物体身份和场景布局。它的模拟成功率估计与真实世界成功率的相关性为 r=0.97；合成轨迹帮助微调后的 π0.5 在三个长程任务上达到 72% 的平均成功率，基础策略为 58%。Qwen-RobotWorld 将同一思路扩展到语言条件视频预测，覆盖操作、驾驶、导航和人到机器人数据，使用 8.6M 个视频-文本样本和超过 200M 帧。

#### 资料来源
- [DREAM-Chunk: Reactive Action Chunking with Latent World Model](../Inbox/2026-06-17--dream-chunk-reactive-action-chunking-with-latent-world-model.md): DREAM-Chunk 摘要给出了测试时动作选择方法和硬件结果。
- [Mem-World: Memory-Augmented Action-Conditioned World Models for Persistent Robot Manipulation](../Inbox/2026-06-17--mem-world-memory-augmented-action-conditioned-world-models-for-persistent-robot-manipulation.md): Mem-World 摘要给出了记忆机制、rollout 指标、策略评估相关性和策略改进结果。
- [Unifying Embodied World Modeling Through Language-Conditioned Video Gen](../Inbox/2026-06-18--unifying-embodied-world-modeling-through-language-conditioned-video-gen.md): Qwen-RobotWorld 摘要给出了语言条件视频模型的范围和训练规模。

### 几何感知动作头
动作生成正在加入更多结构。EquiVLA 为基于冻结视觉-语言骨干和流匹配扩散 Transformer 动作头的 VLA 策略加入 SO(2) 旋转等变性。目标行为很直接：场景旋转时，预测动作随之旋转。

报告的收益很具体。在采用相对控制的 LIBERO 上，EquiVLA 达到 92.6% 的平均成功率，GR00T N1.5 为 78.1%。在五个 Mobile ALOHA 真实机器人任务上，它报告平均成功率为 72%，GR00T N1.5 为 54%。这符合本周更广的关注点：能在硬件上工作的动作头、训练循环和预测模型。

#### 资料来源
- [EquiVLA: A General Framework for Rotationally Equivariant Vision-Language-Action Models](../Inbox/2026-06-18--equivla-a-general-framework-for-rotationally-equivariant-vision-language-action-models.md): EquiVLA 摘要给出了旋转等变设计和基准测试结果。

### 具身策略的伤害安全评估
安全研究正在测试具身模型是否会在执行前拒绝危险机器人动作。RoboShackles 从真实 DROID 观测中构建了 10,000 个危险机器人视频片段，覆盖手部和人体直接伤害，以及火灾、电气、涉水和跌落风险。

最有用的结果是诊断性结果。在基于拒绝的判据下，六个被评估的具身基础模型都在每个测试类别中产生了不安全动作。摘录中没有报告量化的安全训练改进，因此有依据的说法是：当前被测试系统未通过这个伤害预防基准。

#### 资料来源
- [ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models](../Inbox/2026-06-17--roboshackles-a-safety-dataset-for-human-injury-prevention-in-embodied-foundation-models.md): RoboShackles 摘要给出了数据集规模、危险类别、评估规则和模型失败结果。
