---
source: arxiv
url: http://arxiv.org/abs/2603.06358v1
published_at: '2026-03-06T15:09:40'
authors:
- Yang Liu
- Li Zhang
- Fang Liu
- Ping Lin
- Xinyi Li
topics:
- context-management
- benchmark
- code-assistant
- repository-level
- long-horizon-dialogue
- memory-system
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# A Scalable Benchmark for Repository-Oriented Long-Horizon Conversational Context Management

## Summary
This paper introduces **LoCoEval**, the first long-horizon multi-turn conversational context management benchmark for code repository development scenarios, designed to evaluate whether code assistants can still remember and correctly use critical information in ultra-long conversations. The authors also propose a repository-aware memory method, **Mem0^R**, to unify the management of conversational information and repository information.

## Problem
- Conversations in code repository development often span dozens to over a hundred turns, with requirements evolving, progressing in parallel, and mixed with noise, causing LLMs to easily lose critical early information.
- Existing context management methods are mostly designed for general-purpose chat and are not well suited to scenarios with strong coupling between “conversational context + repository code/text,” which limits the effectiveness of code assistants in real repository development.
- This area lacks a reliable benchmark, making it difficult for researchers to systematically evaluate whether models can correctly recall, retrieve, and answer questions in repository-level long conversations of 64K~256K tokens.

## Approach
- The authors construct **LoCoEval**: an automated benchmark for repository-oriented long-horizon conversation, built on the existing repository-level function-generation dataset DevEval.
- The benchmark uses an LLM-driven pipeline to generate realistic conversations: it first extracts “key information items” from the reference implementation of target functions, then deliberately creates some “distractor information,” and distributes this information across multiple user queries to simulate iterative requirements, noisy input, and retrospective questioning.
- To ensure the evaluation truly depends on conversation rather than only repository retrieval, the authors first filter out samples that “can be solved using repository RAG alone”; in total, 788 out of 1,825 DevEval samples are removed.
- LoCoEval contains **128** samples, **2** subsets (single-hop / multi-hop), and **3** task types (topic awareness, information item extraction, function generation); each sample has an average of **2.5** requirements, about **50** conversational turns, and total context length of about **64K~256K** tokens.
- Methodologically, the authors propose **Mem0^R**: an extension of Mem0 for repository scenarios that writes conversational history and repository information into a unified memory and supports context-aware repository retrieval.

## Results
- In terms of benchmark scale and setup, LoCoEval includes **128 samples / 768 tasks / 37 repos**, with each sample containing **30~70 turns**, **1~4 requirements**, and **64K~256K tokens**.
- The experiments cover **7** baseline methods (including **4** representative context management method categories) and **3** advanced backbone LLMs, indicating a relatively comprehensive comparison range.
- The authors explicitly claim that even with preliminary RAG adaptation, **standalone LLMs** and existing general-purpose context management methods still face “substantial challenges” in repository-oriented long-horizon conversations, especially **memory systems**, which make insufficient use of repository information.
- The authors further claim that **Mem0^R** outperforms all non-Oracle baselines overall and is more robust; the passage does not provide specific scores, Pass@k values, or relative percentage improvements, so it is not possible to list precise benchmark comparisons.
- An additional strongest concrete takeaway is that context management in repository development scenarios cannot only remember the conversation; it must jointly model repository code/text together with the conversation. This is the core reason the authors give for why existing methods fail and why Mem0^R has an advantage.

## Link
- [http://arxiv.org/abs/2603.06358v1](http://arxiv.org/abs/2603.06358v1)
