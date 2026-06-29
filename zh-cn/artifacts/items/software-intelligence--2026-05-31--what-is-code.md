---
source: hn
url: https://martinfowler.com/articles/what-is-code.html
published_at: '2026-05-31T21:40:11'
authors:
- wapasta
topics:
- llm-assisted-coding
- code-intelligence
- domain-driven-design
- software-design
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# What Is Code

## Summary
LLM 生成代码让键入式指令变得更便宜，所以代码的持久价值在于它编码的共享概念模型。文章认为，团队应把编码看成是为人、工具和 LLM 建立词汇。

## Problem
- LLM 可以根据高层提示生成可执行代码，这降低了单纯输入实现细节的价值。
- 团队仍然需要共享的领域含义：名称、边界、不变式、工作流和规则，供人和工具推理。
- 快速生成会带来认知债务，当代码包含团队看得懂却不理解、也无法维护的常见模式时尤其如此。

## Approach
- 文章把代码分成 2 个角色：机器指令和问题领域的人类可读模型。
- 它把编码解释为领域词汇和技术词汇之间的转换，例如把零售概念 catalog、order、payment 和 shipment 映射到 Web 和数据结构中。
- 它用领域驱动设计中的 bounded contexts 和 ubiquitous language 来解释为什么本地抽象必须和领域专家及用户一起发现。
- 它认为 TDD、重构和主动编码通过反馈帮助团队发现名称、边界和不变式。
- 它把同样的观点用于 LLM：精确的代码词汇、稳定的抽象和测试，会比单靠含糊提示给模型更多上下文。

## Results
- 定量结果：0。文章没有数据集、基准指标、基线、用户研究数量或测得的生产效率提升。
- 它提出代码有 2 个主要角色：机器的指令，以及供人、工具和 LLM 使用的概念模型。
- 它指出 1 个主要 LLM 风险：由生成出的词汇和结构引起、开发者不理解的认知债务。
- 它给出 3 个面向 LLM 辅助工作的具体设计帮助：稳定的抽象、清晰的语义，以及嵌入代码库中的测试。
- 它认为结构良好的代码可以降低对提示的敏感性和对模型的依赖，但没有给出准确率、缺陷率或延迟数据。

## Link
- [https://martinfowler.com/articles/what-is-code.html](https://martinfowler.com/articles/what-is-code.html)
