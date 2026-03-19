---
source: hn
url: https://github.com/Replikanti/agentis
published_at: '2026-03-09T23:07:42'
authors:
- ylohnitram
topics:
- ai-programming-language
- llm-as-stdlib
- agent-runtime
- content-addressed-code
- version-control
relevance_score: 0.09
run_id: materialize-outputs
language_code: zh-CN
---

# Agentis – An AI-native programming language where the LLM is the stdlib

## Summary
Agentis 提出了一种面向智能体的 AI-native 编程语言，把 LLM 直接当作“标准库”，并将代码存储为带版本控制的哈希 DAG 而非文本文件。其目标是把提示、执行约束、分支探索和可追踪版本管理融合到同一个编程模型中。

## Problem
- 现有编程语言和工具链主要为传统确定性软件设计，不适合以 LLM 调用为核心原语的 agent 工作流。
- 基于文本文件和常规 VCS 的开发方式，难以自然表达提示驱动执行、分支探索、执行预算控制和内容寻址代码管理。
- 如果缺少内建的沙箱、验证和成本约束，LLM agent 容易失控、难复现，也不利于安全执行。

## Approach
- 把 `prompt` 设计成语言原语，而不是库函数；很多本应由 stdlib 完成的操作都交给 LLM，例如字符串抽取、分类等。
- 使用类型化输出和 `validate` 机制，让 LLM 结果可以按结构化类型返回，并通过约束检查提高可控性。
- 引入 Cognitive Budget（CB）作为执行燃料，为操作计费，限制 agent 无限循环或过度调用模型。
- 使用 `explore` 进行“进化式分支”：执行时可分叉尝试方案，成功则保留为分支，失败则丢弃。
- 代码底层不是文本文件，而是 SHA-256 哈希的 AST/DAG，并与内建 VCS 融合，支持按哈希导入、提交、运行、切换分支等。

## Results
- 文中没有提供标准论文式定量实验结果，也没有在公开基准上报告准确率、成功率或成本对比。
- 给出的最具体性能声明是：首次运行 `agentis go examples/fast-demo.ag` 的输出时间约 **3–8 秒**。
- 系统功能性主张包括：代码为 **SHA-256** 内容寻址 AST，声称可避免传统文本合并冲突，并支持按哈希导入。
- 安全/工程约束主张包括：文件 I/O 被限制在 `.agentis/sandbox/`，网络访问需要域名白名单。
- 极简实现主张包括：运行时/实现“Zero bloat”，仅依赖 **Rust + sha2 + ureq**。
- 示例覆盖范围主张包括：仓库文档称提供 **6 个示例程序**，从 hello world 到 evolutionary branching。

## Link
- [https://github.com/Replikanti/agentis](https://github.com/Replikanti/agentis)
