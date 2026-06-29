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
## 总结
本文提出 Test-Oriented Programming（TOP），一种软件开发方式：开发者先审查生成的测试，再让 LLM 根据这些测试生成生产代码。作者构建了一个概念验证工具 Onion，并展示这种工作流可以完成一个小型命令行程序，但也有明确的限制和失败模式。

## 问题
- 现有的 LLM 编码工具仍然让开发者检查生产代码，因此抽象层级仍然接近普通编程。
- 自然语言规格本身有歧义，LLM 输出也不确定，所以直接把实现交给模型并不容易信任。
- 论文想知道，开发者能否把审查重点从生产代码转到测试代码；如果 GenAI 要在可靠的前提下减少人工编码，这个问题就很重要。

## 方法
- TOP 先根据自然语言规格生成测试代码，再用这些测试生成生产代码。
- 开发者会审查和编辑生成的 YAML 配置、系统结构和测试文件，但在目标工作流中不直接编辑生产代码。
- 作者把这个想法实现为 Onion，这是一个命令行 Python 工具，会迭代生成项目结构、验收测试、类测试，然后生成实现代码，直到测试通过或运行中止。
- 评估使用了一个小型 BibTeX 命令行应用，功能包括添加条目、列出条目和搜索文本，并对比了两个模型：GPT-4o-mini 和 Gemini 2.5-Flash。

## 结果
- Onion 在同一任务上每个模型运行 **5 次**，总共 **10 次运行**。
- **10 次运行全部成功** 生成了目标应用。
- 在 **0 次运行** 中，开发者需要直接修改生产代码。
- 在 **共 2 次运行** 中（**1 次使用 GPT-4o-mini，1 次使用 Gemini 2.5-Flash**），开发者不得不给测试代码加注释，以便在同一组测试上多次失败后引导生成。
- 对于 **GPT-4o-mini**，作者报告有 **1 次运行** 需要在检查实现之前修改测试代码。
- 论文没有报告标准软件指标，例如基准通过率、节省时间、token 成本、准确率，也没有和 Copilot、TDD 或多智能体基线比较。最明确的结论是：在一个小任务上，生产代码可以从经过审查的测试中生成；不同运行之间的输出会变化；Gemini 2.5-Flash 生成的代码通常比 GPT-4o-mini 更长、注释更多。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08102v1](http://arxiv.org/abs/2604.08102v1)
