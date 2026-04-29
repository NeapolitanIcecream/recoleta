---
source: arxiv
url: http://arxiv.org/abs/2604.21746v1
published_at: '2026-04-23T14:51:18'
authors:
- Krishna Narasimhan
topics:
- static-analysis
- llm-evaluation
- code-intelligence
- domain-specific-language
- agentic-systems
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Less Is More: Measuring How LLM Involvement affects Chatbot Accuracy in Static Analysis

## Summary
This paper studies how much control a static-analysis chatbot should give to an LLM when translating natural-language requests into Joern CPGQL queries. A schema-bound JSON intermediate works better than direct query generation and better than an agentic tool loop on this benchmark.

## Problem
- The paper targets natural-language access to static analysis tools, where users ask for code analysis in plain English but the system must produce correct queries in Joern's CPGQL DSL.
- This matters because static analysis tools are useful but hard to use; writing CPGQL requires DSL knowledge, graph-traversal semantics, and schema knowledge that many developers do not have.
- Prior systems vary in how much work they give to the LLM, but they do not isolate "degree of LLM involvement" as the variable being tested.

## Approach
- The authors compare three architectures for the same task: **A1 direct generation** of CPGQL, **A2 structured intermediate** generation of schema-valid JSON that a deterministic mapper converts to CPGQL, and **A3 agentic tool use** with a ReAct-style loop over analysis tools.
- The core mechanism in A2 is simple: the LLM fills a small typed JSON form with fields such as query type, source, sink, and output columns, and ordinary code builds the final Joern query. The LLM never writes CPGQL syntax.
- They evaluate these designs on a new benchmark of **20 code-analysis tasks** across **3 tiers**: structural, data-flow, and composite queries, over **Apache Commons Lang** and **OWASP WebGoat**.
- The experiment uses **4 open-weight models** in a **2×2 design**: Llama 3.3 70B, Llama 3.1 8B, Qwen 2.5 72B, and Qwen 2.5 7B, with **3 repetitions** each. The paper reports **720 planned trials** and **660 usable trials** after excluding many A3/Llama-70B infrastructure failures.

## Results
- **A2 gives the best result-match rate for every tested model.** On large models, it beats A1 by **+15.0 percentage points** for **Qwen 72B** (**58.3% vs 43.3%**) and **+25.0 points** for **Llama 70B** (**55.0% vs 30.0%**).
- On small models, A2 still beats A1, but by less: **Qwen 7B** improves from **31.7% to 35.0%** (**+3.3 points**) and **Llama 8B** improves from **30.0% to 35.0%** (**+5.0 points**).
- **A3 performs worst** on the reported models despite much higher cost. Result match is **25.0%** for **Qwen 72B**, **15.0%** for **Qwen 7B**, and **15.0%** for **Llama 8B**. The abstract says A3 uses about **8× more tokens per task** than A2.
- A2's gain depends on model size. Its execution success is **100%** on **Qwen 72B** and **Llama 70B**, but drops to **65.0%** on **Qwen 7B** and **53.3%** on **Llama 8B**, showing that small models often fail JSON parsing or schema validation.
- A1 has high execution success across models, at **98.3% to 100%**, but lower result correctness than A2. That means direct CPGQL generation often runs, yet still returns the wrong analysis output.
- The main claim is that, for a formal domain like static analysis, the best split is: let the LLM interpret the request into a typed intermediate, then let deterministic code build and run the final query.

## Link
- [http://arxiv.org/abs/2604.21746v1](http://arxiv.org/abs/2604.21746v1)
