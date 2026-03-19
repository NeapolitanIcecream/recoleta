---
source: hn
url: https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1
published_at: '2026-03-05T23:56:24'
authors:
- gz09
topics:
- incremental-view-maintenance
- stream-processing
- sql-aggregates
- z-sets
- query-engines
relevance_score: 0.47
run_id: materialize-outputs
language_code: en
---

# Why incremental aggregates are difficult

## Summary
This article explains why incremental aggregation in SQL is not simple in real query plans, especially when aggregation results continue to participate in subsequent queries. The core point is: aggregation produces deletion updates, so an execution model is needed that can uniformly represent both inserts and deletes.

## Problem
- The problem to solve is: when underlying tables change, how can views containing aggregations such as `SUM`/`GROUP BY` be maintained efficiently, instead of being fully recomputed each time.
- This matters because complex SQL queries are usually composable; once aggregation results are used by downstream queries, updates are no longer as simple as just “adding the new value.”
- Traditional query engines can often perform incremental maintenance only for some updates; when faced with deletes or non-monotonic operators, they tend to fall back to full recomputation, hurting streaming and continuous computation performance.

## Approach
- The article uses the simplest example to show that the initial computation of an ordinary `SUM` scans all rows, with complexity `O(n)`; but for view maintenance, in theory it can use the old result and process only the changed portion.
- The core mechanism of Feldera/DBSP is **Z-sets**: representing a table as “row + integer weight,” where positive weights indicate inserts and negative weights indicate deletes, thereby unifying data and data changes into the same representation.
- In this model, an aggregation update does not output only the new value; it outputs both “delete the old aggregate result” and “insert the new aggregate result.” For example, when the total sum changes, the view delta will contain an old value with `-1` and a new value with `+1`.
- All query operators must uniformly accept positive and negative changes; only then can downstream operators continue propagating the deletion updates produced by aggregation and support incremental maintenance of compositional queries.
- The article emphasizes that aggregation and operators such as `EXCEPT` are **non-monotonic**: even if the input contains only inserts, the output may still contain deletes. This is exactly the root reason standard engines are difficult to adapt.

## Results
- The article does not provide quantitative results such as benchmark tests, experimental data, or accuracy metrics.
- The explicit complexity conclusion given is that the initial execution of a conventional aggregation must examine all input rows, with complexity `O(n)`.
- It uses an example to illustrate incremental maintenance behavior: when table `T` initially has two salary rows, `100` and `115`, `SUM=215`; after inserting `120`, the new total becomes `345`.
- The key mechanistic result is that for updates to an aggregate view, the system must emit two changes—delete the old result and insert the new result—rather than just sending a new value.
- The article claims that the breakthrough of DBSP/Feldera is using Z-sets to handle inserts and deletes uniformly, enabling consistent incremental maintenance for arbitrary mixed updates and compositional queries containing aggregation; by contrast, many traditional engines can support only some update types.

## Link
- [https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1](https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1)
