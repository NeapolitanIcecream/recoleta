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
language_code: zh-CN
---

# Nobody ever got fired for using a struct

## Summary
这篇文章分析了一个真实的性能回归案例：将宽而稀疏、包含数百个可空列的 SQL 行直接映射为 Rust struct 并用 rkyv 序列化时，磁盘表示膨胀，导致 IO 和吞吐下降。作者通过把逐字段 `Option<T>` 改为位图加裸值、并在稀疏行上使用指针索引的布局，在不改变内存中接口的前提下显著缩小了序列化体积。

## Problem
- 论文解决的问题是：**宽表（700+ 可空列）在 Rust/rkyv 的默认 struct 序列化下出现严重空间浪费和性能下降**，这很重要，因为 Feldera 处理的大多是**放不进内存、需要频繁落盘**的数据流工作负载。
- 内存中的 Rust struct 本身并不差；问题主要出在**磁盘/归档表示**：很多 `Option<T>` 在序列化后不再“免费”，尤其是 `Option<ArchivedString>` 会显式存储判别信息。
- 当 SQL 模式默认可空、表又很宽且数据稀疏时，**row-oriented 存储 + 大量 nullable 字段** 的组合会让简单 struct 布局成为瓶颈。

## Approach
- 核心方法很简单：**不再为每个字段单独存 `Option<T>` 的归档形式，而是先写一个 bitmap 表示哪些字段存在，再只存字段值本身**。
- 用一个通用辅助 trait `NoneUtils` 统一处理 `Option<T>` 和普通 `T`：序列化时先问 `is_none()` 决定 bitmap，再用 `unwrap_or_self()` 取出要写入的裸值；反序列化时通过 `from_inner()` 恢复为 `Some(...)` 或原值。
- 这样把布局从“每个字段自带 Option 开销”变成了概念上的 `| bitmap | field0 | field1 | ... |`，从而消除大量可空字段的固定额外成本。
- 对更稀疏的行，再进一步采用稀疏布局：`| bitmap | ptrs | values... |`，只存**实际存在的字段值**，并用相对指针索引，跳过所有 `NULL` 字段。
- 系统通过宏自动生成这些序列化/反序列化逻辑，并且**按行选择 dense 或 sparse 表示**，保留原有 Rust struct 的内存接口。

## Results
- 在示例 8 字段 struct 中，**内存布局为 40B**，但默认 rkyv 归档后变成 **88B**，即**超过 2 倍**；主要原因是 `Archived<Option<SqlString>>` 每个字符串字段要 **24B = 16B 字符串 + 8B Option 判别/开销**。
- 作者指出：以前一个为 `None` 或空字符串的字符串字段也会消耗 **24B**，优化后在最佳情况下只需 **1 bit** 来表示缺失。
- 在触发问题的真实客户工作负载中，**序列化后的 row size 约减少 2x**。
- 由于行大小缩小，**disk IO 相应下降**，并且**throughput 恢复到客户预期水平**；文中未提供更细的吞吐绝对值、数据集规模或与其他系统的定量对比。
- 文章最强的实际结论是：对于**数百可空列 + 小字符串/稀疏数据 + 行式存储**的场景，改变序列化数据布局比继续沿用普通 struct 更关键。

## Link
- [https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct](https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct)
