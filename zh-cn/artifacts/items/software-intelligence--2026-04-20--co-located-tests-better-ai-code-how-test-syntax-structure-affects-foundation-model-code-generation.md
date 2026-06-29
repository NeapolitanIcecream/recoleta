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
论文提出，测试的放置方式会改变 AI 编码模型的代码生成质量。把测试放在代码旁边，像 Python doctest 那样，保留率和正确率都明显高于 Rust 里分开的测试块。

## 问题
- 论文研究测试语法结构是否会改变基础模型生成代码的方式，尤其是它们会不会保留提示里给出的测试，以及生成的代码能不能通过这些测试。
- 这对 AI 辅助开发很重要，因为团队现在常让模型同时生成实现和测试，测试组织方式会影响代码质量、CI 行为和模型评估。
- 以往的代码基准主要看正确率，但通常不测模型是否保留了给定测试，也不看保留率和正确率是否同步变化。

## 方法
- 作者做了一项大规模实证研究，包含 830+ 个生成文件、12 个模型和 3 家提供方，任务是实现一个 d 叉堆。
- 他们比较了 Python doctest 形式的内联测试和 Rust `#[test]` 块形式的分离测试，并在 temperature 0 下重复运行。
- 评估使用 SEGA，这是一套三部分指标：**确定性**（多次运行中输出相同的比例）、**保留率**（输出中保留了提示测试的比例）和**正确率**（测试通过的比例）。
- 他们还对 7 个开源架构做了机制分析，包括 6 个 transformer 和 RWKV-6，用来测量内联语法中的测试标记是否比分离语法更强地关注函数 token。
- 他们用 knockout 和 steering 实验检验这些内部信号是否会因果地影响行为。

## 结果
- 在 Python 基线任务里，模型生成自己的 doctest 时，测试过的 9 个模型都达到 **100% 保留率** 和 **100% 正确率**；但确定性仍有差异，从 Mistral Medium 的 **0%** 到多个 Claude 模型的 **100%**。
- 在提示给出的内联 Python doctest 下，除 **Claude 3.5 Haiku** 外，所有模型的保留率都是 **100%**；Haiku 把所有 doctest 都删掉，保留率降到 **0%**。正确率仍然很高，在 64 个测试的设置下是 **92–97%**，在调整后的 73 个测试设置下是 **98.6–99%**。
- 在分离的 Rust `#[test]` 块下，模型表现明显分化：**Haiku 4.5、Sonnet 4/4.5 和 Opus 4.6** 达到 **100% 保留率** 和 **100% 通过率**；**Opus 4/4.1/4.5** 的保留率是 **0%**，因为它们把所有测试都抑制掉了，尽管生成的 Rust 代码仍能编译，并被描述为功能正确。
- **Haiku 3** 在 Rust 上表现很差，保留率 **0%**、无法编译、通过率 **0%**。**Mistral Medium** 在 50 次运行里保留了全部 28 个 Rust 测试，但只有 **62%** 的运行能编译并通过。
- 对 7 个开源架构的机制分析发现，在 **5/7** 个模型中，内联 Python 测试标记获得的注意力比 Rust 测试标记强 **2.8x 到 4.4x**；报告中的例子包括 Qwen2.5-Coder-7B 的 **3.51x**、CodeGemma-7B 的 **4.35x** 和 RWKV-6 的 **2.96x**，并给出 **p < 0.0002**。
- 论文还指出，**temperature 0 并不能保证确定性**：例如 Mistral Medium 的确定性是 **0%**，Devstral-2512 是 **52%**，Claude Opus 4.6 是 **30–64%**，而有些模型仍保持 **100%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19826v1](http://arxiv.org/abs/2604.19826v1)
