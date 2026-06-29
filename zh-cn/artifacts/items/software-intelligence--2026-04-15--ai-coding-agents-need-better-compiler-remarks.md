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
## 总结
这篇论文认为，AI 编码代理在编译器指导的性能重构中失败，原因在于编译器备注太模糊，而不是模型太弱。在 TSVC 上，更精确的优化反馈提高了向量化成功率，也能让 7B 模型表现好很多。

## 问题
- AI 代理尝试重构 C/C++ 代码，让编译器可以自动向量化，但编译器反馈常常缺少结构，也不够清楚。
- 含糊的备注只会告诉代理优化失败，却没有说明造成失败的数据依赖关系或具体代码位置。
- 这很重要，因为反馈差会让优化成功率很低，也会在代理猜错时引发破坏语义的编辑。

## 方法
- 作者测试了一种编译器指导的编码流程：Qwen2.5-Coder 7B 接收源代码以及编译器警告、错误和优化备注，然后改写代码，让代码可以自动向量化。
- 他们在 151 个 TSVC 循环上评估，使用 Clang 21.1.8 和 Intel 2025.3，在有备注和没有备注两种情况下，温度分别设为 0.2、0.8 和 1.2，每个循环做 100 次试验。
- 结果通过编译器的向量化优化记录来检查，也通过差分测试来捕捉语义破坏。
- 为了隔离反馈质量的影响，他们使用单轮设置，而不是更长的迭代代理循环。
- 他们还把一些含糊备注替换成手写的精确备注，明确暴露精确的依赖关系和源位置，并给出具体修复建议。

## 结果
- 没有备注时，成功率很低：Clang 在 T=0.2、0.8 和 1.2 时分别是 0.20%、0.80% 和 1.45%；Intel 分别是 1.10%、2.38% 和 3.67%。
- 有备注时，Clang 提高到 0.64%、2.68% 和 3.93%，Intel 提高到 4.59%、6.95% 和 7.83%。在 T=0.8 时，备注把 Clang 从 0.80% 提高到 2.68%，把 Intel 从 2.38% 提高到 6.95%，大约是 3.3 倍和 2.9 倍。
- 现有的精确备注类型能带来很大帮助：Intel Output Dependence 在 T=0.8 时增加 26.00 个百分点，Anti Dependence 增加 15.50，Multiple Exits 在 T=0.2 时增加 22.33。
- 一些含糊备注效果弱，甚至有害。Clang ArrayBounds 在 T=0.8 时下降 2.00，在 T=1.2 时下降 3.00；Libcall/Instr 在 T=0.8 时下降 2.50。论文还报告说，Clang NonReductionValue 在案例研究中经常触发破坏语义的幻觉。
- 手写的精确依赖备注带来最大增益：ReadAfterWrite 在 T=0.8 时增加 50.00，在 T=1.2 时增加 59.00；WriteAfterRead 在 T=0.2 时增加 45.00，在 T=0.8 时增加 40.80，在 T=1.2 时增加 35.20。
- WriteAfterWrite 的增益较小，最高只到 T=0.8 时的 9.00，这说明只有依赖标签时有时还不够，还需要更多分析。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13927v1](http://arxiv.org/abs/2604.13927v1)
