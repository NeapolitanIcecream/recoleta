---
source: arxiv
url: https://arxiv.org/abs/2605.04107v1
published_at: '2026-05-04T15:35:45'
authors:
- Furkan Sakizli
topics:
- tool-calling
- agentic-llms
- schema-compression
- prompt-compression
- mcp
- llm-agents
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments

## Summary
## 摘要
TSCG 将 JSON 工具 schema 编译成紧凑的结构化文本，让 LLM 智能体在使用更少输入 token 的同时更准确地选择工具。论文报告称，当工具目录变长时，小模型和前沿模型都有大幅提升。

## 问题
- 生产环境中的智能体 API 以 JSON schema 发送工具定义，每次调用会消耗 3,000–25,000 个输入 token，并随工具数量线性增长。
- 随着目录规模扩大，小模型的工具使用准确率会下降；论文报告称，在 JSON schema 设置下，超过 15 个工具后准确率为 0–49%。
- 这个问题会提高 schema 开销和成本，并阻碍许多本地 4B–14B 模型进行可靠的工具调用。

## 方法
- TSCG 是位于 API 边界的确定性编译器：它在模型看到 JSON schema 之前，将其转换为结构化文本。
- 它使用八个固定算子，包括与 tokenizer 对齐的分隔符、约束优先布局、因果排序、填充内容移除、结构压缩和选择性锚点复制。
- 它不需要模型权重、微调、搜索或运行时模型调用；实现是一个零依赖、1,200 行的 TypeScript 包，编译时间低于 1 毫秒。
- 该方法保留完整可见的工具目录，同时减少重复的 JSON 语法和 schema 样板内容。

## 结果
- 主要基准包含约 19,000 次调用，覆盖 12 个模型和 5 个核心场景，另有 BFCL 和 GSM8K 检查。
- 在前沿模型上，TSCG 文本在所有报告的场景 A/B 单元中都优于原生函数调用：Claude Sonnet 4 提升 +11.2 pp 和 +5.0 pp，并节省 50.1% token；GPT-4o 提升 +1.0 pp 和 +9.7 pp，并节省 6.2%；GPT-5.2 提升 +29.7 pp 和 +9.2 pp，并节省 11.4%。
- 在使用 Claude Sonnet 4 的 BFCL 上，TSCG 将准确率从 85.7% 提高到 93.2%，工具选择从 86.7% 提高到 95.0%，参数 F1 从 84.2% 提高到 91.7%，同时节省 46.8% token。
- 对于小模型，保守版 TSCG 将 Mistral 7B 在 20 个工具下的准确率从 35.0% 提高到 80.0%，在 50 个工具下从 30.0% 提高到 75.3%；Gemma 3 4B 在 50 个工具下从 24.3% 提高到 87.5%。
- 摘要称 Phi-4 14B 在 20 个工具下的准确率从 0% 恢复到 84.4%，在 50 个工具下达到 90.3%。
- 论文称，对格式良好的 schema，形式化压缩下界至少为 51%；在重型 MCP schema 上可节省 52–57% token；在约 10,500 个输入 token 时有 +5.0 pp 的准确率优势。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04107v1](https://arxiv.org/abs/2605.04107v1)
