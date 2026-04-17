---
source: arxiv
url: http://arxiv.org/abs/2604.08102v1
published_at: '2026-04-09T11:21:28'
authors:
- Jorge Melegati
topics:
- test-oriented-programming
- llm-code-generation
- software-engineering
- test-generation
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Test-Oriented Programming: rethinking coding for the GenAI era

## Summary
## 摘要
论文提出了测试导向编程（TOP）：开发者审核生成的测试，再让 LLM 根据这些测试生成生产代码。作者构建了一个概念验证工具 Onion，并展示这种工作流可以完成一个小型命令行程序，同时也暴露了明确的局限和失败模式。

## 问题
- 现有的 LLM 编码工具仍然要求开发者检查生产代码，因此抽象层级仍然接近普通编程。
- 自然语言规格有歧义，而 LLM 输出具有非确定性，所以很难直接信任把实现工作交给模型。
- 论文提出的问题是：开发者能否把审核重点从生产代码转移到测试代码上；如果 GenAI 要以可靠方式减少手工编码工作，这一点就很重要。

## 方法
- TOP 先用自然语言规格生成测试代码，再用这些测试生成生产代码。
- 在设想的工作流中，开发者会审核并编辑生成的 YAML 配置、系统结构和测试文件，但不直接编辑生产代码。
- 作者在 Onion 中实现了这一思路。Onion 是一个 Python 命令行工具，会迭代生成项目结构、验收测试、类测试，然后生成实现代码，直到测试通过或运行中止。
- 评估使用了一个小型 BibTeX 命令行应用，功能包括添加条目、列出条目和搜索文本，并比较了两个模型：GPT-4o-mini 和 Gemini 2.5-Flash。

## 结果
- 在同一任务上，Onion 对每个模型各运行 **5 次**，总计 **10 次运行**。
- **10 次运行全部成功**，都生成了目标应用。
- 在 **0 次运行** 中，开发者需要直接修改生产代码。
- 总共 **2 次运行** 需要开发者在测试代码中添加注释来引导生成（**GPT-4o-mini 1 次，Gemini 2.5-Flash 1 次**），原因是模型在同一组测试上反复失败。
- 对于 **GPT-4o-mini**，作者报告有 **1 次运行** 需要在检查实现之前先修改测试代码。
- 论文**没有报告标准软件指标**，例如基准通过率、节省时间、token 成本、准确率，或与 Copilot、TDD、多代理基线的比较。最明确的结论是：在一个小任务上，经过审核的测试可以用于生成生产代码；不同运行的输出会变化；Gemini 2.5-Flash 生成的代码通常比 GPT-4o-mini 更长，注释也更多。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08102v1](http://arxiv.org/abs/2604.08102v1)
