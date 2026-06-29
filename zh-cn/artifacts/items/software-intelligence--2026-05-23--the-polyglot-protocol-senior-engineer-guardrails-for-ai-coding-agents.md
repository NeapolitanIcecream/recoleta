---
source: hn
url: https://github.com/sabir-gbs/the-polyglot-protocol
published_at: '2026-05-23T22:11:00'
authors:
- sabirsemerkant
topics:
- ai-coding-agents
- code-generation
- polyglot-codebases
- agent-validation
- software-quality
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# The Polyglot Protocol – senior-engineer guardrails for AI coding agents

## Summary
## 摘要
The Polyglot Protocol 为 AI 编码代理提供了一份共享的工程检查清单，面向多语言仓库。它通过仓库发现、语言选择规则、依赖检查、测试、安全审查和最终验证，来提高代码生成的安全性。

## 问题
- AI 编码代理常会猜测 API、包名、标志和项目约定，这会产出看起来有效、但在审查或运行时检查中失败的代码。
- 多语言仓库把风险放大了，因为代理必须选对语言、保留本地模式，并处理不同的运行时和工具链。
- 团队会在重复那些本应由代理在写代码前就应用的标准上浪费时间。

## 方法
- 该项目为 Codex、Claude Code、OpenCode 和自定义编码代理工作流打包了一种可移植技能。
- 这个协议要求先做仓库发现，再执行语言选择、依赖纪律、安全、测试、验证和最终审查的规则。
- 它为 22 种语言提供了专门指南，包括 TypeScript、Python、Rust、SQL、Java、Go、Swift、Kotlin、C++ 和 Zig。
- 它要求代理根据本地代码或官方文档核实工具和 API 说法，并用证据标注不受支持的检查。
- 本地脚本 `scripts/validate-workspace.py` 用于检查协议工作区。

## 结果
- 摘要没有报告代理性能基准提升、任务成功率，也没有与基线提示进行比较。
- 项目报告 `workspace validation: PASS` 和 `language guidance validation: PASS`，当前得分为 `100/100`。
- 仓库包含 `22` 种语言的指南和 `22` 个语言 README 文件。
- 它列出了用于工作流、验证和规则的 `11` 个运维文件。
- 它包含面向 `3` 个命名编码环境的适配器：Codex、Claude Code 和 OpenCode。

## Problem

## Approach

## Results

## Link
- [https://github.com/sabir-gbs/the-polyglot-protocol](https://github.com/sabir-gbs/the-polyglot-protocol)
