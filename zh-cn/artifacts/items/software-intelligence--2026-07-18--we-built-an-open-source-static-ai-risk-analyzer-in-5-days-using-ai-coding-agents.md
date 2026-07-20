---
source: hn
url: https://github.com/ikaruscareer/SafeAI
published_at: '2026-07-18T22:24:40'
authors:
- ikaruscareer
topics:
- code-intelligence
- ai-agent-security
- static-analysis
- software-supply-chain
- mcp-security
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# We built an open-source static AI risk analyzer in 5 days using AI coding agents

## Summary
## 摘要
SafeAI 是一款开源静态分析器，可在部署前发现 AI 智能体源代码中的安全、能力和治理风险。它完全离线运行，生成确定性的风险评分和兼容 CI 的报告，并作为运行时测试的补充，而非替代方案。

## 问题
- 传统的 SAST、软件成分分析和基础设施扫描无法直接识别智能体特有的风险，例如提示注入、工具滥用、MCP 暴露、能力扩张或治理控制缺失。
- 在部署前发现这些问题十分重要，因为智能体可能通过框架代码和配置暴露 shell、文件系统、数据库或外部服务等能力。

## 方法
- 通过导入、配置、依赖、AST 解析、框架特定对象指纹以及备用正则表达式，检测 AI 框架和智能体能力。
- 将检测到的能力映射到标准化风险类别，并应用带有严重性和权重的可配置规则。
- 根据类别加权计算 0 到 100 的确定性信任评分，并为发现结果附加证据、置信度、已解析定义和溯源信息。
- 完全离线运行，不执行智能体或调用 LLM，随后导出终端、JSON、SARIF 2.1.0 和 HTML 报告，以集成到 CI/CD 流程中。

## 结果
- 在所提供的扫描示例中，SafeAI 分析了 12 个文件，检测到 LangGraph 和 CrewAI 框架以及 2 个 MCP 资产，并生成了 73 分的总体 AI 风险评分。
- 同一扫描报告了 9 项发现：1 项严重、3 项高危和 5 项中危；示例包括将不可信输入插入提示、检测到 shell 执行，以及缺少 MCP 身份验证。
- 该工具至少支持检测 8 个已命名的框架或平台集成，包括 LangGraph、CrewAI、LangChain、Semantic Kernel、OpenAI Agents SDK、Microsoft Agent Framework、Azure AI Foundry 和 Bedrock Agent。
- 所提供材料未报告独立基准测试、精确率/召回率评估或对比性能结果；对于部分基于 MCP 的能力，能力覆盖仍不完整，其框架适配器已列入计划。

## Problem

## Approach

## Results

## Link
- [https://github.com/ikaruscareer/SafeAI](https://github.com/ikaruscareer/SafeAI)
