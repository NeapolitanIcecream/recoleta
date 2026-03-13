---
source: hn
url: https://github.com/Replikanti/agentis
published_at: '2026-03-09T23:07:42'
authors:
- ylohnitram
topics:
- ai-native-language
- agent-programming
- llm-as-stdlib
- content-addressed-code
- evolutionary-branching
relevance_score: 0.93
run_id: materialize-outputs
---

# Agentis – An AI-native programming language where the LLM is the stdlib

## Summary
Agentis 提出一种面向 AI 代理的编程语言，把 LLM 直接作为“标准库”，并将代码表示为带版本控制的二进制哈希 DAG 而非文本文件。其目标是让程序天然围绕提示、验证、分支探索和受控执行来构建。

## Problem
- 传统编程语言把 LLM 当外部 API，而不是语言级原语，这使得构建以推理、分类、提取为核心的 agent 程序较为笨重。
- 文本文件 + 常规 VCS 的模型不一定适合 AI 生成/演化式代码，容易出现合并冲突，也缺少围绕 agent 执行的原生分支与追踪机制。
- 自主代理容易产生失控调用、无限消耗或不安全 I/O，因此需要预算约束、沙箱和可验证的执行模型。

## Approach
- 把 `prompt` 设计成语言原语：很多原本由传统 stdlib 完成的操作，改为直接向 LLM 请求，并支持类型化输出，如 `prompt(...) -> list<string>` 或结构化类型。
- 通过 `validate` 机制对 LLM 输出做约束检查，例如置信度阈值，从而把生成结果纳入程序逻辑与失败处理流程。
- 引入 Cognitive Budget（CB）/ fuel 机制，对操作成本进行限制，防止代理无限运行，并鼓励更高效的提示设计。
- 使用 `explore` 做进化式分支：执行可分叉，成功结果形成新分支，失败分支被丢弃，适合搜索式问题求解。
- 将代码存为 SHA-256 内容寻址的 AST/DAG，并与内置 VCS 融合；同时提供沙箱文件 I/O 和域名白名单网络访问以增强安全性。

## Results
- 文本中**没有提供正式实验、基准测试或同行评测的定量结果**，因此无法验证其相对现有语言/框架的性能提升幅度。
- 给出了可操作性声明：首次运行 `agentis go examples/fast-demo.ag` 的输出时间约 **3–8 秒**，但未说明硬件、模型、任务和对比基线。
- 提供了若干具体功能主张：支持类型化提示输出、验证规则、进化式分支、内容寻址代码存储、无合并冲突设计、沙箱 I/O、网络白名单。
- 工具链层面列出了命令与流程，如 `init`、`go`、`commit`、`run`、`branch`、`switch`、`log`，说明其不仅是语言概念，也包含执行与版本管理实现。
- 实现复杂度主张较强：宣称“Zero bloat”，基于 **Rust**，依赖仅提到 **sha2** 与 **ureq**，但这属于工程描述而非效果指标。

## Link
- [https://github.com/Replikanti/agentis](https://github.com/Replikanti/agentis)
