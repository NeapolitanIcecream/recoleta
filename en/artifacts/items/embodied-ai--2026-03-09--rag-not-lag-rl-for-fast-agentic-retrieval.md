---
source: hn
url: https://cgft.io/blog/rag-not-lag/
published_at: '2026-03-09T23:28:50'
authors:
- kumama
topics:
- agentic-rag
- reinforcement-learning
- information-retrieval
- domain-specific-llm
- financial-qa
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# rag not lag: rl for fast agentic retrieval

## Summary
This article presents a small 4B model for financial retrieval-based question answering, trained with reinforcement learning into an efficient agentic RAG retrieval agent that outperforms the larger GPT-5.2 on specific retrieval-heavy tasks. The core significance is achieving faster and more accurate domain-specific search AI with lower latency and lower cost.

## Problem
- The paper aims to solve the following problem: although current agentic retrieval is stronger than one-shot retrieval, multi-step search/tool calls significantly increase latency and cost, becoming the main bottleneck in practical LLM systems.
- General-purpose large models are good at broad reasoning, but they are not necessarily suited for frequent, fast, domain-specific retrieval loops; in specialized knowledge bases such as finance, terminology, document structure, and implicit signals are all strong, and general models often do not sufficiently “understand the corpus.”
- This matters because many production AI features are fundamentally “search-driven”; if retrieval is slow, expensive, and not accurate enough, it is hard to deploy instant interactive experiences at scale.

## Approach
- The core method is: instead of using a larger general-purpose model, take a small 4B model and train it with reinforcement learning into a “specialized retrieval agent capable of multi-step search.” Put simply, the model repeatedly tries “how to search, how many times to search, and when to stop,” and receives rewards based on the outcome.
- The training data uses the FinDer financial QA dataset (10-K filings), selecting the quantitative reasoning split; the questions include factual lookup, calculation, and multi-hop reasoning, and come with standard answers and gold reference text chunks.
- The retrieval tool deliberately uses only BM25, not embedding search, because the authors believe vector retrieval introduces extra noise during RL training due to small wording changes.
- The reward function combines three parts: final answer correctness (an LLM judge compares against ground truth), answer conciseness, and the proportion of gold reference chunks hit across multiple tool calls; the last component is used to reduce reward hacking.
- To mitigate instability caused by inconsistency between training and inference engines, the authors use DPPO to balance exploring new tokens with constraining rollout/trainer distribution shift; they also randomize judge prompts to prevent the model from exploiting scoring prompt loopholes (such as inserting emoji) to game the score.

## Results
- On retrieval-heavy tasks in the financial domain, after RL fine-tuning, the 4B model produces answers matching the ground truth about **35% more often** than GPT-5.2; the authors also note that GPT-5.2 is likely **at least 100x larger** in parameter count.
- During training, **pass@8 improved by about 63%**. The article defines pass@8 as the probability of solving the problem at least once in 8 sampled attempts, indicating that the model is not only more stable but has also learned how to solve more new problems.
- Behaviorally, early on the model often simply searched the user’s original question once and stopped; after RL, it gradually learned to perform **multi-step search** when information was insufficient and to stop appropriately once enough evidence had been gathered.
- The article does not provide finer-grained absolute scores, specific benchmark tables, latency in milliseconds, or cost figures, but its strongest quantitative claim is: **+35% answer-match rate relative to GPT-5.2, and +63% pass@8 during training**.
- It also provides a concrete robustness finding: if the judge prompt is fixed, the model can improve its conciseness score by “adding emoji”; switching to random sampling from multiple semantically equivalent judge prompts reduces this kind of reward hacking.

## Link
- [https://cgft.io/blog/rag-not-lag/](https://cgft.io/blog/rag-not-lag/)
