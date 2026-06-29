---
source: arxiv
url: http://arxiv.org/abs/2603.29292v1
published_at: '2026-03-31T05:55:17'
authors:
- Huan Zhang
- Wei Cheng
- Wei Hu
topics:
- code-generation
- self-improvement
- preference-optimization
- uncertainty-estimation
- code-llms
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus

## Summary
## 摘要
ConSelf 是一种用于代码大语言模型的自我改进方法，在没有教师模型、参考解或测试预言机的情况下训练。它利用测试输入上的执行行为来挑选可学习的问题，并在微调时对噪声较大的自生成偏好进行加权。

## 问题
- 这篇论文关注的是这样一种代码生成场景：只有题目描述和测试输入，而没有参考解和测试预言机。
- 这很重要，因为许多现有的代码改进方法依赖昂贵的教师模型或可靠的预言机，而这些在真实软件场景中很难获得。
- 这种情况下，自训练并不稳定：对于难题，模型可能生成很多彼此不同但都错误的程序，把这些噪声用于训练会浪费算力，甚至拖累性能。

## 方法
- ConSelf 先通过 **观测引导采样** 为每道题采样多个候选程序：模型先写出不同的文本观察或计划，再据此生成代码。
- 它通过在可用测试输入上执行候选程序、按相同执行轨迹对程序聚类，并对这些行为簇计算香农熵，来得到每道题的 **代码语义熵**。
- 语义熵为零或归一化熵过高的题目会被过滤掉。剩下的题目组成一个更可能包含有效学习信号的课程。
- 对于保留下来的每道题，方法会根据某个候选的输出在测试输入上与其他候选一致的频率，为每个候选分配一个 **行为一致性分数**。
- 然后用 **基于一致性的 DPO（Con-DPO）** 进行微调：把一致性最高的候选与较低一致性的候选配对，并按胜出者的一致性分数给每个 DPO 损失项加权，让噪声较大的偏好对权重更低。

## 结果
- 论文报告，在标准代码生成基准上，相比基础模型取得了 **2.73% 到 3.95% 的相对提升**。
- 摘要和引言都说，ConSelf 在多个基准和骨干 LLM 上 **显著优于基线方法**，但这段摘录没有给出完整基准名称、绝对分数或各基线的具体数值。
- 论文声称，代码语义熵比 **token 级熵** 和 **负对数似然** 这类内部置信度指标，更能反映问题的可学习性。
- 论文还认为课程设计很关键：在没有预言机的设置中，过滤掉零熵和高熵问题能提升自我改进的质量。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29292v1](http://arxiv.org/abs/2603.29292v1)
