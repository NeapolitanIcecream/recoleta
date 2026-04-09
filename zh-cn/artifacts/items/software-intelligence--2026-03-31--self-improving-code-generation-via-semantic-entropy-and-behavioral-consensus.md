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
ConSelf 是一种用于代码大语言模型的自我改进方法，训练时不需要教师模型、参考解答或测试预言机。它利用测试输入上的执行行为来选择更可学的问题，并在微调时为带噪声的自生成偏好样本分配权重。

## 问题
- 论文研究的代码生成场景中，只有题目描述和测试输入可用，而参考解答和测试预言机缺失。
- 这一点很重要，因为许多现有的代码改进方法依赖昂贵的教师模型或可靠的预言机，而这些资源在真实软件环境中往往很难获得。
- 在这种条件下，自训练并不稳定：面对困难问题，模型可能生成大量彼此不同但都错误的程序，用这些噪声数据训练会浪费算力，或拉低性能。

## 方法
- ConSelf 首先通过 **observation-guided sampling** 为每个问题采样大量候选程序：模型先写出多样化的文本观察或计划，再在此基础上生成代码。
- 它通过执行候选程序在现有测试输入上的结果，为每个问题计算 **code semantic entropy**：将执行轨迹完全相同的程序聚类，并计算这些行为簇上的香农熵。
- 熵为零或归一化熵过高的问题会被过滤掉。剩余问题构成一个课程，更可能包含有用的学习信号。
- 对于每个保留下来的问题，该方法会根据候选程序在各个测试输入上的输出与其他候选程序一致的频率，为每个候选分配一个 **behavioral consensus score**。
- 然后，它使用 **consensus-driven DPO (Con-DPO)** 进行微调：将共识分数最高的候选与共识更低的候选配对，并用获胜者的共识分数对每个 DPO 损失项加权，从而降低带噪偏好对训练的影响。

## 结果
- 论文报告称，在标准代码生成基准上，相比基础模型取得了 **2.73% 到 3.95% 的相对提升**。
- 摘要和引言称，ConSelf 在多个基准和多种骨干 LLM 上都 **显著优于基线方法**，但给出的摘录没有提供完整的基准名称、绝对分数或各基线的具体数值。
- 论文称，code semantic entropy 比 **token-level entropy** 和 **negative log-likelihood** 等内部置信度指标更适合判断一个问题是否可学。
- 论文还称，课程设计很关键：在无预言机设定下，过滤掉零熵和高熵问题可以提升自我改进的效果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29292v1](http://arxiv.org/abs/2603.29292v1)
