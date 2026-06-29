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
TSCG 将 JSON 工具 schema 编译成紧凑的结构化文本，让 LLM 代理在使用更少输入 token 的同时更准确地选择工具。论文报告称，当工具目录变长时，小模型和前沿模型都获得了大幅提升。

## 问题
- 生产环境的代理 API 会把工具定义作为 JSON schema 发送，每次调用消耗 3,000 到 25,000 个输入 token，并且会随工具数量线性增长。
- 当目录规模变大时，小模型的工具调用准确率会下降；论文报告称，在 JSON schema 设置下，15 个工具以上的准确率为 0% 到 49%。
- 这会抬高 schema 开销，也让许多本地 4B–14B 模型难以稳定进行工具调用。

## 方法
- TSCG 是一个位于 API 边界的确定性编译器：它在模型看到输入之前，把 JSON schema 转成结构化文本。
- 它使用八个固定操作，包括与 tokenizer 对齐的分隔符、先约束后布局、因果排序、填充项删除、结构压缩和选择性锚点重复。
- 它不需要模型权重、微调、搜索或运行时模型调用；实现是一个零依赖、1,200 行的 TypeScript 包，编译时间低于毫秒级。
- 这个方法保留完整的工具目录可见性，同时减少重复的 JSON 语法和 schema 样板内容。

## 结果
- 主要基准大约包含 19,000 次调用，覆盖 12 个模型和 5 个核心场景，并附带 BFCL 和 GSM8K 检查。
- 在前沿模型上，TSCG 文本在所有报告的 Scenario A/B 单元中都优于原生 function calling：Claude Sonnet 4 提升 +11.2 个百分点和 +5.0 个百分点，节省 50.1% token；GPT-4o 提升 +1.0 个百分点和 +9.7 个百分点，节省 6.2%；GPT-5.2 提升 +29.7 个百分点和 +9.2 个百分点，节省 11.4%。
- 在 BFCL 上，Claude Sonnet 4 使用 TSCG 后，准确率从 85.7% 提高到 93.2%，工具选择从 86.7% 提高到 95.0%，参数 F1 从 84.2% 提高到 91.7%，同时节省 46.8% token。
- 对小模型，保守版 TSCG 让 Mistral 7B 在 20 个工具时从 35.0% 提高到 80.0%，在 50 个工具时从 30.0% 提高到 75.3%；Gemma 3 4B 在 50 个工具时从 24.3% 提高到 87.5%。
- 摘要称，Phi-4 14B 在 20 个工具时准确率从 0% 恢复到 84.4%，在 50 个工具时达到 90.3%。
- 论文还称，对于格式良好的 schema，形式化压缩下界至少为 51%；在较重的 MCP schema 上可节省 52% 到 57% 的 token；在约 10,500 个输入 token 时，准确率仍有 +5.0 个百分点的优势。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04107v1](https://arxiv.org/abs/2605.04107v1)
