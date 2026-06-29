---
source: arxiv
url: https://arxiv.org/abs/2606.27268v1
published_at: '2026-06-25T16:50:21'
authors:
- Wen Ye
- Peiyan Li
- Tingyu Yuan
- Yuan Xu
- Xiangnan Wu
- Chaoyang Zhao
- Jing Liu
- Nianfeng Liu
- Yan Huang
- Liang Wang
topics:
- vision-language-action
- robot-test-time-scaling
- robot-manipulation
- generalist-robot-policy
- robot-data-scaling
- embodied-reasoning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation

## Summary
## 摘要
E-TTS 通过在推理时搜索来增强机器人操作策略：它采样多个推理-动作对，用视觉语言验证器检查，并用带历史上下文的反馈细化失败样本。它无需重新训练基础策略，也无需收集新的专家机器人演示，就能提升多个 VLA 策略的表现。

## 问题
- 现有具身测试时扩展方法主要重新采样动作，因此可能选出与模型高层推理不匹配的动作。
- 机器人操作需要过去的上下文，因为每个动作都依赖先前的观测、推理和已执行运动。
- 额外机器人数据成本高，因此在推理时提高任务成功率，对物体重新摆放等可容忍延迟的任务有价值。

## 方法
- 在每个时间步，E-TTS 采样 M 个推理候选，并为每个推理候选采样 N 个动作候选，然后把每个推理-动作对作为一个候选。
- 历史缓冲区存储近期观测和已选择的推理-动作对，验证器在为新候选评分时使用这些上下文。
- 零样本 Qwen2.5-VL-7B 推理验证器对文本、多模态或空间推理的任务匹配度和落地性评分。
- LLaVA-7B 动作验证器在来自 SimplerEnv 和 LIBERO 的 9 万组成对成功与失败演示上训练，使用修改后的 Bradley-Terry 偏好损失为动作可行性评分。
- 系统将归一化后的推理分数和动作分数相乘，使用带分数阈值的 epsilon-greedy 选择规则，并在一批候选被拒绝时要求验证器生成反馈。

## 结果
- 在 4 个基准、6 个环境、3 种机器人形态和 4 个基础 VLA 模型上，E-TTS 报告的最高模拟成功率提升为 33.14 个百分点，平均提升为 13.52 个百分点。
- 在真实世界实验中，论文称在不重新训练基础策略的情况下，最高提升 26.62 个百分点。
- 在使用 E-CoT 的 SimplerEnv WidowX Visual Matching 上，平均成功率从 6.67% 升至 39.81%，提升 33.14 个百分点。
- 在同一 SimplerEnv WidowX 设置中，E-TTS 的平均成功率高于 E-CoT + naive TTS 的 23.61% 和 E-CoT + RoboMonkey 的 26.38%。
- SimplerEnv WidowX 上的消融实验显示，移除组件会降低平均成功率：无反馈为 25.04%，无推理扩展为 26.39%，无动作扩展为 30.56%，无联合评分为 31.13%，无历史缓冲区为 31.94%，无 epsilon-greedy 为 36.11%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27268v1](https://arxiv.org/abs/2606.27268v1)
