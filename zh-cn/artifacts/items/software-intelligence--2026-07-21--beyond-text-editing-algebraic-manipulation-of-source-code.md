---
source: arxiv
url: https://arxiv.org/abs/2607.18742v1
published_at: '2026-07-21T06:05:17'
authors:
- Kevin Pulo
topics:
- code-intelligence
- automated-software-production
- llm-coding-agents
- semantic-code-editing
- program-transformation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Text Editing: Algebraic Manipulation of Source Code

## Summary
## 摘要
论文提出了源代码代数（source code algebra）：将代码变更表示为确定性的语义操作，而不是底层文本编辑。一项概念验证表明，LLM 编程代理可以更成功地执行非局部变更，同时使用少一到两个数量级的 token，但相关证据仍属初步结果。

## 问题
- 基于文本的编辑要求程序员和 LLM 代理识别并更新每个受影响的位置，增加了上下文需求，也提高了出现语法、语义、合并和逻辑错误的风险。
- 这对代理式软件开发很重要，因为高层次的编程计划必须被转换为分散在整个代码库中的底层编辑。

## 方法
- 源代码代数将代码库视为一种结构化对象，可以通过 `AddParam`、`Rename`、`MakeCond`、`MoveParam` 和 `TupleToStruct` 等逻辑操作进行转换。
- 每个操作旨在完成一次语义修改所需的全部变更，从而生成确定的、在语法和语义上均有效的输出。
- 操作可以组合成更高层次的操作，例如 `MakeOptional`，并可以呈现完备性、可组合性、幂等性、复幂性和交换性等性质。
- 源代码代数系统（Source Code Algebraic System，SCAS）使用 tree-sitter 解析代码，为语法树补充语义信息，将结果存储在 MongoDB 中，并将可组合操作作为工具提供给 LLM 代理。

## 结果
- 一项可行性探测试验在一个约 5.5k 行、500 KB、200k token、包含 8 个文件的合成代码库中，使用配备 SCAS 的 ReAct 代理执行跨文件 Java 方法符号重命名任务。
- 该任务特意使用了含义模糊的符号名称，使朴素的文本替换方法不可靠。
- 摘要报告称，代数编辑的成功率高于基于文本的基线，但摘录没有提供确切的成功率或样本量。
- 对于所演示的非局部变更，SCAS 所需的 token 数比基于文本的基线少一到两个数量级。
- 结果支持该方法的可行性，并推动进一步研究，但评估明确属于初步工作，尚不能证明其在不同语言、任务或代码库上的广泛性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18742v1](https://arxiv.org/abs/2607.18742v1)
