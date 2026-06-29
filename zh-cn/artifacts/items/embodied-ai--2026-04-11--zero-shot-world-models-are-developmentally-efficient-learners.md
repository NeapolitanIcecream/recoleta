---
source: arxiv
url: http://arxiv.org/abs/2604.10333v1
published_at: '2026-04-11T19:32:33'
authors:
- Khai Loong Aw
- Klemen Kotar
- Wanhee Lee
- Seungwoo Kim
- Khaled Jedoui
- Rahul Venkatesh
- Lilian Naing Chen
- Michael C. Frank
- Daniel L. K. Yamins
topics:
- world-model
- self-supervised-video
- zero-shot-vision
- physical-reasoning
- developmental-learning
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# Zero-shot World Models Are Developmentally Efficient Learners

## Summary
## 总结
这篇论文提出了 Zero-shot World Model（ZWM），一种自监督视觉预测模型，目标是用有限的自然视频学习灵活的物理场景理解，并且无需针对具体任务的训练就能完成任务。核心主张是：在儿童自我视角视频上训练的模型，可以零样本完成光流、深度、分割和简单物理推理，同时性能仍然接近强监督系统。

## 问题
- 论文针对当前视觉学习中的两个缺口：在类似儿童的自然视频上数据效率不高，以及从已学表示中零样本复用任务的能力弱。
- 传统自监督视觉模型通常需要针对每个下游任务训练有标签的读出层，这和儿童似乎用同一个通用视觉系统跨任务复用的方式不一致。
- 这对认知建模和 AI 都重要，因为如果系统能从有限的真实世界经验中学到广泛的物理理解，就能减少对整理好的数据和任务专用监督的依赖。

## 方法
- ZWM 在视频对上训练一个带掩码的双帧预测器。它完整看到第一帧，但只看到第二帧大约 10% 的 patch，并学习重建完整的第二帧。
- 这种不对称掩码的目的，是让模型把外观信息和运动、场景动态分开，利用第一帧的密集内容和第二帧的稀疏运动线索。
- 训练后，模型通过一个小输入改动来零样本回答问题：先在原始输入和扰动后的输入上运行预测器，再比较输出。这个差异用来提取运动、深度或物体归属等目标量。
- 论文把这称为近似因果推断：移动物体上的一个 patch，观察预测中还有哪些地方变化，再用这种传播开的变化恢复物体分割或其他结构。
- 更复杂的任务通过组合更简单的提取来完成，例如先得到光流，再用双目光流估计相对深度，或者结合假设运动和光流来做分割和直觉物理。

## 结果
- 训练数据：BabyZWM 只用 BabyView 儿童自我视角视频训练，总计 **868 小时**，来自 **34** 名儿童。论文说这大约相当于 **3 个月的清醒经验**。
- 模型规模和设置：ZWM 使用 **170M** 和 **1B** 参数的 ViT 主干，在 **150-450 ms** 的帧间隔上训练，输入分辨率为 **256x256**，并揭示第二帧 **10%** 的 patch。
- 光流：论文声称其零样本光流性能达到 **state-of-the-art** 或接近 **state-of-the-art**。在 **TAP-Vid-DAVIS** 上，BabyZWM 被描述为与监督式 **CoTracker3**、**DPFlow** 和 **SeaRAFT** 相当，并且在遮挡检测上与监督基线持平。在 **TAP-Vid-Kubric** 上，它表现较强，但略低于在合成数据上训练的监督模型。摘录中没有给出精确分数。
- 相对深度：在 **UniQA-3D** 上，ZWM 和 BabyZWM 的零样本准确率都 **超过 90%**。论文说它们超过 **Gemini-1.5**、**GPT-4-Turbo** 和 **GPT-4o**，与监督式 **MiDaS-CNN** 和自监督 **MonoDepth2** 单目方法相当，只落后于一个监督式双目模型。
- 物体分割：在 **SpelkeBench** 上，BabyZWM 被说成接近监督式 **Mask2Former** 变体，表现略低于 **SAM2**。摘录没有给出精确的分割数值。
- 直觉物理：在作者的短时间尺度物理推理基准上，**ZWM、BabyZWM 和 V-JEPA2 在所有类别上都接近 100% 表现**，而 **Baby V-JEPA2** 没有达到这一水平。该基准覆盖 cohesion、support、force transfer 和 force separation。
- 数据效率：一个 **单儿童** 版本只用一名儿童的 **132 小时** 数据训练，在大多数任务上与完整的 BabyZWM 表现相近。按年龄顺序单次遍历训练的设置也表现相近，说明它能容忍持续学习式课程。
- 消融：对称掩码变体（**45%-45%** 和 **90%-90%**）明显弱于标准的不对称设置，支持这样一个判断：按时间分解的掩码有助于零样本抽象和数据效率。由于摘录里没有完整表格，很多主结果比较只给了定性描述。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10333v1](http://arxiv.org/abs/2604.10333v1)
