---
source: arxiv
url: http://arxiv.org/abs/2603.01490v1
published_at: '2026-03-02T05:56:03'
authors:
- Cheng Yang
- Jianhao Jiao
- Lingyi Huang
- Jinqi Xiao
- Zhexiang Tang
- Yu Gong
- Yibiao Ying
- Yang Sui
- Jintian Lin
- Wen Huang
- Bo Yuan
topics:
- vision-language-action
- robot-inference
- attention-guidance
- action-guidance
- training-free
relevance_score: 0.36
run_id: materialize-outputs
language_code: zh-CN
---

# ATA: Bridging Implicit Reasoning with Attention-Guided and Action-Guided Inference for Vision-Language Action Models

## Summary
ATA 是一个针对视觉-语言-动作（VLA）机器人模型的免训练推理框架，通过注意力引导和动作引导两种隐式推理信号，在不增加标注和重训练的前提下提升动作预测。它的核心价值在于同时改善任务成功率、鲁棒性与推理效率。

## Problem
- 现有 VLA 方法虽能根据图像、语言指令和机器人状态预测动作，但在复杂操作中容易因早期感知或决策错误而发生级联失败。
- 显式推理增强方法通常依赖 CoT 式逐步标注、框/掩码等视觉监督，数据构建与重训练成本高，难以扩展。
- 这类方法还常带来更长的推理链路和更慢的在线执行，不利于真实机器人场景中的高效控制。

## Approach
- 提出 **ATA**：一个 **training-free, plug-and-play** 的推理时增强框架，不改模型参数，只在推理阶段改造视觉输入。
- **注意力引导**：从 VLA 中间层提取最后查询 token 对图像 patch 的注意力，聚合并归一化成掩码，把模型“已经关注”的关键区域凸显出来、弱化背景。
- **动作引导**：利用末端执行器位姿和相机参数，把机械臂当前朝向/运动意图投影为图像上的方向性 RoI，用软掩码强调动作可能相关的区域。
- **集成策略**：通常在首帧施加注意力引导，在任务早期施加动作引导，并可按一定频率周期性启用注意力引导，以较小额外开销稳定早期决策。
- 简单来说，方法先“看模型在看哪里”，再“看机器人准备往哪里动”，据此重加权图像，让原有 VLA 更容易在关键区域上做出正确动作。

## Results
- 在 **LIBERO** 环境中，ATA 使 **OpenVLA** 的性能提升 **5.2%**，使 **π0-fast** 提升 **2.0%**。
- 在 **RLBench** 环境中，ATA 使 **HybridVLA** 提升 **5.3%**。
- 在真实世界 **GR00T-N1.5** 三层积木堆叠任务中（积木尺寸仅 **3 cm × 3 cm × 3 cm**），复杂场景下性能提升 **最高 10%**。
- 论文宣称 ATA 在多个 SOTA VLA 上都能持续提升任务成功率与鲁棒性，同时保持甚至增强推理效率；其额外成本主要是在启用引导时增加一次前向过程。
- 评测覆盖模拟与真实环境，包括 **OpenVLA、π0-fast、HybridVLA、GR00T-N1.5**，说明方法具有较好的模型适配性与即插即用性。

## Link
- [http://arxiv.org/abs/2603.01490v1](http://arxiv.org/abs/2603.01490v1)
