---
source: arxiv
url: https://arxiv.org/abs/2605.08658v1
published_at: '2026-05-09T03:54:51'
authors:
- Shan Jiang
- Zijian Yi
- Chenguang Zhu
topics:
- code-generation
- inference-time-scaling
- program-sketching
- code-intelligence
- execution-based-selection
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching

## Summary
## 摘要
SketchVerify 是一种代码生成的推理时方法。它先针对不同的算法草图额外花计算，再采样具体实现。它最强的结论是：在难的 HumanEval+ 题目上，弱模型会有提升；但更强模型直接贪心解码，仍然可能更便宜，也更准确。

## 问题
- 小型代码模型在多次采样时常常重复同一个错误算法，所以额外生成的候选可能只是表面不同，并没有带来新的解题策略。
- 当实践者必须使用便宜或低延迟的模型层，并且希望在不换模型的情况下提高 pass@1 时，这个问题就很重要。
- 平面采样无法直接控制模型尝试了多少种不同算法。

## 方法
- 模型先为一个编程题列出 K 种不同的算法策略，例如哈希表、双指针排序，或动态规划。
- 对每种策略，模型写一个带有 ?? 空洞的部分 Python 程序草图，空洞可以是表达式、条件或边界，主控制流保持固定。
- 模型对每个草图填充 M 次，得到 K×M 个候选程序。
- 候选程序会经过编译并在生成的测试上运行；通过测试的候选会按执行指纹分组，然后从行为簇最大的组里选出最短程序。
- 这个方法的选择器和平面的 Semantic Voting 很接近，所以主要变化在候选生成，而不是新的投票规则。

## 结果
- 在 Gemini 3.1 Flash Lite 贪心解码失败的 19 道 HumanEval+ 题目上，Lite Sketch K=2,M=5 解出 11/19 题，即 58%，而平面 N=10 只解出 5/19，即 26%，在候选数量相同的情况下高出 32 个百分点。
- 在同一组难题上，Lite Sketch K=10,M=10 解出 15/19，即 79%，而平面 N=100 解出 10/19，即 53%，在候选数量相同的情况下高出 26 个百分点。
- Lite Sketch K=2,M=5 每题成本为 $3.8e-4，并且超过了平面 N=50；后者解出 9/19，即 47%，每题成本为 $1.1e-3。
- 在完整 HumanEval+ 上，Lite Sketch K=10,M=10 的 pass@1 达到 92.1%，高于 Lite greedy 的 85.4% 和平面 Semantic Voting 的 92.7%。
- 在一个包含 100 道题的 Lite 扩展扫描中，Sketch K=2,M=5 在约 11.6K tokens 下达到 91.0%，而平面 N=10 在约 8.0K tokens 下达到 85.0%；Sketch K=10,M=10 在约 88.4K tokens 下达到 93.0%，而平面 N=100 在约 62.0K tokens 下达到 89.0%。
- 跨层级结果削弱了部署层面的主张：在难题子集上，Flash greedy 解出 17/19，即 89%，每题成本为 $1.1e-4，超过了 Lite Sketch K=10,M=10 的 15/19，即 79%，以及每题成本 $2.8e-3。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08658v1](https://arxiv.org/abs/2605.08658v1)
