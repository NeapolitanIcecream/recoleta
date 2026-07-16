---
kind: ideas
granularity: day
period_start: '2026-04-11T00:00:00'
period_end: '2026-04-12T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied-ai
- vla-robustness
- world-models
- zero-shot-vision
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vla-robustness
- topic/world-models
- topic/zero-shot-vision
language_code: zh-CN
---

# 感知与鲁棒性工作流

## 摘要
这组证据里最清楚的操作变化，是把具身控制的评测收紧，把感知预训练做得更窄、更可复用。STRONG-VLA 支持一种部署流程：先用特定的文本和视觉扰动测试 VLA 模型，再用单独的干净数据重新对齐阶段做微调。ZWM 支持一种感知流程：用一个掩码视频预测器去做多个零样本读出，而且已有早期证据表明，哪怕是规模不大的私有视频语料也能派上用场。

## 面向 VLA 部署的多模态扰动回归测试
对于发布 VLA 策略的团队，一个实用的下一步是在部署前和每次微调后都跑一次扰动门控。STRONG-VLA 为这个门控提供了可用的形式：它覆盖文本和视觉的 28 种扰动类型，包括语义漂移、上下文干扰项和动态视觉伪影等留出案例。论文也说明，这件事应该和训练绑定，而不只是做评测。先在逐步增强的扰动难度下训练，再用干净数据重新对齐的两阶段流程，在 OpenVLA、OpenVLA-OFT 和 pi0 上都提高了 LIBERO 成功率，同时把干净性能保持在接近基线的水平。眼下可以先做一个小的内部测试套件，围绕你的机器人实际会遇到的扰动展开：指令污染、遮挡、图像位移和传感器噪声。最便宜的检查很直接：在加入单独的干净数据重新对齐阶段前后，比较干净任务成功率和扰动任务成功率。如果差距缩小，而且干净数据表现没有明显下降，这套训练流程就值得保留。如果没有，团队拿到的是一张具体的失败图，而不是一个平均成功率数字。

### 资料来源
- [STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations](../Inbox/2026-04-11--strong-vla-decoupled-robustness-learning-for-vision-language-action-models-under-multimodal-perturbations.md): Summary of the two-stage training method, 28 perturbation benchmark, and clean-performance tradeoff.
- [STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations](../Inbox/2026-04-11--strong-vla-decoupled-robustness-learning-for-vision-language-action-models-under-multimodal-perturbations.md): Concrete LIBERO gains across OpenVLA, OpenVLA-OFT, and pi0, plus mention of real-robot validation.

## 用于具身感知的共享视觉预测器与零样本读出
机器人和具身感知可以把可复用的视觉预测器收敛成一个预训练组件，再配多个零样本读出，而不是为光流、深度、分割和短时物理推理分别训练带标签模型。ZWM 是这组证据里最清楚的一项。它用成对帧训练：完整输入第一帧，只给第二帧大约 10% 的 patch，然后在测试时通过小的输入干预，从预测变化里恢复运动、深度和物体结构。报告中的覆盖面比单个基准更重要：在 868 小时儿童第一人称视频上训练的 BabyZWM，在 TAP-Vid-DAVIS 光流上有竞争力，在 UniQA-3D 深度上超过 90%，在 SpelkeBench 分割上表现强，在论文的短时程物理基准上接近 100%。这里一个具体的做法，是把内部感知骨干做成一个 API，直接暴露这些读出，并在任何任务特定微调前先做迁移测试。便宜的验证步骤是：用目标环境里较窄的一段自然视频语料训练这个预测器，然后检查零样本深度和运动是否仍然足够支撑下游规划或策略学习。

### 资料来源
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): Summary of the masked two-frame predictor, intervention-based readout method, and benchmark breadth.
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): Paper framing around data-efficient, flexible visual cognition from limited first-person experience.

## 把小规模私有视频语料当作零样本感知的预训练输入
收集机器人视频或第一人称视频的团队，应该先测试：来自一个场景或一个操作者的几百小时数据，是否已经足够支撑广泛的视觉预训练。ZWM 报告说，只用 132 小时、来自单个孩子的模型，在大多数任务上和完整的 868 小时 BabyZWM 表现接近；按年龄顺序单次遍历训练，结果也差不多。这会改变最初的落地步骤。你不需要先做一套庞大的多任务标注计划，才能从私有视频档案里学到有用内容。一个具体的流程调整是，先从目标环境的一段连续语料开始，训练一个掩码下一帧预测器，然后在建立标签或合成数据流水线之前，先测零样本运动和深度。对实验室和产品团队来说，这一点最相关，因为他们手里可能有专有的第一人称或机器人视频，规模还不够支撑传统的监督感知项目，但已经足够覆盖常见场景和物体交互。

### 资料来源
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): Summary includes the 132-hour single-child result and the age-ordered single-pass result.
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): Paper motivation on why natural video has been hard for existing methods and why reusable zero-shot behavior matters.
