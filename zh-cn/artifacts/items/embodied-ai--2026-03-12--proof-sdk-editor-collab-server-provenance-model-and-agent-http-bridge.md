---
source: hn
url: https://github.com/everyinc/proof-sdk
published_at: '2026-03-12T23:20:13'
authors:
- azhenley
topics:
- collaborative-editing
- markdown-editor
- provenance-tracking
- agent-interface
- realtime-server
relevance_score: 0.06
run_id: materialize-outputs
language_code: zh-CN
---

# Proof SDK: Editor, collab server, provenance model, and agent HTTP bridge

## Summary
Proof SDK 是一个开源协作文档基础设施，提供编辑器、实时协作服务、来源追踪模型以及面向智能体的 HTTP 桥接接口。它的目标是支撑可协作的 Markdown 文档编辑，并让外部 agent 能读取状态、提交编辑与交互事件。

## Problem
- 需要一个可嵌入的协作文档系统，同时支持实时多人编辑、评论/建议/改写等工作流。
- 传统编辑器或协作后端通常缺少**provenance tracking**（编辑来源与变更来历追踪），这会影响审计、协作透明度和 agent 参与。
- 若要让 AI/agent 直接参与文档协作，需要稳定公开的接口来访问文档状态、标记、presence 和事件。

## Approach
- 提供一套开源 SDK，包含四个核心部分：协作 Markdown 编辑器、实时协作服务器、provenance model，以及 agent HTTP bridge。
- 用公开的 HTTP 路由暴露文档生命周期与协作能力，例如创建文档、获取 state/snapshot、提交 edit/ops、同步 presence、处理 events。
- 为 agent 提供专门桥接接口，使其能够读取文档状态与 marks，并提交 comments、suggestions、rewrite 等操作。
- 通过模块化 package 组织实现（如 `doc-core`、`doc-editor`、`doc-server`、`doc-store-sqlite`、`agent-bridge`），并附带示例应用以便本地部署与集成。

## Results
- 文中**没有提供量化实验结果**，没有数据集、基线方法或性能指标对比。
- 最强的具体成果声明是发布了一个可运行的开源系统，覆盖 4 个核心能力：editor、collab server、provenance model、agent HTTP bridge。
- 公开 SDK surface 列出了多条规范路由，支持文档状态、快照、编辑、ops、presence、pending events、ack，以及 bridge 下的 state/marks/comments/suggestions/rewrite/presence。
- 工程可落地性方面，要求 Node.js 18+，可通过 `npm run dev` 与 `npm run serve` 本地启动，默认编辑器端口为 `3000`，API/server 端口为 `4000`。

## Link
- [https://github.com/everyinc/proof-sdk](https://github.com/everyinc/proof-sdk)
