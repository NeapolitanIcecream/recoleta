---
source: hn
url: https://github.com/JitseLambrichts/WTF-CLI
published_at: '2026-03-06T23:46:53'
authors:
- JitseLambrichts
topics:
- cli-tool
- terminal-error-debugging
- developer-tools
- llm-applications
- rust
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: WTF-CLI – An AI-powered terminal error solver written in Rust

## Summary
这是一个用 Rust 编写的命令行包装器：当终端命令执行失败时，它会自动读取报错并调用 AI 给出诊断与修复建议。其核心卖点是无缝接入现有命令流，以及优先支持本地模型以保护隐私并降低成本。

## Problem
- 终端报错通常信息分散、难以快速定位，尤其对不熟悉命令行或环境配置的用户来说，排错成本高。
- 现有做法往往需要手动复制错误信息到搜索引擎或聊天模型中，打断工作流且效率低。
- 对很多开发者而言，将敏感错误日志发送到云端也存在隐私与费用顾虑，因此需要本地优先的解决方案。

## Approach
- 用一个极简的 CLI 包装层工作：只需在原命令前加上 `wtf`，若命令成功则正常透传输出，若失败则拦截错误输出并触发 AI 分析。
- 将失败命令的错误信息发送给已配置的模型提供方，返回结构化解释与可执行修复建议，帮助用户直接采取下一步操作。
- 提供多后端支持：优先本地 Ollama，也支持 OpenAI、Gemini、OpenRouter 作为云端或回退方案。
- 通过 `wtf --setup` 进行交互式配置，或使用 `.env` / 环境变量手动指定 provider、模型与 API key，降低部署门槛。
- 采用 Rust 实现并通过 Cargo 安装，强调轻量、易分发和对现有 shell 使用习惯的最小侵入。

## Results
- 文档展示了明确的使用方式：例如 `wtf npm run build` 与 `wtf ls /fake/directory`，在命令失败时自动捕获错误并输出 AI 诊断与修复建议。
- 声称可实现“无缝包装”：成功命令按正常方式退出，失败命令才触发 AI 分析，不改变常规命令执行路径。
- 声称具备“隐私优先”特性：支持通过 Ollama 在本地运行模型，从而避免 API 成本并减少错误日志外发。
- 支持 4 类模型提供方/后端：Ollama、OpenAI、Gemini、OpenRouter，并允许通过环境变量切换具体模型，如 `qwen3.5:9b`、`gpt-4o-mini`、`gemini-2.0-flash` 等。
- 提供的文本**没有给出任何定量实验结果**，没有报告成功率、修复率、延迟、用户研究或与其他终端助手/搜索方式的基线对比。仅有功能性与产品特性层面的主张。

## Link
- [https://github.com/JitseLambrichts/WTF-CLI](https://github.com/JitseLambrichts/WTF-CLI)
