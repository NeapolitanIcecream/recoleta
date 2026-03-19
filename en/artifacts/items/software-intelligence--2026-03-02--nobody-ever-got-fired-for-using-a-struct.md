---
source: hn
url: https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct
published_at: '2026-03-02T23:16:20'
authors:
- gz09
topics:
- rust-serialization
- database-systems
- storage-layout
- performance-optimization
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# Nobody ever got fired for using a struct

## Summary
This article analyzes a real performance regression case: when wide, sparse SQL rows with hundreds of nullable columns were mapped directly to Rust structs and serialized with rkyv, the on-disk representation bloated, causing increased I/O and reduced throughput. By changing per-field `Option<T>` to a bitmap plus raw values, and using a pointer-indexed layout for sparse rows, the author significantly reduced serialized size without changing the in-memory interface.

## Problem
- The problem addressed is: **wide tables (700+ nullable columns) suffer severe space waste and performance degradation under Rust/rkyv’s default struct serialization**, which matters because most of Feldera’s workloads are data streams that **do not fit in memory and must be spilled to disk frequently**.
- The in-memory Rust struct itself is not the main issue; the problem is primarily in the **on-disk / archived representation**: many `Option<T>` values are no longer “free” after serialization, especially `Option<ArchivedString>`, which explicitly stores discriminant information.
- When SQL schemas are nullable by default, tables are very wide, and data is sparse, the combination of **row-oriented storage + many nullable fields** turns a simple struct layout into a bottleneck.

## Approach
- The core idea is simple: **instead of storing the archived form of `Option<T>` separately for each field, first write a bitmap indicating which fields are present, then store only the field values themselves**.
- A generic helper trait `NoneUtils` is used to handle both `Option<T>` and plain `T`: during serialization, it first calls `is_none()` to decide the bitmap, then uses `unwrap_or_self()` to extract the raw value to write; during deserialization, it reconstructs `Some(...)` or the original value via `from_inner()`.
- This changes the layout from “each field carries its own Option overhead” into the conceptual form `| bitmap | field0 | field1 | ... |`, thereby eliminating the fixed extra cost of many nullable fields.
- For even sparser rows, it further uses a sparse layout: `| bitmap | ptrs | values... |`, storing only the **fields that are actually present** and indexing them with relative pointers, skipping all `NULL` fields.
- The system generates these serialization/deserialization routines automatically via macros and **chooses dense or sparse representation per row**, while preserving the original Rust struct’s in-memory interface.

## Results
- In the example 8-field struct, the **in-memory layout is 40B**, but after default rkyv archiving it becomes **88B**, i.e. **more than 2x larger**; the main reason is that each `Archived<Option<SqlString>>` string field takes **24B = 16B string + 8B Option discriminant/overhead**.
- The author notes that previously a string field that was `None` or an empty string would still consume **24B**, whereas after optimization it can require as little as **1 bit** in the best case to represent absence.
- In the real customer workload that triggered the issue, the **serialized row size was reduced by about 2x**.
- Because row size shrank, **disk I/O decreased accordingly**, and **throughput returned to the level the customer expected**; the article does not provide more detailed absolute throughput numbers, dataset sizes, or quantitative comparisons with other systems.
- The strongest practical takeaway is: for scenarios with **hundreds of nullable columns + small strings / sparse data + row-oriented storage**, changing the serialization data layout is more important than continuing to rely on an ordinary struct.

## Link
- [https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct](https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct)
