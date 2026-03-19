---
source: hn
url: https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct
published_at: '2026-03-02T23:16:20'
authors:
- gz09
topics:
- rust
- serialization
- data-layout
- sql-engines
- storage-optimization
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Nobody ever got fired for using a struct

## Summary
This article analyzes a real-world performance anomaly: a wide-table Rust struct is efficient in memory, but after being serialized to disk it bloats because of a large number of `Option` fields, slowing I/O and throughput. The author proposes keeping the in-memory struct interface while redesigning the archive format, using bitmaps and sparse storage to significantly compress row size and restore performance.

## Problem
- The article addresses the problem of **space usage and throughput degrading sharply when wide SQL tables (with hundreds of nullable columns) are serialized/persisted**; this matters because most datasets Feldera processes **do not fit in memory**, so disk I/O directly determines system performance.
- The root cause is not the memory layout of Rust structs, but that after `rkyv` archiving, types like `Option<ArchivedString>` **lose the “free Option” optimization**, so each nullable field must explicitly store extra discriminant information.
- In wide SQL tables with 700+ nullable fields, where many values are `NULL`/empty strings, naive struct serialization causes severe space waste, which in turn slows the entire data pipeline.

## Approach
- The core idea is simple: **instead of storing each field separately as `Option<T>`, store all the “is None” information together in a bitmap**; the value portion stores only the raw value `T`.
- During serialization, record 1 bit for each field first: `1` means the value is present, `0` means `None`; if present, then write the actual value. During deserialization, check the bitmap first, then reconstruct `Some(...)` or `None`.
- To handle `Option<T>` and plain `T` uniformly in Rust generics, the author introduces a `NoneUtils` trait that provides `is_none()`, `unwrap_or_self()`, and `from_inner()`, allowing **generic serialization/deserialization logic to be generated automatically without reflection**.
- On top of this, two archive layouts are implemented: the **dense** layout is `| bitmap | values... |`, suitable for denser data; the **sparse** layout is `| bitmap | ptrs | values... |`, which stores only fields that are actually present and indexes them with relative pointers, making it suitable for rows with many `NULL`s.
- This optimization changes only the on-disk/archive representation; it **does not change the in-memory Rust struct interface**, and dense or sparse representation can be chosen per row.

## Results
- In one small example given in the article, the original in-memory struct is only **40B**, but after `rkyv` archiving it becomes **88B**, i.e. **more than 2x larger**; the main inflation comes from `Option<ArchivedString>`, where each field is about **24B = 16B string archive + 8B Option discriminant/overhead**.
- Under the new scheme, values that were previously `None` or empty strings often took **24B**, but in the best case now require only **1 bit** to represent absence, greatly reducing the storage cost of large numbers of empty values in wide tables.
- In the real customer workload that triggered the problem, the author says the **serialized row size was reduced by about 2x**, so **disk I/O decreased correspondingly**, and overall **throughput returned to the level the customer expected**.
- The article does not provide a more systematic benchmark table, dataset names, or precise throughput figures (such as rows/s, MB/s, or end-to-end latency); the strongest quantitative conclusion is that **row size was roughly halved, I/O decreased accordingly, and performance recovered**.

## Link
- [https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct](https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct)
