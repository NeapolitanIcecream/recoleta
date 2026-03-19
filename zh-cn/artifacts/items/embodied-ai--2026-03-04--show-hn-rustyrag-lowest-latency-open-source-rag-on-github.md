---
source: hn
url: https://github.com/AlphaCorp-AI/RustyRAG
published_at: '2026-03-04T23:28:14'
authors:
- zer0tokens
topics:
- rag-systems
- low-latency-inference
- rust
- vector-search
- contextual-retrieval
relevance_score: 0.06
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: RustyRAG lowest-latency open-source RAG on GitHub

## Summary
RustyRAG 是一个面向检索增强生成（RAG）的低延迟开源系统，把文档摄取、切块、向量检索和答案流式生成整合进一个异步 Rust 二进制。其主要卖点是减少传统 Python 微服务式 RAG 的请求开销，并通过上下文化检索与本地嵌入提升速度/精度权衡。

## Problem
- 传统 RAG 栈通常由多个 Python 微服务拼接而成，导致**每次请求开销高、首 token 延迟（TTFT）更慢**。
- 文档块只做浅层向量化时，**检索容易忽略块在整篇文档中的上下文角色**，影响命中质量与答案准确性。
- 部署上常见问题是组件分散、依赖复杂，**难以快速搭建一个支持 PDF、流式输出、来源引用的完整 RAG 服务**。

## Approach
- 将**上传、文本提取、语义切块、上下文化前缀生成、嵌入、Milvus 检索、LLM 流式回答**全部合并到一个 async Rust + Actix-Web 服务中，减少跨服务通信开销。
- 使用 **jina-embeddings-v5-text-nano-retrieval** 本地部署在 HuggingFace TEI 上，文档与查询分别用非对称检索任务类型进行嵌入，以获得更好的速度/成本比。
- 对每个 chunk 先让 LLM 结合**文档概览 + 邻近页滑窗**生成 1–2 句“上下文前缀”，再与 chunk 文本拼接后向量化，从而让向量同时编码局部内容和全局语义。
- 检索层采用 **Milvus HNSW + cosine similarity**；生成层支持 **Groq 和 Cerebras** 两类低延迟推理提供商，并通过 SSE 实时向客户端流式返回 token 与 sources。
- 文档摄取支持 **PDF/TXT/ZIP**，其中 ZIP 可并发处理，PDF 保留页码，便于最终来源归因。

## Results
- 文中声称是 **“GitHub 上最低延迟的开源 RAG”**，并展示了在**同一 977-PDF 语料、同一模型**下比较 **TTFT（time to first token）** 与总响应时间的演示界面，但**摘录中未给出具体数值、基线名称或完整实验表**。
- 系统支持使用 **Cerebras qwen-3-235b-a22b-instruct-2507** 进行带 **3 个来源** 的流式 RAG 响应演示，说明其面向大模型流式问答场景做了延迟优化。
- 嵌入模型使用 **768 维** 的 jina 小模型，并宣称其在 **MTEB** 上属于小模型中的高性能选择，具备较优的性能/成本比；但本文摘录**没有提供该系统自身在检索准确率上的量化提升数字**。
- 上下文化检索被描述为能带来 **“significantly better search accuracy”**，但**未提供准确率、召回率、nDCG 或与无前缀检索的定量对比**。
- 工程上给出的最强具体主张是：**单二进制部署、流式 SSE、并发 ZIP 摄取、本地嵌入、Milvus 2.4、Rust 1.70+**，重点创新更偏向系统实现与低延迟工程整合，而非新的学习算法基准突破。

## Link
- [https://github.com/AlphaCorp-AI/RustyRAG](https://github.com/AlphaCorp-AI/RustyRAG)
