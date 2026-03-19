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
language_code: en
---

# Show HN: RustyRAG lowest-latency open-source RAG on GitHub

## Summary
RustyRAG is an open-source RAG system focused on ultra-low latency, integrating document ingestion, retrieval, and answer streaming into a single async Rust binary. Its core selling point is lower per-request overhead than typical Python microservice-based RAG stacks, while supporting low-latency inference via Groq/Cerebras and local embeddings.

## Problem
- Traditional RAG systems are often stitched together from multiple Python microservices, resulting in long per-request paths and high inter-process overhead, which increases time to first token and overall response time.
- Retrieval based only on ordinary chunk embeddings often lacks document-level context, hurting recall accuracy and answer traceability.
- From an engineering perspective, systems must also simultaneously handle PDF/ZIP ingestion, page-number preservation, vector retrieval, streaming output, and model switching, making integration complex.

## Approach
- Collapse the full RAG pipeline into **one async Rust binary**: upload, extraction, semantic chunking, embedding, storage, retrieval, and generation all happen within the same service, reducing cross-service overhead.
- Use **Actix-Web + SSE** for real-time streaming responses: send a sources event first, then continuously return generated tokens to optimize perceived latency (TTFT).
- On the retrieval side, use **contextual retrieval**: for each chunk, have an LLM generate a 1–2 sentence contextual prefix, then concatenate it with the chunk text before embedding, so the vector encodes both local content and document context.
- For embedding and retrieval, use **local Jina embeddings v5 nano retrieval + Milvus HNSW**, and leverage asymmetric passage/query retrieval; on the generation side, requests can switch between **Groq or Cerebras** models.
- Document processing supports PDF/TXT/ZIP, preserves page numbers, performs semantic chunking along sentence boundaries, and processes files inside ZIP archives concurrently with batched embedding.

## Results
- The article includes a chat UI demo on the **same 977-PDF corpus and the same model (Cerebras qwen-3-235b-a22b-instruct-2507)**, and shows **TTFT (time to first token) and total response time**; however, it **does not provide a table of specific values, averages, or quantitative comparisons against baselines**.
- The strongest concrete speed claim is that RustyRAG is the “**lowest-latency open-source RAG**” on GitHub, attributing its low latency to the **single-binary Rust architecture** and **Groq/Cerebras** low-latency inference hardware.
- On retrieval quality, the claim is that LLM-generated contextual prefixes can deliver “**significantly better search accuracy**,” but the excerpt **does not report accuracy, recall, nDCG, MTEB subtasks, or controlled experiment numbers**.
- Specific cost/efficiency details given include the use of **jina-embeddings-v5-text-nano-retrieval**, a vector dimension of **768-dim**, and the claim that it has a high **MTEB** ranking among small models and a strong speed-to-quality ratio; however, **no measured throughput or cost figures for this system are provided**.

## Link
- [https://github.com/AlphaCorp-AI/RustyRAG](https://github.com/AlphaCorp-AI/RustyRAG)
