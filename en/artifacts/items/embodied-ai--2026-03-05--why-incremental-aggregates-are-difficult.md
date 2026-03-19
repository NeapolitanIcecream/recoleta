---
source: hn
url: https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1
published_at: '2026-03-05T23:56:24'
authors:
- gz09
topics:
- incremental-view-maintenance
- sql-aggregation
- stream-processing
- z-sets
- dbsp
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Why incremental aggregates are difficult

## Summary
This article explains why incremental aggregation in SQL is not as simple as “maintaining a running total,” especially when aggregation appears in composable query plans. The core point is that aggregation produces deletion updates, which requires the entire query engine to handle inserts and deletes uniformly, rather than only processing newly added data.

## Problem
- The problem it addresses is: **when underlying tables change, how can SQL views that include aggregation be maintained efficiently without fully recomputing the entire table or the whole query pipeline**.
- This matters because SQL queries are composable; even if a single aggregate view `V` can be maintained incrementally, a downstream view `L` that depends on it may still be unable to continue incremental updates because aggregation generates “old value deletions.”
- Traditional query engines are usually better at handling monotone operators, but non-monotone operations such as aggregation and `EXCEPT` can produce output deletions even when the input only receives inserts, making incremental maintenance difficult.

## Approach
- The article uses the simplest possible example to show that the initial computation of `SUM(salary)` is an `O(n)` aggregation over all rows, but once the view already exists, the ideal behavior when a new row is inserted is to update only the delta rather than rescan the full table.
- The core mechanism in Feldera/DBSP is to represent **data and data changes uniformly as Z-sets**: each row carries an integer weight, where `+1` denotes an insertion and `-1` denotes a deletion.
- In this model, view updates do not mean “emit only the new result,” but instead simultaneously **retract the old aggregate result** and **insert the new aggregate result**; for example, when the total sum changes, the output contains `-1` for the old sum and `+1` for the new sum.
- All query operators are evaluated uniformly over Z-sets, so deletions produced by upstream aggregation can continue propagating to downstream queries; this enables incremental maintenance for complex composed queries as well.
- The article further points out that the difficulty is not in some local optimization, but in the fact that **all operators in the entire execution engine must support negative updates**, which is also why standard engines find it hard to add this after the fact.

## Results
- The article **does not provide benchmark experiments, datasets, or systematic quantitative metrics**, so there are no reportable accuracy, throughput, latency, or relative improvement numbers.
- The complexity conclusion given is that ordinary full `SUM` requires scanning all input rows, with complexity **`O(n)`**; the goal of incremental maintenance is to process only the changed portion rather than rescanning all data.
- In the example, table `T` initially has two salary rows, `100` and `115`, and the aggregate result is **`215`**; after inserting `120`, the new total becomes **`345`**.
- Under Feldera’s Z-set semantics, a view update is not a single new value but two changes: **delete the old result (weight `-1`) and insert the new result (weight `+1`)**. This is the key concrete claim that allows incremental aggregation changes to propagate to downstream queries.
- The article claims that one of the main contributions of its underlying theory, **DBSP**, is to **handle inserts and deletes uniformly** through Z-sets, thereby supporting incremental view maintenance for complex queries containing non-monotone operators such as aggregation; many traditional engines support only some update types and fall back to full recomputation when deletions arise.

## Link
- [https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1](https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1)
