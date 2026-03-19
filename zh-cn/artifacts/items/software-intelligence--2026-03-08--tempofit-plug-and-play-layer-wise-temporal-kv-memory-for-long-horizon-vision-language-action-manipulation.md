---
source: arxiv
url: http://arxiv.org/abs/2603.07647v1
published_at: '2026-03-08T14:17:25'
authors:
- Jun Sun
- Boyu Yang
- Jiahao Zhang
- Ning Ma
- Chencheng Wu
- Siqing Zhang
- Yiou Huang
- Qiufeng Wang
- Shan Liang
- Yaran Chen
topics:
- vision-language-action
- temporal-memory
- kv-cache
- long-horizon-manipulation
- training-free
- robotics
relevance_score: 0.56
run_id: materialize-outputs
language_code: zh-CN
---

# TempoFit: Plug-and-Play Layer-Wise Temporal KV Memory for Long-Horizon Vision-Language-Action Manipulation

## Summary
TempoFit针对视觉-语言-动作（VLA）机器人策略在长时程操作中“只看当前帧、没有记忆”的问题，提出一种无需训练的即插即用时间记忆机制。它直接复用冻结模型内部各层的注意力KV状态作为历史记忆，在不增加输入上下文长度的情况下提升长程操控稳定性。

## Problem
- 现有预训练VLA虽然单步操作强，但推理通常是**memoryless**，在遮挡、状态混淆、动作后变化细微等非马尔可夫长程任务中容易重复动作、漏步骤或阶段衔接失败。
- 常见做法是堆叠历史帧，但这会显著增加视觉token数量和注意力计算开销，还引入大量近重复像素，导致延迟更高、信息冗余。
- 另一类方法通过额外 temporal module / memory interface 注入历史，但通常需要训练或微调，且可能破坏原始单帧推理图，难以直接改造冻结的强基座VLA。

## Approach
- 核心思想：把Transformer前缀注意力中的**keys/values (K/V)** 当作模型原生的“可寻址运行时状态”，跨时间步缓存并复用，而不是存原始图像或学习新记忆模块。
- 在选定的**中间层**维护分层FIFO KV缓存，只保存prefix阶段的K/V，不增加任何输入token，因此基本保持原模型的推理结构与动作头不变。
- 用当前时刻的K去和历史K做**K-to-K retrieval**，即在模型原本的键空间里做相似度匹配，从历史中读出相关的K/V上下文；这是参数无关、训练无关的检索方式。
- 引入**Frame-Gap Temporal Bias (FGTB)**，对更久远的帧施加固定的时间衰减偏置，让检索结果“以当前为主、历史为辅”，减少陈旧上下文干扰。
- 将检索到的历史K/V通过**pre-attention residual loading**残差注入当前K/V，并做**norm-preserving rescaling**，尽量避免冻结权重下的分布漂移与注意力失稳。

## Results
- 在**LIBERO-Long**上，TempoFit将**π0.5**从**92.6%**平均成功率提升到**96.6%**，即**+4.0 个百分点**；在同一表中超过**MemoryVLA 93.4%**，也略高于**HiF-VLA 96.4%**。
- 在**LIBERO-Long**上，TempoFit将**QwenGR00T**从**90.8%**提升到**94.4%**，即**+3.6 个百分点**。
- 在具体困难子任务“**Put both pots on stove**”上，**π0.5**从**58.0%**提升到**84.0%**，提升**+26.0 个百分点**，表明其对跨阶段时序关联尤其有效。
- 在**CALVIN D-D**上，平均任务长度从**3.78**提升到**3.84**；分步指标中第5步从**59.8**提升到**62.3**，说明后续指令执行更稳。
- 在**CALVIN ABC-D**上，平均任务长度从**3.83**提升到**3.87**；第5步从**61.4**提升到**62.0**。
- 论文还声称该方法具有**接近实时/可忽略的推理开销**并可迁移到真实机器人长程任务，但给定摘录中未提供更详细的实时延迟数值。

## Link
- [http://arxiv.org/abs/2603.07647v1](http://arxiv.org/abs/2603.07647v1)
