---
source: arxiv
url: http://arxiv.org/abs/2604.14125v1
published_at: '2026-04-15T17:50:07'
authors:
- Tianshuo Yang
- Guanyu Chen
- Yutian Chen
- Zhixuan Liang
- Yitian Liu
- Zanxin Chen
- Chunpu Xu
- Haotian Liang
- Jiangmiao Pang
- Yao Mu
- Ping Luo
topics:
- vision-language-action
- hierarchical-policy
- robot-manipulation
- visual-grounding
- diffusion-policy
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System

## Summary
## 摘要
HiVLA 是一个分层机器人操作系统：视觉语言模型负责规划和视觉指向，单独的扩散策略负责电机控制。论文认为，这种拆分避免了端到端微调带来的推理能力下降，并提升了长时程、杂乱场景中的操作表现。

## 问题
- 端到端视觉-语言-动作模型在小规模、特定领域的机器人控制数据上微调后，常常会失去推理能力。
- 操作任务既需要语义规划，也需要精确到物体层面的感知，尤其是在杂乱场景和多步骤任务中。
- 现有的视觉指向接口往往会丢失全局空间上下文或局部精细细节中的一部分，这会影响细粒度控制。

## 方法
- HiVLA 将系统分成两部分：高层 VLM 规划器和低层 Diffusion Transformer 动作专家。
- VLM 规划器接收任务、场景、动作历史和机器人状态，然后输出一个结构化计划，其中包含子任务指令、技能标签、目标物体和归一化边界框。
- 该边界框用于从原始 1920x1080 相机画面中裁剪出高分辨率局部图像块，让控制器获得目标物体的细节外观。
- 动作专家在 DiT 策略中使用 conditional flow matching，并在每个模块中应用级联交叉注意力，按顺序注入三类信号：全局场景特征、带位置感知的局部裁剪特征，以及子任务语言嵌入。
- 局部裁剪 token 使用与其在原始图像中坐标绑定的绝对位置嵌入，因此该策略同时保留物体细节和场景位置。

## 结果
- 在 RoboTwin 2.0 基准上，HiVLA 的总平均成功率达到 **83.3%**，而 **H-RDT** 为 **70.6%**，**StarVLA** 为 **46.4%**，**pi_0** 为 **45.6%**，**pi_0.5** 为 **44.8%**。
- 论文称，在 RoboTwin 2.0 上，这比 **H-RDT** 绝对提高了 **17.7 个百分点**，比 **pi_0** 绝对提高了 **42.7 个百分点**。
- 在高难任务上，HiVLA 的平均成功率为 **73.2%**，而 **H-RDT** 为 **54.6%**，**pi_0/pi_0.5/StarVLA** 为 **36.4%–38.6%**。
- 在简单任务上，HiVLA 的平均成功率为 **96.0%**，接近去除技能输入后的消融版本的 **96.5%**，并高于 **H-RDT** 的 **90.5%**。
- HiVLA 的任务示例结果包括：*Move Stapler* 为 **60%**，H-RDT 为 **34%**；*Stamp Seal* 为 **76%**，H-RDT 为 **43%**；*Stack 3 Blocks* 为 **37%**，H-RDT 为 **20%**；*Click 3 Bells* 为 **98%**，H-RDT 为 **88%**。
- 摘录提到实验还包括真实世界评测，但提供的文本里没有给出真实世界的定量结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14125v1](http://arxiv.org/abs/2604.14125v1)
