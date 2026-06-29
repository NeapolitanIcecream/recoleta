---
source: arxiv
url: https://arxiv.org/abs/2606.11869v1
published_at: '2026-06-10T09:44:54'
authors:
- Marc Alier Forment
- Juanan Pereira
- "Francisco Jos\xE9 Garc\xEDa-Pe\xF1alvo"
- "Mar\xEDa Jos\xE9 Casa\xF1 Guerrero"
topics:
- custom-ai-agents
- agent-engineering
- multi-agent-software-engineering
- llm-tool-use
- agent-evaluation
- cli-orchestration
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Agents All the Way Down; A Methodology for Building Custom AI Agents from Substrate to Production

## Summary
## 摘要
本文提出“Agents All the Way Down”，一种在真实产品中构建自定义 AI 代理的五阶段方法。它重点说明如何把用通用代码代理做出的原型，转换成基于 CLI 的已交付代理，并配合场景测试。

## 问题
- 工程师需要在自己的应用里使用私有工具、产品数据、安全规则、审计日志和领域语言的代理。
- 文中认为，现有资料分别说明了 function calling、MCP、CLI、ReAct、Reflexion 和 code agents 等单个部分，但没有把它们串成一套端到端的构建实践。
- 这个缺口很重要，因为自定义代理需要可预测的成本、可维护的代码、产品集成，以及超出普通确定性软件测试的测试方式。

## 方法
- P1 把 LLM 视为一个软件组件，并按 `tools -> system -> messages` 组织提示词，让稳定内容保持可缓存，动态内容留在消息历史中。
- P2 定义了构建块：function calling、MCP、CLI 工具、liteshell 模式、agent loop、skills、characters、hooks 和 scaffolding。
- P3 使用 Claude Code、OpenCode 或 Cursor 这类通用代码代理，在真实应用上做原型。
- P4 把原型里的工具、提示词、skills、安全检查和指令提取出来，收拢成一个小型自定义代理循环，并作为 CLI 交付，这被称为 Turtle 模式。
- P5 用通用代理驱动自定义代理跑行为场景；这和单元测试、集成测试以及端到端测试互为补充。

## 结果
- 该方法共有 5 个阶段：P1 和 P2 这两个前提，后面接一个重复的三步循环 P3 -> P4 -> P5。
- 主要案例是 LAMB 教育平台上的 AAC：由 1 名开发者和一个 AI pair-programmer 用约 10 天完成，随后从 2026 年 4 月起在 2 所大学部署，覆盖约 200 名 educator-creators。
- 在 CLI 与 MCP 的成本对比中，文中引用了一项受控的匹配任务基准：通过 MCP 的 token 数大约是 CLI 的 35 倍，而硬场景完成可靠性在 MCP 上为 72%，在 CLI 上为 100%。
- 文中还引用了一个 GitHub 语言检查案例：通过匹配的 MCP server 大约用了 44,026 个 token，而通过 `gh` CLI 大约用了 1,365 个 token。
- 另一个 GitHub MCP 案例中，93 个暴露工具在会话开始时带来约 55,000 个 registry token，而 `gh` 对应版本约为 200 个 token。
- 文中没有对完整五阶段方法给出受控的定量评估；其安全收益以设计论证的方式提出，依赖数量和攻击面测量留待未来工作。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.11869v1](https://arxiv.org/abs/2606.11869v1)
