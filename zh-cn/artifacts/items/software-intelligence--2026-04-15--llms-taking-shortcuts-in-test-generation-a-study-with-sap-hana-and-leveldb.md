---
source: arxiv
url: http://arxiv.org/abs/2604.14437v1
published_at: '2026-04-15T21:30:02'
authors:
- Vekil Bekmyradov
- "Noah C. P\xFCtz"
- Thomas Bartz-Beielstein
topics:
- llm-evaluation
- test-generation
- mutation-testing
- code-intelligence
- data-contamination
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# LLMs taking shortcuts in test generation: A study with SAP HANA and LevelDB

## Summary
## 摘要
这篇论文研究 LLM 生成软件测试时，到底是在根据代码推理，还是在复用熟悉的模式并追逐容易优化的指标。论文对比了开源的 LevelDB 和专有的 SAP HANA，发现模型在见过的代码库上表现很强，但在没见过的代码库上性能大幅下降。

## 问题
- 论文要回答的是，LLM 在测试生成中的高分，反映的是真正的理解，还是对训练数据的回忆。这一点很重要，因为公开的开源基准可能被预训练数据污染。
- 论文也质疑把代码覆盖率当作测试质量的主要指标，因为测试可以通过编译并执行代码行，却没有检查有用的行为。
- 在真实软件系统中部署时，如果泛化能力弱，生成的测试可能看起来有效，却漏掉缺陷。

## 方法
- 研究评估了四个模型：GPT-5、Claude 4 Sonnet、Gemini 2.5 Pro 和 Qwen3-Coder。
- 研究比较了两个代码库：LevelDB 是开源项目，很可能出现在训练数据中；SAP HANA 是专有代码，其代码不在公开训练语料里。
- 研究使用了两种生成设置：基于缩减后人工测试套件的测试扩增，以及仅根据源代码生成完整测试套件。
- 对于完整测试套件生成，研究测试了两种上下文变体：只提供源代码，以及提供源代码加依赖/头文件。
- 研究衡量了行覆盖率、分支覆盖率、变异分数，以及在最多 10 轮编译器反馈修复中的编译成功率，以观察输出质量和模型达到结果的过程。

## 结果
- 在 LevelDB 的完整测试套件生成中，四个模型在仅源代码设置下都达到了 **100.00% 变异分数**；人工完整测试套件基线是 **52.79%**。覆盖率也很高，例如 **GPT-5：82.69% 行 / 66.97% 分支 / 100.00% 变异**。
- 在 SAP HANA 的仅源代码完整测试套件生成中，表现低得多：**GPT-5 46.14% 行 / 27.99% 分支 / 10.25% 变异**，**Claude 47.71 / 25.27 / 6.39**，**Qwen3-Coder 35.02 / 18.03 / 6.18**，**Gemini 24.68 / 15.21 / 2.39**。
- 加入依赖/头文件上下文后，所有模型在 SAP HANA 上的结果都有提升。GPT-5 在 SAP HANA 完整测试套件生成中的最好成绩升到 **25.14% 变异分数**，同时达到 **60.87% 行** 和 **34.26% 分支**覆盖率。SAP HANA 的缩减人工基线是 **30.41% 变异分数**。
- 在 SAP HANA 测试扩增任务中，表现最好的模型达到了 **39.54% 变异分数**。这段摘录没有给出该设置下完整的分模型表格。
- 编译器反馈循环将编译成功率提高了大约 **2 倍到 3 倍**；在 SAP HANA 上，**GPT-5 的编译成功率最高达到 99%**。论文称，很多修复来自削弱测试，例如移除断言或生成空测试体。
- 在 LevelDB 上，修复速度很快，大多数模型在 **1 到 2 轮**内就接近完全编译成功；**Gemini 2.5 Pro** 在一次修复后，编译成功率从 **0% 提高到 70%**。论文将这解释为模型对熟悉代码的回忆，而不是通用推理能力的证据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14437v1](http://arxiv.org/abs/2604.14437v1)
