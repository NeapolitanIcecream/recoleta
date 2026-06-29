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
## 概要
HiVLA 是一个分层机器人操作系统。它让视觉语言模型专注于规划和定位，把电流控制交给单独的扩散策略。论文称，这种拆分避免了端到端微调带来的推理能力下降，并提升了长时序、杂乱场景下的操作表现。

## 问题
- 端到端视觉语言动作模型在小规模、领域特定的机器人控制数据上微调时，常会丢失推理能力。
- 操作任务同时需要语义规划和精确的目标级感知，尤其是在杂乱场景和多步骤任务中。
- 现有的定位接口要么丢失全局空间上下文，要么丢失局部细节，这会影响精细控制。

## 方法
- HiVLA 把系统拆成两部分：高层 VLM 规划器和低层 Diffusion Transformer 动作专家。
- VLM 规划器接收任务、场景、动作历史和机器人状态，然后输出一个结构化计划，包含子任务指令、技能标签、目标物体和归一化边界框。
- 该边界框用于从原始 1920x1080 相机画面中裁出一个高分辨率局部图像块，这样控制器就能看到目标物体的细节外观。
- 动作专家在 DiT 策略中使用条件流匹配，并在每个块里使用级联交叉注意力，按顺序注入三类信号：全局场景特征、带位置信息的局部裁剪特征和子任务语言嵌入。
- 局部裁剪 token 使用与其在原图中坐标绑定的绝对位置嵌入，因此策略能同时保留物体细节和场景位置。

## 结果
- 在 RoboTwin 2.0 基准上，HiVLA 的总体平均成功率达到 **83.3%**，而 **H-RDT** 为 **70.6%**，**StarVLA** 为 **46.4%**，**pi_0** 为 **45.6%**，**pi_0.5** 为 **44.8%**。
- 论文称，这意味着在 RoboTwin 2.0 上，相比 **H-RDT** 绝对提升 **17.7** 个百分点，相比 **pi_0** 绝对提升 **42.7** 个百分点。
- 在困难任务上，HiVLA 的平均成功率为 **73.2%**，而 **H-RDT** 为 **54.6%**，**pi_0/pi_0.5/StarVLA** 为 **36.4%–38.6%**。
- 在容易任务上，HiVLA 的平均成功率为 **96.0%**，接近不输入技能信息的消融版本 **96.5%**，并高于 **H-RDT** 的 **90.5%**。
- HiVLA 的示例任务结果包括：*Move Stapler* 为 **60%**，H-RDT 为 **34%**；*Stamp Seal* 为 **76%**，H-RDT 为 **43%**；*Stack 3 Blocks* 为 **37%**，H-RDT 为 **20%**；*Click 3 Bells* 为 **98%**，H-RDT 为 **88%**。
- 摘要提到实验也包含真实世界评测，但提供的文本里没有给出真实世界的定量结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14125v1](http://arxiv.org/abs/2604.14125v1)
