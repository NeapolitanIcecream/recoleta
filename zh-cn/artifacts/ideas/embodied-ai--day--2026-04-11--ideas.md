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

## Summary
这组证据中最清楚的操作变化，是对具身控制进行更严格的评估，以及为感知采用更窄但更可复用的预训练方式。STRONG-VLA 支持这样一种部署流程：针对特定的文本和视觉损坏测试 VLA 模型，并在微调时加入单独的干净数据重新对齐阶段。ZWM 支持这样一种感知流程：用一个带掩码的视频预测器探测多个零样本读出，而且已有初步证据表明，即使规模不大的私有视频语料也可能有用。

## 面向 VLA 部署的多模态扰动回归测试
对交付 VLA 策略的团队来说，一个实际的下一步是加入扰动闸门，在部署前和每次微调后都运行一次。STRONG-VLA 为这种闸门提供了可用的基本形态：覆盖文本和视觉的 28 种扰动类型，包括 semantic drift、contextual distractors 和 dynamic visual artifacts 这类留出测试项。论文也说明了为什么这件事应当和训练绑定，而不只是用于评估。两阶段流程——先在不断增加的扰动难度下训练，再用干净数据重新对齐——在保持干净数据表现接近基线的同时，提高了 OpenVLA、OpenVLA-OFT 和 pi0 在 LIBERO 上的成功率。眼下可以先做一个小型内部测试工具，围绕你的机器人实际会遇到的扰动：指令损坏、遮挡、图像偏移和传感器噪声。低成本检查也很直接：比较加入单独的干净数据重新对齐阶段前后，干净任务成功率和扰动任务成功率的变化。如果差距缩小，且干净数据表现没有明显下降，这套训练流程就值得保留。如果没有，团队至少能得到一张具体的失败分布图，而不是只有一个平均成功率数字。

### Evidence
- [STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations](../Inbox/2026-04-11--strong-vla-decoupled-robustness-learning-for-vision-language-action-models-under-multimodal-perturbations.md): 两阶段训练方法、28 种扰动基准，以及干净数据性能权衡的摘要。
- [STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations](../Inbox/2026-04-11--strong-vla-decoupled-robustness-learning-for-vision-language-action-models-under-multimodal-perturbations.md): OpenVLA、OpenVLA-OFT 和 pi0 在 LIBERO 上的具体提升，以及真实机器人验证的说明。

## 用于具身感知、带零样本读出的共享视觉预测器
对机器人和具身感知来说，可复用的视觉预测器现在可以被定义为一个预训练组件，提供多个零样本读出，而不是为光流、深度、分割和短时程物理推理分别训练带标注的模型。ZWM 是这组证据里最清楚的例子。它在配对帧上训练：第一帧完整输入，第二帧只显示约 10% 的 patch，然后在测试时通过小幅输入干预，从预测变化中恢复运动、深度和物体结构。这里更重要的是覆盖范围，而不是某一个基准成绩：BabyZWM 只用 868 小时的儿童第一视角视频训练，在 TAP-Vid-DAVIS 光流上有竞争力，在 UniQA-3D 深度上超过 90%，在 SpelkeBench 分割上表现很强，在论文的短时程物理基准上接近 100%。一个具体可做的方向是搭建内部感知主干，通过一个 API 暴露这些读出，并在任何任务特定微调之前先测试迁移效果。低成本验证步骤是：用目标环境中的一小批自然视频语料训练这个预测器，再检查零样本深度和运动是否仍然足够有用，能支持下游规划或策略学习。

### Evidence
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): 掩码双帧预测器、基于干预的读出方法和基准覆盖范围的摘要。
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): 论文对有限第一视角经验中高数据效率、可灵活复用的视觉认知的论述。

## 将小规模私有视频语料作为零样本感知的预训练输入
收集机器人视频或第一视角视频的团队应当测试：单一场景或单一操作员积累的几百小时数据，是否已经足够支撑较广泛的视觉预训练。ZWM 报告称，一个只用 132 小时数据训练的单儿童模型，在大多数任务上的表现与完整的 868 小时 BabyZWM 接近，按年龄排序的单遍训练也相差不大。这改变了最初的采用方式。你不需要先制定一个大型多任务标注计划，才能从私有视频档案中学到有用的东西。一个具体的流程调整是：先从目标环境中的一份连续语料开始，训练一个带掩码的下一帧预测器，再在构建标注或合成数据流水线之前，先测量零样本运动和深度效果。这一点尤其适合那些拥有专有第一视角视频或机器人视频的实验室和产品团队：这类数据规模不足以支撑传统的监督式感知项目，但足以覆盖常见场景和物体交互。

### Evidence
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): 摘要中包含 132 小时单儿童结果和按年龄排序的单遍训练结果。
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): 论文解释了为什么自然视频一直难以被现有方法利用，以及为什么可复用的零样本行为很重要。
