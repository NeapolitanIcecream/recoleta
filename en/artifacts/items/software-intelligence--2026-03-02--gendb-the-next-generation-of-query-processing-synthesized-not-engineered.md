---
source: arxiv
url: http://arxiv.org/abs/2603.02081v1
published_at: '2026-03-02T17:03:43'
authors:
- Jiale Lao
- Immanuel Trummer
topics:
- llm-agents
- query-processing
- database-systems
- code-generation
- performance-optimization
relevance_score: 0.79
run_id: materialize-outputs
language_code: en
---

# GenDB: The Next Generation of Query Processing -- Synthesized, Not Engineered

## Summary
GenDB proposes a different approach from traditional database engines: instead of maintaining a general-purpose query executor through long-term engineering, it uses LLMs to directly synthesize execution code for each query. The paper demonstrates with a multi-agent prototype that this “generate a customized program for each query” approach can significantly outperform existing engines on OLAP benchmarks.

## Problem
- Traditional DBMSs are highly complex and difficult to extend; when facing new data types, new hardware, and new optimization techniques, they iterate slowly and incur high costs.
- General-purpose query engines must use fixed operator abstractions to handle arbitrary workloads, making it hard to aggressively optimize for specific data distributions, query patterns, and cache/hardware characteristics.
- This matters because analytical queries often recur; if specialized code can be generated for high-frequency queries, the generation cost can be amortized and performance can be significantly improved.

## Approach
- The core method is: for each input query, instead of relying on a large handwritten execution engine, an LLM-driven multi-agent system analyzes the data, workload, and hardware, then directly generates executable query code.
- The system is divided into several specialized agents: Workload Analyzer extracts structured features, Storage/Index Designer generates customized storage and indexes, Query Planner produces resource-aware plans, Code Generator outputs C++/Python code, and Query Optimizer iteratively improves based on runtime feedback.
- Put simply, it is like an “automatic database compiler + automatic tuner”: it first examines the specifics of the query and the machine, then writes the most suitable specialized program, rather than invoking a fixed set of general-purpose operators.
- The optimization mechanism emphasizes data awareness and hardware awareness, for example choosing aggregation strategies based on cardinality and cache hierarchy: for small groups it uses in-array structures in L1 cache directly, while for large groups it switches to hash structures suited to L2/L3; it also generates query-specific data structures and operator rewrite code.
- Correctness is currently validated mainly by comparing query results with those from traditional databases; if no ground-truth results are available, manual inspection of the generated code is recommended.

## Results
- On 5 representative queries from TPC-H (SF=10), GenDB has a total execution time of **214 ms**, which is **2.8×** faster than the two fastest baselines, **DuckDB 594 ms** and **Umbra 590 ms**, and **11.2×** faster than **ClickHouse**.
- On the newly constructed **SEC-EDGAR** benchmark, GenDB has a total execution time of **328 ms**, **5.0×** faster than **DuckDB** and **3.9×** faster than **Umbra**.
- On the complex query **TPC-H Q9** (five-table join + LIKE filter), GenDB takes **38 ms**, **6.1×** faster than DuckDB.
- Iterative optimization is highly effective: **TPC-H Q18** drops from **12,147 ms** to **74 ms** in round 1, an improvement of **163×**; **TPC-H Q6** reaches near-optimal **17 ms** already at round 0.
- On SEC-EDGAR, **Q4** drops from **1,410 ms** to **106 ms** (**13.3×**), and **Q6** drops from **1,121 ms** to **88 ms** (**12.7×**); moreover, Q6 surpasses all baselines by round 1.
- Ablation experiments show that the multi-agent setup outperforms a single agent: on TPC-H, multi-agent achieves **236 ms**, **1.2×** faster than the best single-agent guided setup at **281 ms**; on SEC-EDGAR, it is **2.3×** faster than guided at **752 ms** and **4.1×** faster than high-level at **1,325 ms**, while also costing less (TPC-H **$14.15 vs. $17.54**; SEC-EDGAR **$23.49 vs. $27.46**).

## Link
- [http://arxiv.org/abs/2603.02081v1](http://arxiv.org/abs/2603.02081v1)
