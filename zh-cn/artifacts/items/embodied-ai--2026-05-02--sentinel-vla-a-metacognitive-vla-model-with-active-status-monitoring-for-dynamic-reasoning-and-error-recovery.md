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
## 摘要
Sentinel-VLA 在基于 PI0 的视觉-语言-动作机器人策略中加入主动状态监控，使其能在操作任务中规划、执行、检测错误并恢复。论文称，在保持较低动作延迟的同时，它的成功率高于 PI0、OpenVLA、ECoT、AHA+OpenVLA 和 OneTwoVLA。

## 问题
- 当前 VLA 策略通常把图像和指令输入直接映射到动作，因此在抓取失败、操作错误物体或姿态出错后仍可能继续执行。
- 逐步推理可以改善决策，但对实时控制可能太慢；在论文的真实世界计时测试中，ECoT 报告为 1528 ms/action。
- 长时程机器人任务需要状态检查和恢复行为，因为小的执行错误可能累积成任务失败。

## 方法
- Sentinel-VLA 在 PI0 中加入 Status Monitor expert。一个学习到的 `[MONITOR]` 查询读取 VLM 键值缓存，并预测四种状态之一：Initial、Normal、New-subtask 或 Error。
- 模型维护一份思维记忆，其中包含计划、当前子任务和错误反思。它在开始时规划，在 Normal 步骤中复用记忆，在子任务边界更新子任务，并在检测到 Error 时生成恢复计划。
- action expert 根据图像、任务指令、状态和思维记忆预测下一个机器人动作。训练将用于动作的 flow matching 与用于思维和状态标签的交叉熵损失结合起来。
- EC-Gen 通过向成功轨迹中注入夹爪、姿态和语义错误来创建训练数据，添加恢复路点，并标注状态和推理轨迹。该数据集包含 11,000 条轨迹、约 260 万个 transitions，以及 44 个 RLBench 任务。
- SECL 收集接近模型能力边界的成功 rollout，能力边界定义为成功率为 20-80% 的设置。它使用正交惩罚训练 LoRA adapter，并以 alpha=0.9 将其合并到离线权重中。

## 结果
- 在 RLBench 已见任务上，Sentinel-VLA 达到 63.5% 的平均成功率，相比之下 PI0 为 57.8%，OneTwoVLA 为 56.9%，ECoT 为 42.4%，OpenVLA 为 35.6%。
- 在 RLBench 扰动任务上，它达到 54.7% 的平均成功率，相比之下 OneTwoVLA 为 48.4%，PI0 为 46.0%。
- 在 RLBench 未见任务上，它达到 51.3% 的平均成功率，相比之下 OneTwoVLA 为 44.0%，PI0 为 42.0%，OpenVLA 为 30.7%。在 Wine at rack 上，论文报告其为 28%，PI0 为 18%，OpenVLA 为 8%。
- 在 LIBERO-LONG 上，论文报告成功率为 90.7%，相比之下 OneTwoVLA 为 87.8%，PI0 为 85.2%，OpenVLA 为 53.7%。
- 在真实世界 Agilex Piper 任务中，它在 Stack cube、Pour water 和 Sweep rubbish 上达到 60.0% 的平均成功率，相比之下 OneTwoVLA 为 52.0%，PI0 为 46.0%。这相对 PI0 提升 30.4%。
- 论文报告在 RTX4090 上为 13 ms/action，相比之下 PI0 为 8.5 ms，OneTwoVLA 为 37 ms，OpenVLA 为 57 ms，AHA+OpenVLA 为 547 ms，ECoT 为 1528 ms。状态监控器在 RLBench 上的错误检测率为 97.4%，在真实世界错误集上为 90.6%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01191v1](https://arxiv.org/abs/2605.01191v1)
