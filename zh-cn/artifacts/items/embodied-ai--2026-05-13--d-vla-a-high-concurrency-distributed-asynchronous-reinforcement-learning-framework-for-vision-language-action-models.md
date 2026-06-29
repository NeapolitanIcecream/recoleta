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
D-VLA 是一个面向大型 Vision-Language-Action 模型的分布式 RL 训练系统，用来减少模拟器与训练之间的争用。它在 ManiSkill 上用 π0.5 和 OpenVLA-OFT 的吞吐量高于 RLinf-VLA 和 RL-VLA³ 基线。

## 问题
- 大型 VLA 的 RL 运行把 GPU 密集的物理仿真、模型推理和训练放在一起，导致显存争用、通信延迟和硬件空闲。
- 基于 SFT 的机器人策略需要昂贵的示范数据，在新任务或状态分布变化时常常失效；在线 RL 可以加入探索，但现有系统对大型 VLA 模型来说速度太慢。
- 这个瓶颈很关键，因为 rollout 吞吐量低会限制机器人策略在训练中能收集多少交互数据。

## 方法
- D-VLA 将流量拆成高频数据平面，用于 rollout，和低频权重控制平面，用于参数更新。
- 一个四线程的 “Swimlane” 管线把采样、权重接收、梯度训练和权重分发并行运行。
- rollout worker 将 PhysX 风格仿真与冻结的策略副本放在一起，减少观测传输开销；actor worker 在 FSDP 下计算 GRPO 优势和裁剪策略梯度。
- 该系统用 NCCL all-to-all 传输轨迹，并用 CPU/Gloo 路径在后台广播权重，避免 CUDA stream 与仿真争用。
- 双池 GPU 显存设计把模型显存和物理引擎临时显存分开，本地拓扑复制把高频采样-推理流量限制在每个节点内部。

## 结果
- 在报告的单节点设置中，D-VLA 在 π0.5 上以 1:1 放置达到 147.0 steps/s，而 RLinf-co 为 127.24 steps/s，提升 22.25%；在 3:1 放置下达到 237.0 steps/s，比 RLinf-co 提升 86.26%。
- 在 OpenVLA-OFT 上，D-VLA 报告 156.0 steps/s，RLinf-co 为 108.24 steps/s，RL-VLA³ 为 110.88 steps/s；相比 RLinf-co 提升 44.44%。
- 在 16-GPU ManiSkill 的 π0.5 表中，D-VLA 在 1:1 下达到 336.04 steps/s，在 3:1 下达到 376.00 steps/s；图中给出的最佳 RL-VLA³ 结果是 250.77 steps/s。
- 在 16-GPU ManiSkill 的 OpenVLA-OFT 表中，D-VLA 在 1:1 下达到 250.90 steps/s；RL-VLA³ 在 1:1 下达到 170.48 steps/s，RLinf-dis 在 1:1 下达到 107.23 steps/s。
- D-VLA 将 π0.5 的 step time 在 16-GPU 1:1 表中降到 488.32，而 RL-VLA³ 1:1 为 669.80，RLinf-co 为 705.50。
- 摘录没有给出最终成功率的数值；它只说 ManiSkill 的成功率曲线显示策略质量有竞争力，同时训练吞吐量上升。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13276v2](https://arxiv.org/abs/2605.13276v2)
