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
论文提出了一种多租户智能体式 RAG 设计：只有在用户有权查看租户数据时，系统才会把这些数据放入提示词。该设计在 OGX 中实现；OGX 是一个兼容 OpenAI 的开源系统，用于服务器端检索、工具使用和多轮智能体执行。

## 问题
- 企业 RAG 和智能体系统常按语义相关性或关键词相关性对文档排序，因此当其他租户的数据匹配查询时，用户可能检索到这些数据。
- 客户端智能体循环可能绕过检索过滤器，调用未授权工具，或在多轮对话中携带已泄露的上下文。
- 这个问题影响企业部署，因为企业需要共享基础设施来控制成本，而共享检索、工具和模型服务可能暴露机密数据或受监管数据。

## 方法
- 核心机制是：在摄取阶段为每个文档分块添加租户和访问元数据，然后在检索前和检索过程中执行授权检查。
- 检索使用 ABAC 门控：搜索前进行资源级检查，搜索后使用分块级元数据过滤；支持谓词下推的后端可以在向量搜索内部应用租户过滤器。
- 工具执行、会话状态、审计日志和策略检查在服务器端运行，因此客户端可以选择任务，但不能控制安全关键循环。
- LLM 服务层在租户之间共享，因为该设计会在检索到的上下文进入提示词前完成隔离。
- OGX 将这些能力实现为兼容 OpenAI 的 API，覆盖 responses、vector stores、search、tools、conversations、safety、telemetry 和 Kubernetes 部署。

## 结果
- 论文报告的证据显示，未加门控的检索在跨租户探测中有 98–100% 会泄露跨租户数据。
- 在使用 ABAC 门控后，所示评估中的 Cross-Tenant Leakage Rate 和 Authorization Violation Rate 在客户端编排和服务器端编排两种模式下都降至 0%。
- 评估包含 6 个实验，基于一个 2×2 矩阵：客户端编排与服务器端编排，分别交叉未加门控检索与 ABAC 门控检索。
- 实验设置包括 3 个租户、总计 300 份文档、每个租户 100 份文档、每份文档约 512 个 token、300 个授权查询、300 个跨租户探测，以及 90 个提示注入探测。
- 论文称 ABAC 门控带来的开销可以忽略，但所给摘录没有包含准确的延迟或吞吐量数值。
- 共享推理将模型端点成本扩展从 O(N·M) 降至 O(M)，其中 N 是租户数量，M 是模型端点数量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05287v1](https://arxiv.org/abs/2605.05287v1)
