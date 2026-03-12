---
source: hn
url: https://github.com/AlphaCorp-AI/RustyRAG
published_at: '2026-03-04T23:28:14'
authors:
- zer0tokens
topics:
- rag
- rust
- low-latency-inference
- contextual-retrieval
- vector-search
relevance_score: 0.9
run_id: materialize-outputs
---

# Show HN: RustyRAG lowest-latency open-source RAG on GitHub

## Summary
RustyRAG 是一个强调超低延迟的开源 RAG 系统，把文档摄取、检索和答案流式生成整合进单个 Rust 异步二进制中。其核心卖点是比常见 Python 微服务式 RAG 栈更低的请求开销，并支持 Groq/Cerebras 低延迟推理与本地嵌入。

## Problem
- 传统 RAG 系统常由多个 Python 微服务拼接而成，单次请求链路长、进程间开销高，导致首 token 延迟和整体响应时间偏高。
- 仅靠普通分块嵌入做检索，往往缺少文档级上下文，影响召回准确性和答案可溯源性。
- 工程上还需要同时解决 PDF/ZIP 文档摄取、页码保留、向量检索、流式输出和模型切换，系统集成复杂。

## Approach
- 将完整 RAG 流水线收敛为**一个 async Rust 二进制**：上传、抽取、语义分块、嵌入、入库、检索、生成全部在同一服务内完成，减少跨服务开销。
- 使用 **Actix-Web + SSE** 实现实时流式回答，先发送 sources 事件，再持续返回生成 token，以优化用户感知延迟（TTFT）。
- 检索侧采用 **contextual retrieval**：对每个 chunk 用 LLM 生成 1-2 句上下文前缀，再与 chunk 文本拼接后嵌入，让向量同时编码局部内容和文档上下文。
- 嵌入与检索采用 **本地 Jina embeddings v5 nano retrieval + Milvus HNSW**，并利用 passage/query 非对称检索；生成侧可按请求切换 **Groq 或 Cerebras** 模型。
- 文档处理支持 PDF/TXT/ZIP，保留页码、按句边界做语义分块，并对 ZIP 内文件并发处理与批量嵌入。

## Results
- 文中给出了**同一 977-PDF 语料库、同一模型（Cerebras qwen-3-235b-a22b-instruct-2507）**下的聊天 UI 演示，并展示 **TTFT（time to first token）和总响应时间**；但**未提供具体数值表、均值或与基线的量化对比**。
- 速度方面的最强具体主张是：RustyRAG 号称是 GitHub 上“**lowest-latency open-source RAG**”，并将低延迟归因于**单二进制 Rust 架构**以及 **Groq/Cerebras** 低延迟推理硬件。
- 检索质量方面的主张是：LLM 生成的 contextual prefix 可带来“**significantly better search accuracy**”，但本文摘录**没有报告准确率、召回率、nDCG、MTEB 子任务或对照实验数字**。
- 成本/效率方面给出的具体信息包括：使用 **jina-embeddings-v5-text-nano-retrieval**，向量维度为 **768-dim**，并强调其在小模型中有较高 **MTEB** 排名和良好 speed-to-quality ratio；但**未给出本系统内实测吞吐/成本数字**。

## Link
- [https://github.com/AlphaCorp-AI/RustyRAG](https://github.com/AlphaCorp-AI/RustyRAG)
