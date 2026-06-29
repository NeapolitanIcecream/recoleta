---
source: arxiv
url: https://arxiv.org/abs/2605.01191v1
published_at: '2026-05-02T02:10:54'
authors:
- Wenhao Li
- Xiu Su
- Yichao Cao
- Hongyan Xu
- Xiaobo Xia
- Shan You
- Yi Chen
- Chang Xu
topics:
- vision-language-action
- generalist-robot-policy
- robot-error-recovery
- active-status-monitoring
- robot-data-scaling
- continual-learning
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery

## Summary
## 概要
Sentinel-VLA 在基于 PI0 的视觉-语言-动作机器人策略中加入了主动状态监测，使模型在操作过程中可以规划、执行、检测错误并恢复。论文声称，它的成功率高于 PI0、OpenVLA、ECoT、AHA+OpenVLA 和 OneTwoVLA，同时保持较低的动作延迟。

## 问题
- 现有 VLA 策略常把图像和指令输入直接映射为动作，因此在抓取失败、拿错物体或位姿出错后，仍可能继续执行。
- 逐步推理能改善决策，但对实时控制来说可能太慢；论文中的真实世界计时测试显示，ECoT 为 1528 ms/动作。
- 长时序机器人任务需要状态检查和恢复行为，因为小的执行误差会累积成任务失败。

## 方法
- Sentinel-VLA 在 PI0 上加入了一个状态监测专家。一个学习得到的 `[MONITOR]` 查询读取 VLM 的键值缓存，并预测四种状态之一：Initial、Normal、New-subtask 或 Error。
- 模型保留一个思维记忆，里面包括计划、当前子任务和错误反思。它在开始时规划，在 Normal 步骤中复用记忆，在子任务边界更新子任务，在检测到 Error 时生成恢复计划。
- 动作专家根据图像、任务指令、状态和思维记忆预测下一步机器人动作。训练时把动作的 flow matching 和思维与状态标签的交叉熵损失结合起来。
- EC-Gen 通过向成功轨迹中注入抓手、位姿和语义错误，加入恢复中间点，并标注状态和推理轨迹来生成训练数据。数据集包含 11,000 条轨迹、约 260 万个 transition 和 44 个 RLBench 任务。
- SECL 收集模型能力边界附近的成功 rollout，这个边界定义为成功率在 20% 到 80% 的设置。它训练一个带正交惩罚的 LoRA adapter，并用 alpha=0.9 将其合并到离线权重中。

## 结果
- 在 RLBench 已见任务上，Sentinel-VLA 的平均成功率为 63.5%，PI0 为 57.8%，OneTwoVLA 为 56.9%，ECoT 为 42.4%，OpenVLA 为 35.6%。
- 在 RLBench 干扰任务上，它的平均成功率为 54.7%，OneTwoVLA 为 48.4%，PI0 为 46.0%。
- 在 RLBench 未见任务上，它的平均成功率为 51.3%，OneTwoVLA 为 44.0%，PI0 为 42.0%，OpenVLA 为 30.7%。在 Wine at rack 任务上，论文报告为 28%，PI0 为 18%，OpenVLA 为 8%。
- 在 LIBERO-LONG 上，论文报告成功率为 90.7%，OneTwoVLA 为 87.8%，PI0 为 85.2%，OpenVLA 为 53.7%。
- 在真实世界的 Agilex Piper 任务中，它在 Stack cube、Pour water 和 Sweep rubbish 上的平均成功率为 60.0%，OneTwoVLA 为 52.0%，PI0 为 46.0%。这比 PI0 高 30.4%。
- 论文报告在 RTX4090 上的速度为 13 ms/动作，PI0 为 8.5 ms，OneTwoVLA 为 37 ms，OpenVLA 为 57 ms，AHA+OpenVLA 为 547 ms，ECoT 为 1528 ms。状态监测器在 RLBench 上的错误检测率为 97.4%，在真实世界错误集上的检测率为 90.6%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01191v1](https://arxiv.org/abs/2605.01191v1)
