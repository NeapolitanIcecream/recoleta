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
- long-context-benchmark
- repository-oriented-llm
- context-management
- code-assistant-evaluation
- memory-system
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# A Scalable Benchmark for Repository-Oriented Long-Horizon Conversational Context Management

## Summary
This paper introduces **LoCoEval**, the first long-horizon conversational context management benchmark for code repository development scenarios, designed to evaluate whether code assistants can still correctly remember and use key information in ultra-long, multi-turn, noisy conversations. The authors also propose a simple improved method, **Mem0^R**, which jointly models conversational memory and repository information, outperforming existing general-purpose methods on this benchmark.

## Problem
- Real conversations in code repository development often span **dozens to hundreds of turns**, and involve iterative requirements, parallel tasks, follow-up questions, and noise. LLMs can easily lose critical information when the context becomes too long.
- Existing context management methods are mostly designed for **general-purpose chat** and do not specifically handle repository-oriented scenarios where “conversational information + repository code information” are tightly intertwined.
- The lack of a reliable benchmark prevents researchers from systematically answering whether models can correctly retain, retrieve, and use historical information in long-horizon repository conversations; this directly affects the usability and consistency of code assistants in real development workflows.

## Approach
- The authors construct **LoCoEval**: starting from an existing repository-level code generation dataset, they first extract the “information items” necessary to complete the target function, then disperse these items throughout long multi-turn conversations, and synthesize long-dialog evaluation samples in reverse.
- To simulate realistic and complex development processes, the benchmark explicitly includes patterns such as **iterative requirements, noisy information, retrospective questions, and parallel topics**, and has mock user queries and agent responses **generated dynamically** during evaluation.
- In terms of scale, LoCoEval contains **128 samples**, divided into **single-hop / multi-hop** subsets; each sample has an average of **2.5 requirements** and about **50 conversation turns**, with total context lengths reaching **64K–256K tokens**.
- The benchmark covers **3 task types**: topic awareness, information item extraction, function generation, to evaluate “what was remembered,” “whether key information can be extracted,” and “whether the code task can ultimately be completed correctly.”
- To address the mismatch of general memory systems in repository scenarios, the authors propose **Mem0^R**: writing **conversation history and repository information into a unified memory**, combined with repository retrieval relevant to the current context, to better recover the information needed to complete the task.

## Results
- LoCoEval is a clearly quantifiable benchmark: **2 subsets, 128 samples, 768 tasks, and 37 repositories** in total; each sample contains **30–70 turns** and **64K–256K tokens**.
- During construction, the authors filtered from **1,825** samples in DevEval and removed **788** samples that could be solved using repository retrieval alone, ensuring that the evaluation truly depends on context management ability in long-horizon conversations.
- The authors evaluate **7 baselines** (including **4 representative context management method types**) and **3 advanced backbone LLMs**; the conclusion is that **standalone LLMs** and existing **general-purpose context management methods** both face significant difficulties in long repository conversations, with **memory systems** performing especially poorly.
- The paper claims that **Mem0^R outperforms all baseline methods (excluding Oracle)** and shows better robustness; however, the provided excerpt **does not include specific scores, Pass@k values, dataset breakdown results, or relative improvement percentages**.
- The strongest empirical takeaway is not an absolute numerical breakthrough, but rather that **context management in repository scenarios cannot rely only on general conversational memory, and must jointly model conversational content and repository code information**.

## Link
- [http://arxiv.org/abs/2603.06358v1](http://arxiv.org/abs/2603.06358v1)
