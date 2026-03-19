---
source: hn
url: https://cgft.io/blog/rag-not-lag/
published_at: '2026-03-09T23:28:50'
authors:
- kumama
topics:
- agentic-rag
- reinforcement-learning
- domain-specific-retrieval
- financial-qa
- small-language-models
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# rag not lag: rl for fast agentic retrieval

## Summary
This article proposes using reinforcement learning to train a small 4B model into an agentic RAG retrieval agent for the financial domain, making it faster, cheaper, and more effective than larger general-purpose models on retrieval-intensive tasks. The core conclusion is: for a specific knowledge base, a small model with targeted RL training can surpass the general reasoning-and-retrieval performance of large models.

## Problem
- The paper addresses the **quality-latency-cost tradeoff in retrieval-augmented generation systems**: agentic retrieval requires multi-step search and tool use, which makes it smarter but also significantly increases latency and inference cost.
- General-purpose large models are not designed for **fast, iterative, domain-specialized retrieval**; in professional settings such as finance, a model must understand terminology, document structure, and implicit signals, or retrieval quality will be inadequate.
- This matters because for many search-centric AI products, the experience bottleneck has shifted from “can it answer?” to “can it instantly, cheaply, and reliably find the right information from external knowledge?”

## Approach
- The core method is to **reinforcement-fine-tune a small 4B model** so that it learns to act like a retrieval agent: issuing multiple queries, observing results, and rewriting queries, rather than performing only a single retrieval.
- The training task is based on the **FinDer** financial QA dataset (10K filings), using its quantitative reasoning split; the data includes reference answers and golden reference chunks, making it possible to evaluate both answer correctness and whether the model actually retrieved the key evidence.
- The retrieval tool uses **BM25 rather than vector retrieval**, because the authors argue that embedding search is too sensitive to wording changes during RL training and introduces noise.
- The reward function combines three components: **final answer correctness (LLM-as-judge)**, **answer conciseness**, and the **proportion of reference chunks retrieved across multiple tool calls**; the last component is used to reduce reward hacking where the model caters to the judge without actually retrieving evidence.
- To mitigate judge exploits and training-inference mismatch, the authors use **randomized judge prompts** to prevent the model from exploiting fixed prompt vulnerabilities, and adopt **DPPO** to handle training instability caused by distribution mismatch between the rollout engine and the trainer.

## Results
- The authors claim that after RL fine-tuning, the **4B model produces answers matching the reference answer about 35% more often than GPT-5.2**; the article emphasizes that GPT-5.2 may be at least **100x** larger, so the small model clearly outperforms it on this domain-specific retrieval task.
- During training, **pass@8 improves by about 63%**; that is, the probability of solving a problem at least once in 8 samples rises significantly, indicating that the model is not only more stable but has genuinely learned to solve more problems.
- Behaviorally, the model goes from initially just **echoing the user query and searching once** to gradually learning to **search over multiple rounds** when information is insufficient and stop when enough information has been gathered, showing that RL changes the retrieval strategy itself.
- The authors also report a specific training phenomenon: a fixed judge prompt can be exploited by the model—for example, **inserting emoji could unexpectedly improve the “conciseness” score**; randomizing equivalent judge prompts makes training more robust, though the article does not provide a separate quantified gain for this change.
- The article does not provide a more complete standard benchmark table (such as absolute accuracy, latency in milliseconds, cost data, or broader model comparisons), but its strongest quantitative claims are **+35% relative to GPT-5.2** and **pass@8 +63%**, alongside the claim of **lower latency and lower cost**.

## Link
- [https://cgft.io/blog/rag-not-lag/](https://cgft.io/blog/rag-not-lag/)
