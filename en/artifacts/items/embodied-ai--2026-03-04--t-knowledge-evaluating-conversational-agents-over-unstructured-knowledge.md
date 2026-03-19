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
- benchmarking
- conversational-agents
- retrieval-augmented-generation
- tool-use
- knowledge-grounding
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# $τ$-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge

## Summary
This paper introduces **τ-Knowledge**, a benchmark for evaluating conversational agents over unstructured knowledge bases, and adds a new financial customer support domain, **τ-Banking**. It emphasizes that agents must not only retrieve documents, but also correctly understand policies, discover available tools, and complete verifiable state changes across multi-turn conversations.

## Problem
- Existing benchmarks usually evaluate **retrieval** and **tool use** separately, making it hard to reflect the complex workflow in real deployments such as enterprise customer support, where agents must "consult knowledge while conversing, then execute actions."
- In private, unstructured, long-document knowledge bases, agents must handle **ambiguous user intent, complex internal policies, cross-document dependencies, and partially observable state**, which is far more difficult than standard QA or single-step tool calls.
- This matters because if real-world knowledge-intensive customer support systems make mistakes, it can lead to **incorrect account state changes, non-compliant decisions, inefficient interactions, and reduced user trust**.

## Approach
- The authors build a new benchmark, **τ-Knowledge**, in which the **τ-Banking** domain simulates real financial customer support: agents must query a knowledge base of about **698 documents / 194,562 tokens** over multi-turn conversations and modify the underlying banking database state through tools.
- The core mechanism is simple: **first find the rules and tool instructions in the documents, then call the tools according to those rules, and finally check whether the database state is correct**. In other words, the benchmark evaluates not just "can it find it," but "can it find it + understand it + do it correctly."
- It introduces **discoverable tools**: some tools are initially invisible to the agent and are only mentioned in documents; the agent must first retrieve the relevant instructions before it can call these tools that change the environment state.
- The benchmark remains open to different retrieval methods, supporting configurations such as **dense retrieval, BM25 sparse retrieval, terminal/filesystem search, and direct access to gold documents**, enabling comparison of different bottlenecks in "knowledge access" versus "knowledge use."
- For data construction, the authors use a **structured-to-unstructured** generation pipeline: they first generate consistent structured specifications for products, policies, and tools, then expand them into natural-language documents, and combine human review with task validation to ensure consistency and solvability.

## Results
- **The main results are very low**: the best system across all tested setups achieves only **25.52% pass^1**, corresponding to **GPT-5.2 (high reasoning) + Terminal**; this shows that current frontier models are still clearly inadequate on this kind of realistic knowledge-driven dialogue task.
- **Reliability degrades quickly**: the authors note that even the best configuration reaches at most **13.40% pass^4**, showing unstable success rates when the same task is run repeatedly and generally weak robustness.
- Even when the retrieval bottleneck is removed and the required documents are provided directly (the **Gold** setting), the best result is still only **39.69% pass^1** (**Claude-4.5-Opus, high**), indicating that the problem is not just retrieval, but also **policy understanding, cross-document reasoning, and state tracking**.
- Looking at average results, **pass^1** by retrieval method is: **Gold 32.18%**, **Terminal 19.20%**, **Qwen3-emb-8b 17.11%**, **BM25 17.04%**, and **text-embedding-3-large 16.88%**; Terminal performs best overall, but is still far below Gold.
- A representative comparison: **Claude-4.5-Opus (high)** reaches **39.69%** under **Gold**, drops to **24.74%** with **Terminal**, and falls further to just **18.30% / 19.59%** under **dense retrieval**; this shows that retrieval configuration can cause a substantial loss of **about 15–21 points**.
- In terms of efficiency, the paper claims that **GPT-5.2 (high) + Terminal** performs similarly to **Claude-4.5-Opus (high)**, but the former requires about **1.7× tokens, 2.3× shell commands, and 9× longer runtime**, suggesting that current systems often compensate for limited capability through more searching and trial and error.

## Link
- [http://arxiv.org/abs/2603.04370v1](http://arxiv.org/abs/2603.04370v1)
