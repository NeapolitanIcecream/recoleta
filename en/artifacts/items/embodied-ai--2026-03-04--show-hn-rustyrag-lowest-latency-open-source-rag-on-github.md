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
language_code: en
---

# Show HN: RustyRAG lowest-latency open-source RAG on GitHub

## Summary
RustyRAG is a low-latency open-source system for retrieval-augmented generation (RAG) that integrates document ingestion, chunking, vector retrieval, and streaming answer generation into a single async Rust binary. Its main selling point is reducing the per-request overhead of traditional Python microservice-style RAG, while improving the speed/accuracy tradeoff through contextual retrieval and local embeddings.

## Problem
- Traditional RAG stacks are typically stitched together from multiple Python microservices, resulting in **high per-request overhead and slower time to first token (TTFT)**.
- When document chunks are only vectorized superficially, **retrieval can easily miss each chunk’s contextual role within the full document**, hurting hit quality and answer accuracy.
- A common deployment issue is fragmented components and complex dependencies, making it **difficult to quickly set up a complete RAG service that supports PDFs, streaming output, and source citation**.

## Approach
- It combines **upload, text extraction, semantic chunking, contextual prefix generation, embedding, Milvus retrieval, and LLM streaming responses** into a single async Rust + Actix-Web service, reducing cross-service communication overhead.
- It uses **jina-embeddings-v5-text-nano-retrieval** deployed locally on HuggingFace TEI, embedding documents and queries with asymmetric retrieval task types to achieve a better speed/cost ratio.
- For each chunk, the LLM first generates a 1–2 sentence **context prefix** using a **document overview + neighboring-page sliding window**, then concatenates that prefix with the chunk text before vectorization, so the vector encodes both local content and global semantics.
- The retrieval layer uses **Milvus HNSW + cosine similarity**; the generation layer supports two low-latency inference providers, **Groq and Cerebras**, and streams tokens and sources back to the client in real time via SSE.
- Document ingestion supports **PDF/TXT/ZIP**, with ZIP processed concurrently and PDF page numbers preserved for final source attribution.

## Results
- The article claims it is the **“lowest-latency open-source RAG on GitHub”** and shows a demo UI comparing **TTFT (time to first token)** and total response time under the **same 977-PDF corpus and same model**, but **the excerpt does not provide specific numbers, baseline names, or a complete experiment table**.
- The system supports a streaming RAG demo using **Cerebras qwen-3-235b-a22b-instruct-2507** with **3 sources**, indicating that it is optimized for latency in large-model streaming QA scenarios.
- The embedding model is a **768-dimensional** small jina model, described as a high-performing choice among small models on **MTEB** with a strong performance/cost ratio; however, **the excerpt does not provide quantitative gains in retrieval accuracy for the system itself**.
- Contextual retrieval is described as delivering **“significantly better search accuracy”**, but **no quantitative comparison is provided for accuracy, recall, nDCG, or versus retrieval without prefixes**.
- The strongest concrete engineering claims presented are: **single-binary deployment, streaming SSE, concurrent ZIP ingestion, local embeddings, Milvus 2.4, Rust 1.70+**. The key innovation is therefore more about systems implementation and low-latency engineering integration than about a new learning-algorithm benchmark breakthrough.

## Link
- [https://github.com/AlphaCorp-AI/RustyRAG](https://github.com/AlphaCorp-AI/RustyRAG)
