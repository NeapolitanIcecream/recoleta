---
source: arxiv
url: http://arxiv.org/abs/2603.03406v1
published_at: '2026-03-03T16:57:14'
authors:
- Jan Miller
topics:
- code-synthesis
- multi-llm
- code-review
- planning-vs-review
- benchmarking
relevance_score: 0.03
run_id: materialize-outputs
---

# Review Beats Planning: Dual-Model Interaction Patterns for Code Synthesis

## Summary
本文研究两个语言模型如何协作做代码生成，核心结论是“先规划再写代码”并不好，反而“先写代码再审查修复”显著更强。作者用两個量化开源模型在低成本硬件上取得了接近甚至超过部分专有模型的代码基准成绩。

## Problem
- 论文要解决的问题是：**两个不同长处的语言模型应如何交互，才能比单模型生成更好的代码**。
- 这很重要，因为很多实际部署只能使用较小、量化、可本地运行的模型，单模型性能往往不够强，需要通过组合提升质量。
- 作者质疑常见假设：让“推理模型先规划、代码模型后实现”是否真的有效；实验显示它不仅无益，反而会把原本能做对的题做错。

## Approach
- 核心方法是 **review-then-fix**：先让代码专长模型自由生成解答，再让推理模型像代码审查员一样对照题目找 bug，最后由代码模型根据具体反馈修复。
- 最简单地说：**不要先教它怎么写，而是在它写完后指出哪里错了**；具体错误反馈比抽象规划更容易被正确执行。
- 作者对比了三类模式：raw-coder 单模型、plan-then-code（先规划后写）、review-then-fix（先写后审），并额外测试带可见测试重试的版本和“双模型独立生成再交叉验证”的 adversarial dual-generation。
- 所有实验使用同一组模型与硬件：Qwen2.5-Coder-14B-Instruct + Qwen3-32B，均为 4-bit AWQ，部署在 2×A10G 上，成本约 **$2/hr**。
- 作者还提出一个关键调节变量：**specification richness**。如果题目说明更丰富（类型、docstring、示例、边界条件更多），审查模型更容易准确发现 bug，因此审查机制收益更大。

## Results
- 在 **HumanEval+ (164题)** 上，raw-coder 为 **78.0% pass@1**；**plan-then-code 仅 75.6%**，比基线**下降 2.4 个百分点**；而 **review-then-fix 87.8%**，比基线**提升 9.8 个百分点**。
- 加上基于可见 docstring 测试的 retry 后，**review-then-fix (+retry)** 达到 **90.2% HumanEval+**，比 raw-coder **+12.2pp**；也高于文中列出的 **GPT-4o 87.2%** 和 **O1 Preview 89.0%**。
- 在 **HumanEval** 上，对应结果为：raw-coder **81.1%**、plan-then-code **80.5%**、review-then-fix **89.6%**、review-then-fix (+retry) **93.3%**、adversarial debate **91.5%**。
- 跨基准验证显示审查收益强烈依赖题目说明质量：在说明丰富的 **HumanEval+** 上，review-then-fix 相对基线提升 **+9.8pp (78.0%→87.8%)**；在说明简略的 **MBPP+ (378题)** 上仅提升 **+2.3pp (67.5%→69.8%)**，即约 **4× 更小**，但仍为净正收益。
- “规格增强”没有真正补上这个差距：HumanEval+ 上 enriched review 仅比普通 review **+0.6pp (87.8%→88.4%)**；MBPP+ 上**无提升**（**69.8% vs 69.8%**）。
- 失败模式分析显示，plan-then-code 在 164 题中带来 **15 个回归**、仅 **14 个改进**；主要错误包括 **缺失 import 7 例**、**算法实现偏差 5 例**、**过度工程 2 例**、**变量名“纠正”导致签名错误 1 例**。

## Link
- [http://arxiv.org/abs/2603.03406v1](http://arxiv.org/abs/2603.03406v1)
