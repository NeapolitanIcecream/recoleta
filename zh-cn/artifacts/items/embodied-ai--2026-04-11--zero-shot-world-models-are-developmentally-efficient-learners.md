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
## 摘要
本文提出 Zero-shot World Model（ZWM），一种自监督视觉预测模型，目标是从有限的自然视频中学习灵活的物理场景理解，并在没有任务专门训练的情况下完成任务。论文的核心主张是：在儿童第一视角视频上训练的模型，可以零样本完成光流、深度、分割和简单物理推理任务，同时与强监督系统保持竞争力。

## 问题
- 论文针对当前视觉学习中的两个缺口：在自然的、接近儿童视角的视频上数据效率较差，以及难以直接用已学表示零样本完成任务。
- 标准的自监督视觉模型通常仍需要为每个下游任务训练带标签的读出层，这与儿童似乎使用同一套通用视觉系统处理多种任务的方式不一致。
- 这对认知建模和 AI 都有意义，因为如果一个系统能从有限的真实世界经验中学到广泛的物理理解，就能减少对精心整理的数据和任务专门监督的依赖。

## 方法
- ZWM 在视频帧对上训练一个带掩码的双帧预测器。它完整看到第一帧，但只能看到第二帧约 **10%** 的图像块，并学习重建完整的第二帧。
- 这种非对称掩码设计是为了迫使模型把外观信息与运动和场景动态分开，利用第 1 帧中的稠密内容和第 2 帧中的稀疏运动线索。
- 训练完成后，模型通过零样本方式被查询：先对输入做一个很小的改动，在原始输入和扰动输入上分别运行预测器，再比较两次输出。输出差异被用来提取目标量，例如运动、深度或对象归属。
- 论文将其描述为近似因果推断：移动一个物体上的某个图像块，观察预测中还有哪些部分发生变化，再用这种传播的变化恢复对象分割或其他结构。
- 更复杂的任务通过组合较简单的提取步骤构建，例如先得到光流，再利用双目流估计相对深度，或把假设运动与光流结合起来做分割和直觉物理推理。

## 结果
- 训练数据：BabyZWM 只在 BabyView 儿童第一视角视频上训练，总计 **868 小时**，来自 **34** 名儿童。论文称这大约相当于 **3 个月的清醒经验**。
- 模型规模与设置：ZWM 使用参数量为 **170M** 和 **1B** 的 ViT 主干网络，在 **150-450 ms** 的帧间隔上训练，输入分辨率为 **256x256**，并揭示第二帧 **10%** 的图像块。
- 光流：论文声称其零样本光流性能达到 **state-of-the-art** 或接近 **state-of-the-art**。在 **TAP-Vid-DAVIS** 上，BabyZWM 被描述为可与监督式 **CoTracker3**、**DPFlow** 和 **SeaRAFT** 竞争，并在遮挡检测上与监督基线持平。在 **TAP-Vid-Kubric** 上，它表现很强，但略低于在合成数据上训练的监督模型。摘录中没有给出精确分数。
- 相对深度：在 **UniQA-3D** 上，ZWM 和 BabyZWM 都能以零样本方式达到 **90% 以上准确率**。论文称它们优于 **Gemini-1.5**、**GPT-4-Turbo** 和 **GPT-4o**，与监督式 **MiDaS-CNN** 和自监督 **MonoDepth2** 单目方法相当，只落后于一个监督式双目模型。
- 对象分割：在 **SpelkeBench** 上，BabyZWM 据称可与监督式 **Mask2Former** 各变体相比，并略低于 **SAM2**。摘录没有提供精确的分割指标。
- 直觉物理：在作者提出的短时间尺度物理推理基准上，**ZWM、BabyZWM 和 V-JEPA2 在所有类别上都接近 100% 表现**，而 **Baby V-JEPA2** 没有达到这一水平。该基准涵盖凝聚、支撑、力传递和力分离。
- 数据效率：一个只用单个儿童 **132 小时** 数据训练的版本，在大多数任务上与完整 BabyZWM 表现相近。按年龄顺序、单次遍历的数据训练设置也表现相近，说明该方法能适应持续学习式课程。
- 消融实验：对称掩码变体（**45%-45%** 和 **90%-90%**）明显差于标准的非对称设置，这支持了论文的说法，即按时间因素拆分的掩码有助于零样本抽象和数据效率。由于摘录未包含完整表格，许多主要对比仍是定性描述。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10333v1](http://arxiv.org/abs/2604.10333v1)
