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
SketchVerify 是一种用于代码生成的推理时方法：它先把额外计算用在不同的算法草图上，再对实现进行采样。它最强的主张是在困难 HumanEval+ 问题上提升弱模型表现；更强模型的贪心解码仍可能成本更低、准确率更高。

## 问题
- 小型代码模型在多次采样时常会重复同一个错误算法，因此额外候选可能只带来表面变化，而不会带来新的解题策略。
- 当实践者必须使用便宜或低延迟的模型档位，并且想在不切换模型的情况下提高 pass@1 时，这一点会影响结果。
- 平铺采样不能直接控制模型尝试多少种不同算法。

## 方法
- 模型先为一个编程问题列出 K 种不同的算法策略，例如哈希表、排序加双指针，或动态规划。
- 对每种策略，模型编写一个带有 ?? 空洞的 Python 部分程序草图，用于表达式、条件或边界，同时固定主控制流。
- 模型将每个草图填充 M 次，生成 K×M 个候选程序。
- 候选程序会被编译并在生成的测试上运行；通过测试的候选按执行指纹分组，并选择最大行为簇中最短的程序。
- 该方法让选择器接近平铺 Semantic Voting，因此主要变化是候选生成方式，而不是新的投票规则。

## 结果
- 在 Gemini 3.1 Flash Lite 贪心解码失败的 19 个 HumanEval+ 问题上，Lite Sketch K=2,M=5 解决了 11/19 个问题，即 58%；平铺 N=10 解决了 5/19 个问题，即 26%；在候选数量相同的情况下提升 +32 pp。
- 在同一个困难子集上，Lite Sketch K=10,M=10 解决了 15/19 个问题，即 79%；平铺 N=100 解决了 10/19 个问题，即 53%；在候选数量相同的情况下提升 +26 pp。
- Lite Sketch K=2,M=5 每题成本为 $3.8e-4，并超过了平铺 N=50；后者解决了 9/19 个问题，即 47%，每题成本为 $1.1e-3。
- 在完整 HumanEval+ 上，Lite Sketch K=10,M=10 达到 92.1% pass@1，Lite 贪心解码为 85.4%，平铺 Semantic Voting 为 92.7%。
- 在 100 题 Lite 扩展扫描中，Sketch K=2,M=5 用约 11.6K tokens 达到 91.0%，平铺 N=10 用约 8.0K tokens 达到 85.0%；Sketch K=10,M=10 用约 88.4K tokens 达到 93.0%，平铺 N=100 用约 62.0K tokens 达到 89.0%。
- 跨档位结果削弱了部署主张：在困难子集上，Flash 贪心解码解决了 17/19 个问题，即 89%，每题成本为 $1.1e-4，超过 Lite Sketch K=10,M=10 的 15/19，即 79%，后者每题成本为 $2.8e-3。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08658v1](https://arxiv.org/abs/2605.08658v1)
