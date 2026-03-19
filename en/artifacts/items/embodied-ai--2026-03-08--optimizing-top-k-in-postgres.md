---
source: hn
url: https://www.paradedb.com/blog/optimizing-top-k
published_at: '2026-03-08T22:54:17'
authors:
- philippemnoel
topics:
- postgresql
- top-k-query
- inverted-index
- columnar-storage
- block-wand
- full-text-search
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Optimizing Top K in Postgres

## Summary
This article analyzes why PostgreSQL often degrades on Top K queries that combine filtering, sorting, and full-text search, and introduces how ParadeDB/Tantivy significantly accelerates this type of query using a single composite index and early pruning. The core idea is: rather than prebuilding different B-Trees for every query shape, make scanning, filtering, and selecting Top K cheap enough by themselves.

## Problem
- The problem to solve is how to efficiently return the “top K results after applying conditions” on very large-scale data, especially for queries that simultaneously include filtering, sorting, and text relevance scoring.
- This matters because Top K is a fundamental access pattern in production databases; if execution cost worsens with combinations of filters and sort orders, the system suffers from high latency, index bloat, and slower writes.
- PostgreSQL’s issue is that B-Trees are fast for a single known query shape, but when faced with additional filters, different sort keys, or GIN full-text search, it often has to scan large numbers of candidates, fetch rows from the heap, and then re-sort, with worst-case performance degrading from milliseconds to tens of seconds.

## Approach
- The core method is to use a **single composite search index** instead of “multiple B-Tree/GIN combinations tailored to specific query shapes.” This index puts searchable, filterable, and sortable fields into the same index and links them with a unified internal doc ID.
- Text search uses an **inverted index** to produce candidate doc IDs; numeric/categorical filters and sort-related fields are stored in **columnar arrays**, accessed with `column[row_id]` for O(1) random access, avoiding PostgreSQL’s repeated heap lookups for entire rows across massive candidate sets.
- For boolean filters, the system directly intersects doc ID streams and uses column min/max metadata plus batch processing/SIMD to skip data blocks that cannot possibly satisfy the conditions, keeping filtering cost as low as possible.
- For Top K sorted by relevance score, it uses **Block WAND**: maintain the current Top K threshold, and if a document block’s theoretical maximum score cannot reach that threshold, skip the whole block instead of scoring documents one by one.
- The article also mentions an upstream Tantivy improvement: in boolean AND queries, using a cheaper membership check instead of frequently advancing iterators with `seek`, further improving performance for some Top K queries.

## Results
- On a 100M-row table, for the simple query `ORDER BY timestamp DESC LIMIT 10`: **about 15 seconds without an index**; after adding a single-column B-Tree, it drops to **about 5ms**, showing that PostgreSQL is very strong when the “query shape exactly matches the index.”
- But after adding a filter, `WHERE severity < 3 ORDER BY timestamp DESC LIMIT 10`, if the index does not match, PostgreSQL may degrade again to **a worst case of about 15 seconds**; this shows its performance is highly sensitive to query shape.
- For a query with full-text search + filtering + sorting by relevance, in PostgreSQL, even with precomputed `tsvector` and a GIN index, execution time is still about **37 seconds**; after creating a **partial GIN index** for `WHERE severity < 3`, it is still about **33 seconds**, because the candidate set remains huge.
- The `EXPLAIN ANALYZE` shown in the article indicates that PostgreSQL actually processed **10,000,000 rows** of candidates for this query, with execution time **33,813.810 ms**; the corresponding ParadeDB approach ran in **299.393 ms**, about **113x** faster.
- The corresponding ParadeDB query `WHERE severity < 3 AND message ||| 'research team' ORDER BY pdb.score(id) DESC LIMIT 10` can be reduced to **about 300ms**, mainly because of single-index execution, low-cost filtering, and early pruning with Block WAND; the execution plan shows only **10 Heap Fetches**.
- On another 100M-row benchmark query, `WHERE message === 'research' AND country === 'Canada' ORDER BY severity, timestamp LIMIT 10`, ParadeDB 0.21.0, with the help of an upstream Tantivy improvement, reduced runtime from **90ms to 70ms**, an improvement of about **22%**; the article also claims that some Top K benchmarks can improve by as much as **30%**.

## Link
- [https://www.paradedb.com/blog/optimizing-top-k](https://www.paradedb.com/blog/optimizing-top-k)
