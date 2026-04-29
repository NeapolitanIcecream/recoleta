---
source: arxiv
url: http://arxiv.org/abs/2604.18834v1
published_at: '2026-04-20T20:58:52'
authors:
- Dinithi Jayasuriya
- Aravind Saravanan
- Nilesh Ahuja
- Amanda Rios
- Amit Trivedi
topics:
- eda-code-generation
- structural-verification
- openroad
- code-intelligence
- tool-use
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging

## Summary
## 概要
这篇论文认为，LLM 在生成 OpenROAD 脚本时，很多失败来自对象和 API 依赖关系被破坏，而不是语法错误。论文引入了执行前的结构验证，让系统在运行 EDA 工具之前就能发现并修复这些问题，从而提高通过率并减少工具调用。

## 问题
- 论文关注从自然语言到 EDA 代码的 OpenROAD 生成任务。在这类任务中，生成的脚本经常失败，原因包括沿用了无效的设计对象路径、跳过了必需的中间对象，或在错误的类型上调用 API。
- 这很重要，因为 tool-in-the-loop 调试依靠反复执行和修复来纠错，会增加延迟、提高工具使用量，并且在多步工作流中扩展性较差，因为前面的错误会向后传播。
- 在 EDA 中，执行依赖有状态的设计层级和操作前提条件，因此仅靠语法检查会漏掉许多真实的失败原因。

## 方法
- 该方法把每个任务转换成一个**结构依赖图**，其中节点是带类型的设计对象、条件和动作，边则编码了有效的获取关系和依赖关系。这个图充当执行契约。
- 它根据提示词并结合 OpenROAD API 模式来构建和验证这个图，在代码生成之前过滤掉幻觉节点、无效的类型转换和缺失的前提条件。
- 检索和代码生成都以该图为条件，因此模型会为特定对象转换检索 API 示例，并生成遵循所需依赖路径的代码。
- 一个四层验证器会检查语法、因果流程、API 对齐和任务级语义，然后依据诊断结果进行局部修复，而不是在外部工具中完整重跑。
- 对于多步任务，它会对每个子任务运行同样的流程，并加入轨迹级反思来诊断跨步骤失败；一个不确定性感知过滤器会对通过验证器的程序打分，在执行前减少误接受。

## 结果
- 在 **single-step** OpenROAD 任务上，完整系统的**通过率达到 82.5%**，高于 **LLM+RAG** 的 **73.0%** 和使用 GPT-4.1-mini 的 **LLM + tool-in-loop** 的 **76.0%**。
- 在同样的 single-step 设置下，该方法每个任务使用 **1.00 次工具调用**，而 tool-in-loop 为 **1.77 次**，OpenROAD-Agent 为 **3.54 次**；总调用次数分别为 **120**、**248** 和 **496**。摘要称，与 tool-in-loop 调试相比，这相当于**减少超过 2×** 的工具调用。
- Table 1 中，完整流程在 single-step 任务上的延迟是 **34.8 s**，而 tool-in-loop 为 **53.0 s**，OpenROAD-Agent 为 **70.0 s**；Table 2 报告 GPT-4.1-mini 的 tool-in-loop 为 **37.6 s**，所提方法为 **34.8 s**。
- 在 **multi-step** 任务上，摘要报告通过率从 **30.0% 提高到 70.0%**，加入 **trajectory-level reflection** 后进一步提高到 **84.0%**。
- 不确定性感知过滤将验证器的误报率从 **20.0%** 降到 **6.7%**，并将精确率从 **80.0%** 提高到 **93.3%**。
- 在不同生成器上，完整方法报告 **GPT-4o** 的通过率为 **83.0%**，**GPT-4.1-mini** 为 **82.5%**；给 OpenROAD-Agent 加上验证器后，其通过率从 **16.4%** 提高到 **31.8%**，同时保持每个任务 **1.00 次**工具调用。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18834v1](http://arxiv.org/abs/2604.18834v1)
