---
source: arxiv
url: https://arxiv.org/abs/2606.18023v1
published_at: '2026-06-16T15:03:05'
authors:
- Jian Yang
- Shawn Guo
- Wei Zhang
- Tianyu Zheng
- Yaxin Du
- Haau-Sing Li
- Jiajun Wu
- Yue Song
- Yan Xing
- Qingsong Cai
- Zelong Huang
- Chuan Hao
- Ran Tao
- Xianglong Liu
- Wayne Xin Zhao
- Mingjie Tang
- Weifeng Lv
- Ming Zhou
- Bryan Dai
topics:
- code-intelligence
- software-foundation-models
- test-time-compute
- looped-transformers
- agentic-software-engineering
- kv-cache-efficiency
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling

## Summary
## 摘要
LoopCoder-v2 发现，用于代码任务的 7B Parallel Loop Transformer 在两轮循环时效果最好；增加到三轮或四轮会退化。两轮模型在代码和软件智能体基准上提升明显，三轮和四轮模型的表现下降。

## 问题
- Looped Transformers 可以在不增加参数的情况下加入潜在计算，但标准顺序循环的延迟和 KV-cache 内存会随循环次数增加。
- Parallel Loop Transformers 降低了这类成本，但仍需要选择循环次数，因为额外循环会通过跨循环偏移引入位置不匹配。
- 这对代码模型很重要，因为 SWE 类任务需要更强的内部计算，同时部署仍受延迟和内存限制。

## 方法
- 模型在各轮循环中复用同一个 Transformer 块，因此有效深度增加，而参数量保持不变。
- PLT 通过跨循环位置偏移降低循环成本：后续每一轮接收前一轮向后偏移一个 token 的结果；同时使用 shared-KV gated sliding-window attention，让后续循环复用第一轮的 KV cache，并与局部注意力混合。
- 作者从头训练 7B LoopCoder-v2 变体，训练数据为 18T 混合文本/代码 token，循环次数分别为 R=1、R=2、R=3 和 R=4；随后在 6M 样本上使用相同的监督式指令微调。
- 他们用 hidden-state movement、effective rank、fixed-point gap、attention KL、attention-head diversity、output-distribution shift，以及内在偏移成本 Ω 来诊断循环行为；Ω 衡量相邻 token 隐状态的不匹配。

## 结果
- 两轮模型将基准平均分从 R=1 基线的 38.0 提高到 46.5，在报告的评测套件上提升 8.5 分。
- 在 SWE-bench Verified 上，R=2 从 43.0 升至 64.4，比非循环基线高 21.4 分；R=3 降至 27.6，R=4 降至 22.4。
- 在 Multi-SWE 上，R=2 从 14.0 提高到 31.0，提升 17.0 分；R=3 得分 11.0，R=4 得分 9.3。
- R=2 在代码基准上的提升包括：HumanEval+ 从 81.1 到 84.1，MultiPL-E 从 69.5 到 73.9，BigCodeBench 从 40.1 到 46.1，LiveCodeBench 从 27.4 到 35.4。
- R=2 在工具和智能体基准上也有提升：Terminal-Bench v1 从 26.3 到 34.2，Terminal-Bench v2 从 11.2 到 21.0，BFCL 从 32.2 到 40.1；M2W 从 35.3 小幅降至 34.5。
- 论文称循环次数的影响是非单调的：第 2 轮给出主要的有效细化，后续循环的更新更小、振荡更强，表征多样性更低，同时偏移成本大致保持固定。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18023v1](https://arxiv.org/abs/2606.18023v1)
