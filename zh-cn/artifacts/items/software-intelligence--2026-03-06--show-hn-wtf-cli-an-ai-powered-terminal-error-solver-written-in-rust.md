---
source: hn
url: https://github.com/JitseLambrichts/WTF-CLI
published_at: '2026-03-06T23:46:53'
authors:
- JitseLambrichts
topics:
- cli-tooling
- terminal-error-diagnosis
- rust
- local-llm
- developer-tools
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: WTF-CLI – An AI-powered terminal error solver written in Rust

## Summary
WTF-CLI 是一个用 Rust 编写的命令行包装器：当终端命令执行失败时，它会自动截获错误输出，并调用本地或云端大模型生成修复建议。它面向开发者常见的 CLI 报错诊断场景，强调低摩擦使用方式与本地隐私优先。

## Problem
- 终端命令失败时，开发者通常需要手动阅读报错、搜索原因、再尝试修复，过程耗时且打断工作流。
- 许多 AI 辅助工具不直接嵌入 shell 命令执行链路，导致从“报错发生”到“得到可执行修复建议”之间仍有较高操作成本。
- 对于敏感代码或本地环境问题，把错误日志发送到云端也可能带来隐私与成本顾虑，因此需要本地优先的错误分析方案。

## Approach
- 核心机制非常简单：把普通命令写成 `wtf <your-command>`；如果命令成功，就像正常执行一样退出；如果失败，就捕获 stderr/stdout 中的错误上下文。
- 工具将失败输出发送给配置好的 AI 提供商，让模型生成结构化诊断与可执行修复命令，直接在终端中返回给用户。
- 默认强调本地模型工作流，优先支持通过 Ollama 运行本地模型，以实现“无 API 成本 + 更强隐私保护”。
- 同时提供云端后备方案，支持 OpenAI、Gemini 和 OpenRouter，可通过 `wtf --setup` 或环境变量快速切换。
- 工程实现上使用 Rust/Cargo 打包为独立 CLI，目标是以最小改动嵌入开发者现有命令行习惯。

## Results
- 文本未提供标准论文式定量实验结果，因此没有可报告的基准数据、准确率、速度或用户研究数字。
- 给出的最强具体产品性声明是：只需在原命令前加上 `wtf` 即可实现“失败即分析、成功即透明通过”的无缝包装体验。
- 支持 **4 类模型提供商**：Ollama、OpenAI、Gemini、OpenRouter；其中本地默认示例模型为 `qwen3.5:9b`，云端示例包括 `gpt-4o-mini`、`gemini-2.0-flash`、`arcee-ai/trinity-mini:free`。
- 给出的示例失败场景包括 **2 个**：`wtf npm run build` 和 `wtf ls /fake/directory`，表明其目标覆盖构建错误与文件系统类命令错误诊断。
- 项目声称输出具有“清晰结构”和“可执行修复命令”，并强调 **privacy first**、本地运行、无 API 成本（在使用 Ollama 时）等实际使用价值。

## Link
- [https://github.com/JitseLambrichts/WTF-CLI](https://github.com/JitseLambrichts/WTF-CLI)
