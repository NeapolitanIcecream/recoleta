---
kind: ideas
granularity: week
period_start: '2026-06-15T00:00:00'
period_end: '2026-06-22T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot VLA
- robotic manipulation
- world models
- cross-embodiment learning
- robot safety
tags:
- recoleta/ideas
- topic/robot-vla
- topic/robotic-manipulation
- topic/world-models
- topic/cross-embodiment-learning
- topic/robot-safety
language_code: zh-CN
---

# 机器人控制环中的 VLA 安全检查

## 摘要
机器人操作团队现在可以针对具体执行风险测试 VLA 策略：接触密集任务中的过时动作块、危险场景中的不安全动作生成，以及桌面物体上的旋转失效。有用的工作靠近机器人控制环：候选动作选择、执行前拒绝评估，以及面向旋转场景的几何感知动作头。

## 过时 VLA 动作块的运行时选择
使用分块 VLA 策略的机器人团队可以在现有策略外加一个运行时选择器。选择器采样多个动作块，用一个小型世界模型预测每个动作块的潜在未来状态，并执行预测状态最接近当前观测的那个动作块中的下一步动作。

DREAM-Chunk 在不微调基础策略的情况下测试了这种模式。它针对低频 VLA 控制中的一个常见失效：策略先承诺执行一个动作块，但在滑移、接触误差、部分可观测性或外部扰动之后，后续动作会过时。在外部扰动下的精确插入任务中，论文报告 DREAM-Chunk 的成功率为 65%，开环 π0.5 为 10%。辅助模型也足够小，可以靠近控制环运行：摘要提到一个 15M 参数的 JEPA 世界模型，编码加预测少于 10 ms，而 VLA 推理超过 100 ms。

一个实用的采用测试是封装现有的 π0.5 或 SmolVLA 动作分块设置，在强制姿态偏移和轻微人为扰动下运行相同的插入或抓取任务，并比较成功率、延迟，以及所选候选动作在 rollout 中途发生变化的频率。

### 资料来源
- [DREAM-Chunk: Reactive Action Chunking with Latent World Model](../Inbox/2026-06-17--dream-chunk-reactive-action-chunking-with-latent-world-model.md): 概述 DREAM-Chunk 的运行时采样、潜在世界模型匹配、硬件测试、扰动结果和延迟对比。
- [DREAM-Chunk: Reactive Action Chunking with Latent World Model](../Inbox/2026-06-17--dream-chunk-reactive-action-chunking-with-latent-world-model.md): 论文摘要描述了面向基于分块的 VLA 策略的测试时候选动作块和潜在未来选择。

## 危险机器人动作执行前的拒绝评估
为真实机器人准备具身策略的团队应加入执行前安全评估，检查模型是否会拒绝观测场景中的物理危险指令。RoboShackles 给出了一个具体起点：基于真实 DROID 观测构建的 10,000 个危险机器人视频片段，类别包括手部伤害、人体伤害、火灾、电气、水和坠落物风险。

评估规则严格，适合部署审查：只有当模型拒绝指令或不产生可执行动作时，样本才算通过。在报告的测试集中，六个被评估的具身基础模型在所有六个类别上的不安全动作生成率都是 100%。这个结果支持一个范围明确的流程改动：在 VLA 策略移动硬件之前，先用一套拒绝测试集检查它，测试集应包含与现场实际机器人任务对应的家庭和实验室危险。

第一次内部检查可以很小。选择常见工位任务的危险变体，例如靠近人的手伸取物体、在液体附近移动带电设备，或从不稳定堆叠中拉出物体。门禁应记录观测、指令、模型输出，以及输出是否可执行；当模型尝试执行该动作时，应阻止真实试验。

### 资料来源
- [ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models](../Inbox/2026-06-17--roboshackles-a-safety-dataset-for-human-injury-prevention-in-embodied-foundation-models.md): 概述 RoboShackles 的构建方式、六个危险类别、基于拒绝的判定标准，以及六个被测试模型的 100% 不安全动作生成率。
- [ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models](../Inbox/2026-06-17--roboshackles-a-safety-dataset-for-human-injury-prevention-in-embodied-foundation-models.md): 论文文本说明，所有被评估模型在基于拒绝的安全标准下都产生了不安全动作。

## 用于桌面操作策略的旋转等变动作头
桌面操作基准应在将 VLA 策略视为适合多样物体布局之前加入旋转压力测试。测试很简单：旋转场景或物体姿态，然后检查预测动作是否随观测一致旋转，以及同一任务的成功率是否保持。

EquiVLA 为使用冻结视觉语言骨干和流匹配 Diffusion Transformer 动作头的策略给出了一条实现路径。EquiPerceptor 从旋转后的图像视角构建具备旋转感知的视觉 token，EquiActor 用 SO(2)-等变层替换标准动作头。报告的效果很具体：在使用相对控制的 LIBERO 上，EquiVLA 的平均成功率达到 92.6%，GR00T N1.5 为 78.1%。在五个 Mobile ALOHA 真实机器人任务上，它报告的平均成功率为 72%，GR00T N1.5 为 54%。

对机器人实验室来说，近期测试是取一个训练好的桌面 VLA，在不同物体旋转角度下运行固定任务脚本，并检查成功率和动作协方差。如果失败集中出现在旋转布局上，那么在收集更多演示之前，动作头就是加入 SO(2) 结构的明确位置。

### 资料来源
- [EquiVLA: A General Framework for Rotationally Equivariant Vision-Language-Action Models](../Inbox/2026-06-18--equivla-a-general-framework-for-rotationally-equivariant-vision-language-action-models.md): 概述 EquiVLA 的 SO(2)-等变动作架构，以及报告的 LIBERO、CALVIN 和 Mobile ALOHA 结果。
- [EquiVLA: A General Framework for Rotationally Equivariant Vision-Language-Action Models](../Inbox/2026-06-18--equivla-a-general-framework-for-rotationally-equivariant-vision-language-action-models.md): 论文文本解释了当前 VLA 架构缺少旋转结构，必须分别学习相关朝向。
