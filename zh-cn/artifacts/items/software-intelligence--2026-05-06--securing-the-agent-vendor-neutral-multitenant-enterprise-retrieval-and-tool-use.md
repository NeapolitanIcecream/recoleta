---
source: arxiv
url: https://arxiv.org/abs/2605.05287v1
published_at: '2026-05-06T17:59:21'
authors:
- Francisco Javier Arceo
- Varsha Prasad Narsing
topics:
- agentic-rag
- multitenant-security
- access-control
- tool-use
- server-side-orchestration
- enterprise-ai
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# Securing the Agent: Vendor-Neutral, Multitenant Enterprise Retrieval and Tool Use

## Summary
## 摘要
论文提出了一种多租户 agentic RAG 设计，只有在用户有权限查看时，才会把租户数据放进提示词。它在 OGX 中实现了这一设计。OGX 是一个面向服务器端检索、工具使用和多轮 agent 执行的开源、兼容 OpenAI 的系统。

## 问题
- 企业 RAG 和 agent 系统常按语义相关性或关键词相关性对文档排序，所以当某个租户的数据与查询匹配时，用户可能检索到另一个租户的数据。
- 客户端侧的 agent 循环可能跳过检索过滤器，调用未授权工具，或在多轮对话中带入泄露的上下文。
- 这个问题很重要，因为企业需要共享基础设施来控制成本，但共享的检索、工具和模型服务会暴露机密或受监管数据。

## 方法
- 核心机制很直接：在摄入阶段给每个文档块打上租户和访问元数据标签，然后在检索前和检索中进行授权检查。
- 检索使用基于 ABAC 的门控，在搜索前做资源级检查，在搜索后做块级元数据过滤；支持谓词下推的后端可以在向量搜索内部应用租户过滤器。
- 工具执行、会话状态、审计日志和策略检查都在服务器端运行，所以客户端可以选择任务，但不能控制安全关键的循环。
- LLM 服务层在各租户之间共享，因为设计会先隔离检索到的上下文，再把它放进提示词。
- OGX 用 OpenAI 兼容 API 实现了响应、向量存储、搜索、工具、会话、安全、遥测和 Kubernetes 部署。

## 结果
- 按论文给出的证据，不加门控的检索会在 98% 到 100% 的跨租户探测中泄露跨租户数据。
- 在所示评估中，加入 ABAC 门控后，Cross-Tenant Leakage Rate 和 Authorization Violation Rate 都降到 0%，客户端和服务器端编排模式都是如此。
- 评估包含 6 个实验，覆盖一个 2×2 矩阵：客户端侧与服务器端编排，分别与不加门控和加 ABAC 门控的检索交叉组合。
- 该设置包括 3 个租户、总计 300 篇文档、每个租户 100 篇文档、每篇大约 512 个 token、300 个授权查询、300 个跨租户探测和 90 个提示注入探测。
- 论文声称 ABAC 门控带来的开销可以忽略，但给出的摘录没有包含精确的延迟或吞吐量数字。
- 共享推理把模型端点成本的扩展方式从 O(N·M) 降到 O(M)，其中 N 是租户数量，M 是模型端点数量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05287v1](https://arxiv.org/abs/2605.05287v1)
