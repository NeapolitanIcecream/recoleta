---
source: hn
url: https://www.together.ai/blog/using-llms-to-optimize-database-query-execution
published_at: '2026-04-11T22:27:08'
authors:
- matt_d
topics:
- database-query-optimization
- llm-for-systems
- query-planning
- code-intelligence
- datafusion
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# AI for Systems: Using LLMs to Optimize Database Query Execution

## Summary
This paper tests whether a large language model can improve database query execution by editing existing physical plans. It reports useful speedups and memory reductions in Apache DataFusion without changing the database engine.

## Problem
- Database optimizers often pick poor execution plans because cardinality estimates miss correlations in the data, such as predicates that are strongly related instead of independent.
- These row-count errors propagate into bad join orders, access paths, and operator choices, which hurts OLAP query latency and resource use.
- Fixing these cases by hand takes engineering effort, so a method that repairs plans automatically matters for real query workloads.

## Approach
- The authors build **DBPlanBench**, a harness that exposes Apache DataFusion physical plans to an LLM in a compact JSON form.
- They serialize the physical operator graph into a token-efficient schema, remove execution-irrelevant fields, and deduplicate file statistics; this cuts payload size by about **10x** versus native serialization.
- The LLM does not generate a whole plan from scratch. It proposes localized **JSON Patch (RFC 6902)** edits such as join reordering or join-side swaps, which lowers the chance of invalid plans.
- The system uses iterative search: generate candidate patches with **GPT-5**, validate them by execution, keep the ones that reduce latency, and then repeat from the improved plan.
- For scale transfer, it finds good plans on smaller benchmark instances such as **SF3** and rewrites them with a deterministic script so they run on larger instances such as **SF10** while preserving the structural edits.

## Results
- In a TPC-DS-derived case study, the LLM changed join order so a `d_year=2001` filter was applied earlier, pruning a sales fact table from **15.1 million** rows to **2.9 million** rows before later joins.
- That case study reports a **4.78x** query speedup.
- The same case reduced aggregate hash-table build time from **10.16 s** to **0.41 s** and build memory from **3.3 GB** to **411 MB**.
- On generated **TPC-H** and **TPC-DS** workloads, median speedups were around **1.1x to 1.2x**.
- Some complex multi-join queries improved more, with speedups up to **4.78x** and several others in the **1.5x to 1.7x** range.
- In the sampled datasets, **60.8%** of queries were improved by more than **5%**. For cross-scale transfer, every selected optimized plan from **SF3** was successfully transferred to **SF10**, and the paper says the speedups stayed close to the original ones.

## Link
- [https://www.together.ai/blog/using-llms-to-optimize-database-query-execution](https://www.together.ai/blog/using-llms-to-optimize-database-query-execution)
