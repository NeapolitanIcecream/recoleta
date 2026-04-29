---
source: arxiv
url: http://arxiv.org/abs/2604.19826v1
published_at: '2026-04-20T14:47:46'
authors:
- "\xC9ric Jacopin"
topics:
- code-generation
- testing
- foundation-models
- mechanistic-interpretability
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation

## Summary
## 摘要
论文认为，测试放置方式会改变 AI 代码模型的生成质量。把测试直接写在代码旁边，比如 Python doctest，比在 Rust 中使用分离的测试块，能带来更好的保留率和更高的正确性。

## 问题
- 论文研究测试语法结构是否会改变基础模型生成代码的方式，尤其是模型是否会保留提示中给出的测试，并生成能够通过这些测试的代码。
- 这对 AI 辅助开发很重要，因为团队现在会让模型同时生成实现和测试，所以测试的组织方式会影响代码质量、CI 行为和模型评估。
- 以往的代码基准主要关注正确性，但通常不衡量模型是否保留给定测试，也不衡量保留率和正确性是否同步变化。

## 方法
- 作者在一个较复杂的任务上做了大规模实证研究：实现 d-ary heap，共生成 830+ 个文件，覆盖 12 个模型和 3 家提供商。
- 他们比较了 Python doctest 形式的内联测试与 Rust `#[test]` 块形式的分离测试，并在 temperature 0 下重复运行。
- 他们使用 SEGA 进行评估，这是一个三部分方案：**Determinism**（多次运行中输出完全相同的比例）、**Preservation**（输出中保留提示测试的比例）和 **Correctness**（测试通过的比例）。
- 他们还对 7 个开放模型做了机制分析，包括 6 个 transformer 和 RWKV-6，用来衡量在内联语法下，测试标记对函数 token 的注意力是否比在分离语法下更强。
- 他们使用 knockout 和 steering 实验来检验这些内部信号是否会因果性地影响模型行为。

## 结果
- 在 Python 基线设置中，模型自行生成 doctest，9 个被测试模型都达到 **100% preservation** 和 **100% correctness**；但 determinism 仍有差异，从 Mistral Medium 的 **0%** 到多个 Claude 模型的 **100%** 不等。
- 在使用提示提供的内联 Python doctest 时，除 **Claude 3.5 Haiku** 外，所有模型的 preservation 都是 **100%**；后者通过删除全部 doctest 使 **0% preservation**。在一种包含 64 个测试的设置中，correctness 仍维持在 **92–97%**，在改进后的 73 测试设置中为 **98.6–99%**。
- 在分离的 Rust `#[test]` 块设置下，模型表现明显分化：**Haiku 4.5、Sonnet 4/4.5 和 Opus 4.6** 达到 **100% preservation** 和 **100% pass rate**；而 **Opus 4/4.1/4.5** 的 **0% preservation**，因为它们抑制了全部测试，虽然生成的 Rust 代码仍可编译，并被描述为功能上正确。
- **Haiku 3** 在 Rust 上表现很差，出现 **0% preservation**、无法编译和 **0% pass rate**。**Mistral Medium** 在 50 次运行中保留了全部 28 个 Rust 测试，但只有 **62%** 的运行能够编译并通过测试。
- 对 7 种开放架构的机制分析发现，在 **7 个模型中的 5 个** 里，内联 Python 测试标记获得的注意力强度比 Rust 测试标记高 **2.8x 到 4.4x**；例子包括 Qwen2.5-Coder-7B 的 **3.51x**、CodeGemma-7B 的 **4.35x** 和 RWKV-6 的 **2.96x**，报告的结果为 **p < 0.0002**。
- 论文还报告，**temperature 0 不能保证 determinism**：例如 Mistral Medium 的 determinism 为 **0%**，Devstral-2512 为 **52%**，Claude Opus 4.6 为 **30–64%**，而有些模型则保持在 **100%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19826v1](http://arxiv.org/abs/2604.19826v1)
