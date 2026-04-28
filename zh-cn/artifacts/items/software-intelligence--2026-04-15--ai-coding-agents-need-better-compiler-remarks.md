---
source: arxiv
url: http://arxiv.org/abs/2604.13927v1
published_at: '2026-04-15T14:35:07'
authors:
- Akash Deo
- Simone Campanoni
- Tommy McMichen
topics:
- compiler-feedback
- code-intelligence
- ai-coding-agents
- auto-vectorization
- program-optimization
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# AI Coding Agents Need Better Compiler Remarks

## Summary
## 摘要
这篇论文认为，AI 编码代理在编译器引导的性能重构上失败，原因是编译器提示语过于含糊，而不是模型能力太弱。在 TSVC 上，更精确的优化反馈会提高向量化成功率，也能让 7B 模型有效得多。

## 问题
- AI 代理会尝试重构 C/C++ 代码，让编译器能够自动向量化，但编译器反馈通常缺少结构，而且表述含糊。
- 含糊的提示语只会告诉代理优化失败了，却不会清楚说明导致失败的数据依赖关系或代码位置。
- 这很重要，因为低质量反馈会导致优化成功率偏低，也会在代理猜错时把它推向破坏语义的修改。

## 方法
- 作者测试了一种由编译器引导的编码流程：让 Qwen2.5-Coder 7B 接收源代码以及编译器警告、错误和优化提示语，然后重写代码以启用自动向量化。
- 他们在 151 个 TSVC 循环上进行评估，使用 Clang 21.1.8 和 Intel 2025.3，在有无提示语两种条件下，测试温度为 0.2、0.8 和 1.2，每个循环运行 100 次试验。
- 成功与否通过编译器优化记录中的向量化结果来检查，并通过差分测试捕捉语义破坏。
- 为了单独观察反馈质量的影响，他们使用了单轮设置，而不是更长的迭代式代理循环。
- 他们还把一些含糊的提示语替换成手写的精确提示语，明确给出具体的依赖关系和源代码位置，并附上明确的修复建议。

## 结果
- 没有提示语时，成功率很低：Clang 在 T=0.2、0.8 和 1.2 时分别达到 0.20%、0.80% 和 1.45%；Intel 分别达到 1.10%、2.38% 和 3.67%。
- 加入提示语后，成功率提升到：Clang 分别为 0.64%、2.68% 和 3.93%，Intel 分别为 4.59%、6.95% 和 7.83%。在 T=0.8 时，提示语让 Clang 从 0.80% 提升到 2.68%，让 Intel 从 2.38% 提升到 6.95%，约为 3.3 倍和 2.9 倍。
- 现有的一些精确提示语类型帮助很大：Intel Output Dependence 在 T=0.8 时增加 +26.00 个百分点，Anti Dependence 增加 +15.50，Multiple Exits 在 T=0.2 时增加 +22.33。
- 一些含糊的提示语作用很弱，甚至有害。Clang ArrayBounds 在 T=0.8 和 T=1.2 时分别下降 -2.00 和 -3.00；Libcall/Instr 在 T=0.8 时下降 -2.50。论文还报告，在案例分析中，Clang NonReductionValue 经常引发破坏语义的幻觉式修改。
- 手写的精确依赖提示语带来最大提升：ReadAfterWrite 在 T=0.8 时增加 +50.00，在 T=1.2 时增加 +59.00；WriteAfterRead 在 T=0.2、0.8 和 1.2 时分别增加 +45.00、+40.80 和 +35.20。
- WriteAfterWrite 的提升较小，在 T=0.8 时最高为 +9.00，这说明仅有依赖标签有时还不够，可能还需要更多分析信息。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13927v1](http://arxiv.org/abs/2604.13927v1)
