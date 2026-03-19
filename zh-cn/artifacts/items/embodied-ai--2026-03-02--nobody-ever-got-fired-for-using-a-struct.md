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
language_code: zh-CN
---

# Nobody ever got fired for using a struct

## Summary
这篇文章分析了一个实际系统中的性能异常：Rust 里的宽表 struct 在内存中高效，但序列化到磁盘后因大量 `Option` 字段而膨胀，拖慢了 I/O 与吞吐。作者提出保留内存中的 struct 接口、改造归档格式，用位图和稀疏存储显著压缩行大小并恢复性能。

## Problem
- 文章解决的是**宽 SQL 表（数百个可空列）在序列化/落盘时空间与吞吐急剧恶化**的问题；这很重要，因为 Feldera 处理的大多数数据集都**放不进内存**，磁盘 I/O 直接决定系统性能。
- 根因不是 Rust struct 的内存布局，而是 `rkyv` 归档后，`Option<ArchivedString>` 等类型**失去“免费 Option”优化**，导致每个可空字段都要显式存储额外判别信息。
- 在有 700+ 个可空字段、且很多值为 `NULL`/空字符串的 SQL 宽表中，朴素 struct 序列化会造成严重空间浪费，进而拖慢整个数据流水线。

## Approach
- 核心方法很简单：**不再把每个字段单独存成 `Option<T>`，而是把“是否为 None”集中存进一个位图 bitmap**；字段值部分只存裸值 `T`。
- 序列化时，对每个字段先记录 1 bit：`1` 表示值存在，`0` 表示 `None`；若存在，再写入实际值。反序列化时先查位图，再重建 `Some(...)` 或 `None`。
- 为了在 Rust 泛型里统一处理 `Option<T>` 和普通 `T`，作者引入了 `NoneUtils` trait，提供 `is_none()`、`unwrap_or_self()`、`from_inner()`，从而**无需反射**也能自动生成通用序列化/反序列化逻辑。
- 在此基础上实现两种归档布局：**dense** 布局为 `| bitmap | values... |`，适合较密集数据；**sparse** 布局为 `| bitmap | ptrs | values... |`，只存实际存在的字段并用相对指针索引，适合大量 `NULL` 的行。
- 该优化只改变磁盘/归档表示，**不改变内存中的 Rust struct 接口**，并且可按行选择 dense 或 sparse 表示。

## Results
- 文中给出的一个小例子中，原始内存 struct 只有 **40B**，但 `rkyv` 归档后变成 **88B**，即**超过 2 倍**；主要膨胀来自 `Option<ArchivedString>`，每个字段约为 **24B = 16B 字符串归档 + 8B Option 判别/开销**。
- 新方案下，原本 `None` 或空字符串常常要占 **24B**，最佳情况下现在只需**1 bit** 来表示缺失，大幅降低宽表中大量空值的存储成本。
- 在触发问题的真实客户工作负载中，作者称**序列化后的行大小约减少 2x**，因此**磁盘 I/O 相应下降**，整体**吞吐恢复到客户预期水平**。
- 文章没有提供更系统的基准表、数据集名称或精确吞吐数值（如 rows/s、MB/s、端到端延迟）；最强的定量结论是**行大小约减半、I/O 相应下降、性能恢复**。

## Link
- [https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct](https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct)
