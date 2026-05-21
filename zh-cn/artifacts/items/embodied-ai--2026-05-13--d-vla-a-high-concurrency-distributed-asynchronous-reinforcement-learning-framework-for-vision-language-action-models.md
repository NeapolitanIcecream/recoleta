---
source: arxiv
url: https://arxiv.org/abs/2605.13276v2
published_at: '2026-05-13T09:54:31'
authors:
- Yucheng Guo
- Yongjian Guo
- Zhong Guan
- Wen Huang
- Haoran Sun
- Haodong Yue
- Xiaolong Xiang
- Shuai Di
- Zhen Sun
- Luqiao Wang
- Junwu Xiong
- Yicheng Gong
topics:
- vision-language-action
- robot-rl
- distributed-training
- robot-data-scaling
- embodied-ai
- sim2real
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# D-VLA: A High-Concurrency Distributed Asynchronous Reinforcement Learning Framework for Vision-Language-Action Models

## Summary
## 摘要
D-VLA 是一个面向大型视觉-语言-动作模型的分布式 RL 训练系统，用于减少模拟器和训练之间的资源争用。它报告了在 ManiSkill 上使用 π0.5 和 OpenVLA-OFT 时，比 RLinf-VLA 和 RL-VLA³ 基线更高的吞吐量。

## 问题
- 大型 VLA RL 运行会同时进行 GPU 负载很高的物理仿真、模型推理和训练，导致内存争用、通信延迟和硬件空闲。
- 基于 SFT 的机器人策略需要成本高昂的示范数据，并且常在新任务或状态分布变化时失败；在线 RL 可以增加探索，但现有系统处理大型 VLA 模型时速度较慢。
- 这一瓶颈很重要，因为低 rollout 吞吐量会限制机器人策略在训练期间可收集的交互数据量。

## 方法
- D-VLA 将流量拆分为用于 rollout 的高频数据平面，以及用于参数更新的较低频权重控制平面。
- 四线程 “Swimlane” 流水线并行运行采样、权重接收、梯度训练和权重分发。
- Rollout worker 将 PhysX 风格仿真与冻结的策略副本部署在同一位置，以减少观测传输开销；actor worker 在 FSDP 下计算 GRPO 优势和裁剪后的策略梯度。
- 系统使用 NCCL all-to-all 传输轨迹，并使用 CPU/Gloo 路径在后台广播权重，以避免 CUDA stream 与仿真发生争用。
- 双池 GPU 内存设计将模型内存与物理引擎临时内存分离，本地拓扑复制把高频采样-推理流量限制在各节点内部。

## 结果
- 在报告的单节点设置中，π0.5 上 D-VLA 在 1:1 放置时达到 147.0 steps/s，RLinf-co 为 127.24 steps/s，提升 22.25%；在 3:1 放置时达到 237.0 steps/s，相比 RLinf-co 提升 86.26%。
- 在 OpenVLA-OFT 上，D-VLA 报告 156.0 steps/s，RLinf-co 为 108.24 steps/s，RL-VLA³ 为 110.88 steps/s，相比 RLinf-co 提升 44.44%。
- 在 π0.5 的 16-GPU ManiSkill 表中，D-VLA 在 1:1 时达到 336.04 steps/s，在 3:1 时达到 376.00 steps/s；表中显示的最佳 RL-VLA³ 结果为 250.77 steps/s。
- 在 OpenVLA-OFT 的 16-GPU ManiSkill 表中，D-VLA 在 1:1 时达到 250.90 steps/s；RL-VLA³ 在 1:1 时达到 170.48 steps/s，RLinf-dis 在 1:1 时达到 107.23 steps/s。
- 在 16-GPU 1:1 表中，D-VLA 将 π0.5 step time 降至 488.32；相比之下，RL-VLA³ 1:1 为 669.80，RLinf-co 为 705.50。
- 摘录没有给出最终成功率的数值；它说 ManiSkill 成功率曲线显示，在训练吞吐量提高的同时，策略质量具有竞争力。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13276v2](https://arxiv.org/abs/2605.13276v2)
