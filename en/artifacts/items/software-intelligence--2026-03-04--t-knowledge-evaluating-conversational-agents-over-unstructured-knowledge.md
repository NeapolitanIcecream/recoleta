---
source: arxiv
url: http://arxiv.org/abs/2603.04370v1
published_at: '2026-03-04T18:34:47'
authors:
- Quan Shi
- Alexandra Zytek
- Pedram Razavi
- Karthik Narasimhan
- Victor Barres
topics:
- agent-benchmark
- knowledge-grounding
- conversational-agents
- tool-use
- retrieval-augmented-generation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# $τ$-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge

## Summary
This paper introduces **τ-Knowledge**, a benchmark for evaluating conversational agents over unstructured knowledge bases, and adds a new financial customer support scenario, **τ-Banking**. It focuses on testing whether agents can simultaneously perform document retrieval, policy reasoning, tool discovery, and state modification in long-horizon conversations, rather than only doing isolated retrieval or isolated tool use.

## Problem
- Existing benchmarks usually evaluate **retrieval** and **tool use** separately, making it difficult to reflect the integrated challenge of “conversing while searching a private knowledge base and executing operations” in real enterprise settings.
- In high-risk applications such as customer support and finance, agents must not only find the correct documents, but also understand complex policies, discover available tools, and make **verifiable and compliant** state changes; this directly affects correctness, latency, and user trust.
- Real environments often involve unclear goals, shifting user intent, private knowledge bases, and out-of-distribution terminology, so simply using traditional RAG to retrieve relevant documents is not sufficient to complete tasks.

## Approach
- The authors extend τ-Bench to build **τ-Knowledge / τ-Banking**: a partially observable conversational environment simulating financial customer support, where task success is determined by whether the final database state is correct.
- The knowledge base contains about **698 documents / 194,562 tokens / 21 product categories / 51 discoverable tools**; agents must obtain policies, procedures, product information, and tool instructions from natural-language documents.
- They design **discoverable tools**: some tools are initially invisible to the agent, and can only be invoked after the agent finds documentation for them in the knowledge base.
- The benchmark supports multiple knowledge access methods while remaining retrieval-mechanism-agnostic: **dense retrieval, BM25 sparse retrieval, terminal/filesystem search, direct gold document access**, allowing errors from “finding knowledge” and “using knowledge” to be distinguished.
- Data construction uses a “**structured specification → unstructured documents**” pipeline, combined with human review, to generate **97 tasks**; each task requires an average of **18.6** documents and **9.52** tool calls.

## Results
- Overall difficulty is high: across all models and retrieval configurations, the best result is only **25.52% pass^1**, achieved by **GPT-5.2 (high) + Terminal**.
- Reliability declines noticeably under repeated trials: the paper reports that the best system reaches only **13.40% pass^4** at most, indicating insufficient stability when the same task is run multiple times.
- Even when retrieval bottlenecks are removed, performance remains limited: under the **Gold** condition, the strongest result is **Claude-4.5-Opus (high) = 39.69% pass^1**, showing that the problem is not just “failing to find documents,” but also includes policy reasoning, cross-document dependencies, and state tracking.
- Average performance by retrieval method (pass^1) is: **Gold 32.18%**, **Terminal 19.20%**, **Qwen3-emb-8b 17.11%**, **BM25 17.04%**, **text-embedding-3-large 16.88%**; Terminal outperforms standard retrieval on average, but still falls far short of Gold.
- A representative comparison: **Claude-4.5-Opus (high)** achieves **39.69%** on Gold, drops to **24.74%** with Terminal, and reaches only **18.30%** with text-embedding-3-large; this shows that retrieval noise causes a loss of **14.9–21.4 percentage points**.
- In terms of efficiency, **GPT-5.2 (high) + Terminal** and **Claude-4.5-Opus (high)** perform similarly, but the former requires about **1.7× more tokens, 2.3× more shell commands, and 9× longer completion time**; the paper therefore emphasizes that both success rate and solution efficiency should be measured.

## Link
- [http://arxiv.org/abs/2603.04370v1](http://arxiv.org/abs/2603.04370v1)
