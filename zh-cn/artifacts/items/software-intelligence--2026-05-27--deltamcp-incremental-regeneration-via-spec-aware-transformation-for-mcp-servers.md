---
source: arxiv
url: https://arxiv.org/abs/2605.28148v1
published_at: '2026-05-27T08:31:21'
authors:
- Aditya Pujara
- Xiaogang Zhu
- Hsiang-Ting Chen
topics:
- model-context-protocol
- code-generation
- api-evolution
- code-intelligence
- software-agents
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# DeltaMCP: Incremental Regeneration via Spec-Aware Transformation for MCP servers

## Summary
## 摘要
DeltaMCP 在 OpenAPI 规范变化时更新现有的 MCP 服务器工具，而不是重新生成整个服务器。这很重要，因为企业级 MCP 服务器通常包含自定义日志、保护措施和适配器代码，完整重生成可能会覆盖这些内容。

## 问题
- MCP 服务器把 API 操作暴露为可供 LLM 代理调用的工具，所以它们必须和不断变化的后端 API 保持一致。
- AutoMCP 之类的现有工具会在每次规范更新时重新生成完整的 MCP 服务器，这会浪费计算资源，也可能删除人工编写的企业逻辑。
- 大型 OpenAPI 差异可能超过 500,000 个 token，因此直接按整个规范重生成很难运行，也很难控制。

## 方法
- DeltaMCP 接收三个输入：现有的 Python MCP 服务器代码、旧的 OpenAPI 规范和新的 OpenAPI 规范。
- 它会解析 OpenAPI 引用，使用 Oasdiff 找出 schema 和端点变化，然后把差异拆成按端点划分的变更单元。
- 每个单元把旧的工具代码和相关的规范变化配对，这样模型只重写受影响的 MCP 工具。
- 作者用来自 Microsoft.Storage Azure REST API 规范的 2,000 多个结构化样本，使用 LoRA 对 StarCoder2-7B、CodeLlama-7B 和 Phi-3-Mini-4k-Instruct 进行微调。
- 生成的工具补丁通过适配器逻辑插回现有的 MCP 服务器，从而保留无关的自定义代码。

## 结果
- 在未见过的 Microsoft.Resources 评测数据上，DeltaMCP 在更新期间的平均 CPU 使用率约为 0.1%，AutoMCP 约为 3.0%。
- DeltaMCP 的内存使用约为 10.5 到 12.5 MB，AutoMCP 平均约为 30 MB。
- 论文报告说，DeltaMCP 在每次版本更新中触及的工具数量远少于 AutoMCP，但摘要没有给出图 4 中的精确数值。
- 代码质量用 100 分标准化量表评估，依据是语法检查、MCP 代理执行和 OpenAPI schema 对齐；摘要说 DeltaMCP 的一致性高于 AutoMCP，但没有给出图 5 中的精确分数。
- 训练使用 2,048 token 的上下文窗口，训练 3 个 epoch，使用 4-bit 量化和 FlashAttention，在一块 480 GB 显存的 NVIDIA GH200 GPU 上完成。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28148v1](https://arxiv.org/abs/2605.28148v1)
