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
- inference-time-guidance
- implicit-reasoning
- robot-manipulation
- sim-to-real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# ATA: Bridging Implicit Reasoning with Attention-Guided and Action-Guided Inference for Vision-Language Action Models

## Summary
ATA 是一个用于视觉-语言-动作（VLA）模型的免训练推理框架，通过注意力引导和动作引导两种隐式推理信号，在不增加标注或重新训练的前提下提升机器人控制表现。它的核心卖点是即插即用、计算开销小，并同时改善成功率、鲁棒性与部分场景下的推理效率。

## Problem
- 现有给 VLA 加“推理”能力的方法通常依赖 CoT 式逐步标注、框/掩码等视觉标注，数据采集和标注成本高，难扩展。
- 许多方法还需要额外训练或重训练大模型，耗费大量算力，并且会拉长推理序列，降低实时性。
- 纯 VLA 直接从观测到动作，在复杂操作中容易因早期误判产生级联错误，影响任务成功率与鲁棒性。

## Approach
- ATA 是**training-free** 的推理时增强方法：先用原模型做一次前向，提取隐含线索，再把图像做“重点突出、背景压低”的处理后重新送入同一个 VLA。
- **Attention-guided**：从模型中间层提取最后 query token 对图像 patch 的注意力，聚合并归一化为掩码，突出模型自己认为与任务相关的视觉区域。
- **Action-guided**：利用机械臂末端执行器位姿和相机参数，把“可能的运动方向”投影到图像上，构造一个扇形/锥形软 RoI，强调动作意图相关区域。
- 两种信号按调度结合：通常首帧使用注意力引导，早期步骤使用动作引导，以减少早期错误在长预测 horizon 中传播。
- 该方法不需要 CoT、框、mask 或额外监督，且可插接到 OpenVLA、pi0-fast、HybridVLA、GR00T-N1.5 等不同 VLA 模型上。

## Results
- 在 **LIBERO** 环境中，ATA 使 **OpenVLA** 的性能提升 **5.2%**，使 **pi0-fast** 提升 **2.0%**。
- 在 **RLBench** 环境中，ATA 使 **HybridVLA** 提升 **5.3%**。
- 在真实世界 **GR00T-N1.5** 三层积木堆叠任务中（积木尺寸 **3cm × 3cm × 3cm**），复杂场景下性能提升最高 **10%**。
- 论文声称 ATA 在提升任务成功率和鲁棒性的同时，能够保持甚至提升推理效率；方法仅在施加引导时引入一次额外前向，但摘要未给出统一的延迟/吞吐数值对比。
- 实验覆盖多种主流 VLA：**OpenVLA、pi0-fast、HybridVLA、GR00T-N1.5**，并横跨仿真与真实机器人场景，强调其即插即用泛化性。

## Link
- [http://arxiv.org/abs/2603.01490v1](http://arxiv.org/abs/2603.01490v1)
