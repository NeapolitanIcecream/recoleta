---
source: hn
url: https://www.paradedb.com/blog/optimizing-top-k
published_at: '2026-03-08T22:54:17'
authors:
- philippemnoel
topics:
- postgresql
- top-k-query
- full-text-search
- inverted-index
- columnar-execution
- block-wand
relevance_score: 0.39
run_id: materialize-outputs
language_code: en
---

# Optimizing Top K in Postgres

## Summary
This article analyzes Postgres’ strengths and bottlenecks for Top K queries, especially why performance deteriorates sharply when filters and full-text search are involved. The author further explains how ParadeDB/Tantivy use a unified composite index, columnar storage, and Block WAND pruning to keep Top K latency consistently low across more query shapes.

## Problem
- The problem to solve is: how to efficiently execute Top K queries on massive datasets that involve **filtering, sorting, and full-text-search relevance scoring**, not just the simplest `ORDER BY ... LIMIT K`.
- This matters because Top K queries in production are usually not simple single-column sorts; they often combine multiple filters, text search, and dynamic ordering. If execution degrades into scanning/sorting a large candidate set, query time can jump from milliseconds to seconds or worse.
- Postgres’ B-Tree performs extremely well only when the index closely matches the query shape. Once filter conditions are not in the index, or when combining GIN text search with sorting, problems arise such as difficulty composing indexes, oversized candidate sets, and expensive heap fetches.

## Approach
- The core idea is: **do not rely on prebuilding many sets of B-Tree indexes for every possible query shape**. Instead, place searchable, filterable, and sortable fields into one unified composite index, so different kinds of Top K queries can complete most of their work within the same index.
- The index combines two structures: an **inverted index** produces doc ID streams for text matching, while **columnar arrays** provide O(1) random access for filtering and reading sort fields for those doc IDs, avoiding Postgres-style row-by-row heap fetches over massive candidate sets.
- For boolean filters (such as `country='US' AND severity<3`), the system simplifies evaluation into intersections of doc ID streams plus columnar value checks. Columns also carry min/max metadata and can perform range comparisons in batched vectorized (SIMD) fashion to reduce filtering cost.
- For Top K ranked by relevance, it uses **Block WAND**: maintain the current minimum score threshold for the Top K, estimate the maximum possible score for each block, and skip an entire block if its upper bound cannot make the Top K, instead of scoring documents one by one.
- The article also introduces an upstream Tantivy improvement: in boolean AND queries, replacing frequent iterator `seek` advances with cheaper doc ID membership checks, further accelerating some Top K queries.

## Results
- On a table with 100M rows, for the simplest `ORDER BY timestamp DESC LIMIT 10`: **about 15 seconds without an index**, dropping to **about 5ms** after building a B-Tree on `timestamp`, showing that Postgres is very strong when the index fully matches the query shape.
- After adding the filter `WHERE severity < 3 ORDER BY timestamp DESC LIMIT 10`, if the index does not match, Postgres can degrade in the worst case to **up to about 15 seconds**, showing that its Top K performance is highly sensitive to query shape.
- For a full-text-search + filter + relevance-sorted query, after optimizing with a generated `tsvector` column + GIN, Postgres still takes **about 37 seconds**; even with a partial GIN index adding `WHERE severity < 3`, it only improves to **about 33 seconds**, a limited gain. `EXPLAIN ANALYZE` shows about **10,000,000** candidate rows and total execution time of **33,813.810 ms**.
- The corresponding ParadeDB query `WHERE severity < 3 AND message ||| 'research team' ORDER BY pdb.score(id) DESC LIMIT 10` drops to **about 300ms** on a similar 100M-row benchmark; the provided execution plan shows total time of **299.393 ms** and only **Heap Fetches: 10**.
- The article argues that this gap comes from the unified index avoiding massive heap fetches, cheaper columnar filtering, and early pruning of large candidate sets via Block WAND. The point is not to beat one specific optimal B-Tree path, but to keep more query shapes within low-variance, acceptable latency.
- Another concrete improvement is ParadeDB 0.21.0: performance for some Top K queries improves by **up to 30%**; the example query on 100M rows drops from **90ms to 70ms**.

## Link
- [https://www.paradedb.com/blog/optimizing-top-k](https://www.paradedb.com/blog/optimizing-top-k)
