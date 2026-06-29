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
## 摘要
这篇论文认为，OpenROAD 脚本生成中的许多 LLM 失败来自对象和 API 依赖被破坏，而不是语法错误。它引入了执行前的结构验证，在运行 EDA 工具前捕获并修复这类错误，从而提高通过率并减少工具调用。

## 问题
- 论文关注面向 OpenROAD 的自然语言到 EDA 代码生成。生成的脚本常常因为沿着无效的设计对象路径前进、跳过必需的中间对象，或对错误类型调用 API 而失败。
- 之所以重要，是因为 tool-in-the-loop debugging 依赖反复执行和修复错误，这会增加延迟、提高工具使用量，并且在多步工作流中扩展性差，因为早期错误会继续传递。
- 在 EDA 中，执行依赖有状态的设计层级和动作前置条件，所以只检查语法会漏掉很多真实失败。

## 方法
- 该方法把每个任务转成一个 **structural dependency graph**。图中的节点是带类型的设计对象、条件和动作，边编码合法的获取关系和依赖关系。这个图充当执行契约。
- 系统根据 OpenROAD API schema 从提示词构建并验证这张图，在代码生成前过滤幻觉节点、无效类型转换和缺失前置条件。
- 检索和代码生成都以这张图为条件，模型会为特定对象转换检索 API 示例，并生成遵循所需依赖路径的代码。
- 一个四层验证器检查语法、因果流程、API 对齐和任务级语义，然后用基于诊断的局部修复代替在外部工具里完整重跑。
- 对多步任务，系统对每个子任务重复同样流程，并加入 trajectory-level reflection 来诊断跨步骤失败；uncertainty filter 会对通过验证器的程序打分，在执行前减少误接受。

## 结果
- 在 **single-step** OpenROAD 任务上，完整系统达到 **82.5% pass rate**，高于 **LLM+RAG** 的 **73.0%** 和使用 GPT-4.1-mini 的 **LLM + tool-in-loop** 的 **76.0%**。
- 在同一个 single-step 设置下，该方法每个任务只用 **1.00 tool calls**，而 tool-in-loop 为 **1.77**，OpenROAD-Agent 为 **3.54**；总调用次数分别是 **120**、**248** 和 **496**。摘要称这比 tool-in-loop debugging 少了 **超过 2×** 的工具调用。
- 表 1 中的 single-step 延迟，完整流程为 **34.8 s**，tool-in-loop 为 **53.0 s**，OpenROAD-Agent 为 **70.0 s**；表 2 报告 GPT-4.1-mini tool-in-loop 为 **37.6 s**，所提方法为 **34.8 s**。
- 在 **multi-step** 任务上，摘要报告通过率从 **30.0%** 提高到 **70.0%**，加入 **trajectory-level reflection** 后进一步提高到 **84.0%**。
- uncertainty-aware filtering 将验证器假阳性从 **20.0%** 降到 **6.7%**，并把 precision 从 **80.0%** 提高到 **93.3%**。
- 在不同生成器上，完整方法使用 **GPT-4o** 时通过率为 **83.0%**，使用 **GPT-4.1-mini** 时为 **82.5%**；给 OpenROAD-Agent 加上验证器后，通过率从 **16.4%** 提高到 **31.8%**，同时每个任务仍保持 **1.00** 次工具调用。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18834v1](http://arxiv.org/abs/2604.18834v1)
