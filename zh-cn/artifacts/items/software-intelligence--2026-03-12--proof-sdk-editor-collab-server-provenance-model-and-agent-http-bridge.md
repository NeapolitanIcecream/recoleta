---
source: hn
url: https://github.com/everyinc/proof-sdk
published_at: '2026-03-12T23:20:13'
authors:
- azhenley
topics:
- collaborative-editor
- provenance-tracking
- agent-http-bridge
- realtime-collaboration
- human-ai-collaboration
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Proof SDK: Editor, collab server, provenance model, and agent HTTP bridge

## Summary
Proof SDK 是一个开源协作文档基础设施，提供编辑器、实时协作服务器、溯源模型以及面向代理的 HTTP 桥接接口。它面向需要把人类协作编辑与智能代理操作接入同一文档工作流的开发者。

## Problem
- 解决的问题是：如何把**多人实时文档协作**、**编辑历史/来源追踪**与**AI/代理可编程操作**统一到同一套文档系统里。
- 这很重要，因为在人机协同写作、代码/文档共创、以及多代理工作流中，系统不仅要支持编辑，还要支持可审计的变更、评论、建议与状态同步。
- 传统编辑器或协作后端通常缺少统一的代理接口与 provenance（溯源）模型，导致自动化能力难以安全地接入协作文档。

## Approach
- 核心方法很简单：把协作文档系统拆成四个可组合部分——**编辑器**、**实时协作服务器**、**provenance 模型**、**agent HTTP bridge**。
- 编辑层支持协作式 Markdown 编辑，并内置 **comments、suggestions、rewrite** 等高层操作，而不只是低级文本编辑。
- 服务端通过一组公开 HTTP 路由暴露文档状态、快照、编辑操作、presence 和事件流，例如 `/state`、`/snapshot`、`/edit`、`/ops`、`/events/pending`。
- 面向代理的 bridge 单独暴露状态、标记、评论、建议、重写和 presence 接口，使外部 agent 可以用标准 HTTP 协议读取文档并提交结构化修改。
- 项目同时提供示例应用与模块化包（如 `doc-editor`、`doc-server`、`agent-bridge`、`doc-store-sqlite`），便于二次集成。

## Results
- 文本**没有提供基准测试、准确率、吞吐量、延迟或用户实验等定量结果**。
- 最强的具体主张是该 SDK 已公开提供完整公共接口面：至少包含 **13 个 canonical routes**，覆盖文档创建、状态读取、快照、编辑、ops、presence、事件以及 agent bridge 能力。
- 功能上声明支持 **4 类核心能力**：协作 Markdown 编辑、溯源跟踪、实时协作服务器、代理 HTTP 桥接。
- 代理侧接口至少覆盖 **6 类交互**：state、marks、comments、suggestions、rewrite、presence，可支撑外部自动化或 agent 参与文档协作。
- 工程交付上，仓库包含示例应用（`apps/proof-example`）和多个基础包，运行要求为 **Node.js 18+**，并可通过本地 editor `:3000` 与 API/server `:4000` 启动完整系统。

## Link
- [https://github.com/everyinc/proof-sdk](https://github.com/everyinc/proof-sdk)
