---
source: hn
url: https://github.com/man-consult/code-mapper
published_at: '2026-06-20T23:49:07'
authors:
- brian-m
topics:
- code-intelligence
- static-analysis
- llm-code-tools
- software-visualization
- developer-workflow
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Codeflowmap – map a codebase's read/write/auth data flows

## Summary
## 摘要
Codeflowmap 是一个实验性的代码库地图，结合静态分析和可选的 LLM 文件注释。它通过展示 import、函数调用、数据读写、配置使用、认证路径和流程跟踪，帮助开发者验证生成代码或不熟悉的代码。

## 问题
- LLM 生成的代码可能可以编译，但仍然难以验证：审查者需要知道它改动了什么、读取和写入了什么，以及认证路径是否符合预期设计。
- 不熟悉的仓库需要在 import、调用、写入、配置和认证检查之间做缓慢的手动追踪。
- 这个问题会影响代码审查，因为遗漏的写入路径或认证流程可能带来安全、隐私或维护风险。

## 方法
- 静态分析在不调用模型的情况下构建基础图：import 边来自模块解析，TypeScript/JavaScript 函数调用边来自通过 TypeScript Compiler API 进行的符号解析。
- LLM 为每个文件添加关于读取、写入、配置、认证和流程的注释。图边不由模型推断。
- 该工具将结果写入 `<repo>/.codemap`，其中包括一个 Markdown vault，每个源文件对应一个 `.md` 文件，并用 `[[wikilinks]]` 表示真实图边。
- Web UI 支持 Files 和 Functions 视图、节点聚焦、上游/下游路径高亮、搜索，以及按流程类型过滤。
- 注释可以通过 Ollama 在本地运行，也可以通过任何兼容 OpenAI 的提供商运行；缓存注释使用文件内容哈希，因此未更改的文件不会被重新发送。

## 结果
- 摘录没有报告基准测试、准确率分数、运行时间测量或用户研究，因此没有提供突破性结果的定量证据。
- 它声称基础图的生成是确定性的，并且没有 token 成本；import 使用真实模块解析，TS/JS 调用边使用 TypeScript 符号解析。
- 语言覆盖范围有限：TS/JS 会得到函数级调用边，而 Python 目前只提供 import 边和符号。
- 默认本地注释模型是 `qwen2.5-coder:7b`，约 `4.7 GB`，据称可在 `16 GB` 笔记本电脑上运行。
- 建议的模型选项包括适用于 `32 GB+` 机器的 `devstral` `24B`，以及适用于 `8 GB` 机器的 `qwen2.5-coder:3b`。
- 该工具需要 Bun `≥ 1.0`；图扫描可以在没有 LLM 的情况下运行，而注释可能会把完整源文件发送给远程提供商，除非使用本地 Ollama。

## Problem

## Approach

## Results

## Link
- [https://github.com/man-consult/code-mapper](https://github.com/man-consult/code-mapper)
