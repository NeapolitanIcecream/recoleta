---
source: arxiv
url: http://arxiv.org/abs/2603.02081v1
published_at: '2026-03-02T17:03:43'
authors:
- Jiale Lao
- Immanuel Trummer
topics:
- query-processing
- database-systems
- llm-code-generation
- agentic-systems
- olap
- system-optimization
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# GenDB: The Next Generation of Query Processing -- Synthesized, Not Engineered

## Summary
GenDB proposes an approach different from traditional database engines: instead of long-term manual engineering of a general-purpose executor, it uses an LLM to directly synthesize customized execution code for each query. The paper’s central claim is that this query-by-query, data-aware, hardware-aware generation approach can already significantly outperform existing top-tier query engines in OLAP scenarios.

## Problem
- Traditional DBMSs are highly complex and difficult to extend; when facing new data types, new hardware, and new optimization requirements, they evolve slowly and incur high engineering costs.
- Existing query-code generation methods based on templates/compilers have limited room for customization and usually do not understand specific data distributions, workload patterns, or hardware characteristics.
- This matters because analytical query performance directly affects data processing cost and latency, and in practice many queries are executed repeatedly, making it suitable to amortize generation cost.

## Approach
- Replace a fixed query-engine pipeline with a **multi-agent LLM system** that performs workload analysis, storage/index design, query planning, code generation, and iterative optimization in sequence.
- Inputs include schema, SQL or natural-language questions, underlying data, user goals/budget, and hardware resources; outputs are **one executable per query**, plus customized storage structures and indexes.
- The core mechanism is to first extract structured features such as column statistics, join patterns, filter selectivity, and SIMD/cache hierarchy, and then use them to generate **instance-optimized** storage layouts, operator algorithms, and C++ execution code.
- The system iteratively improves plans and implementations by running the generated code and reading feedback; correctness is currently validated mainly by comparing results against traditional databases, and if no ground truth exists, manual code review is recommended.
- One typical example is **cache-adaptive aggregation**: for low-cardinality group by, it directly uses arrays that fit in L1 cache; for very high cardinality, it switches to implementations adapted to L2/L3 or shared hash tables, reducing hashing, locking, and merge overhead.

## Results
- On 5 representative queries at **TPC-H SF=10**, GenDB’s total execution time is **214 ms**; compared with **DuckDB 594 ms** and **Umbra 590 ms**, it is **2.8×** faster; compared with ClickHouse, it is **11.2×** faster.
- On the newly constructed **SEC-EDGAR** benchmark, GenDB’s total time is **328 ms**; it is **5.0×** faster than **DuckDB** and **3.9×** faster than **Umbra**.
- On **TPC-H Q9** (5-table join + LIKE), GenDB takes **38 ms**, **6.1×** faster than DuckDB.
- Iterative optimization yields large gains: **TPC-H Q18** drops from **12,147 ms** to **74 ms** (round 1), a **163×** improvement; the reason is replacing a hash aggregation with severe cache thrashing by an index-aware sequential scan.
- On **SEC-EDGAR Q4**, runtime drops from **1,410 ms** to **106 ms** (3 rounds), a **13.3×** improvement; **Q6** drops from **1,121 ms** to **88 ms** (4 rounds), a **12.7×** improvement, and by round 1 it already surpasses all baselines.
- Ablation experiments show the multi-agent design outperforms a single agent: on TPC-H, **236 ms vs. 281 ms** (guided), **1.2×** faster; on SEC-EDGAR, compared with **752 ms** (guided) and **1,325 ms** (high-level), the multi-agent system is **2.3×** and **4.1×** faster respectively. At the same time, cost is lower: TPC-H **$14.15 vs. $17.54**, SEC-EDGAR **$23.49 vs. $27.46**.

## Link
- [http://arxiv.org/abs/2603.02081v1](http://arxiv.org/abs/2603.02081v1)
