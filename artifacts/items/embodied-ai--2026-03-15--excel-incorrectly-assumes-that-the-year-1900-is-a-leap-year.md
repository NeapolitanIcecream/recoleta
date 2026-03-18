---
source: hn
url: https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year
published_at: '2026-03-15T23:34:35'
authors:
- susam
topics:
- excel-date-system
- leap-year-bug
- backward-compatibility
- spreadsheet-software
relevance_score: 0.0
run_id: materialize-outputs
---

# Excel incorrectly assumes that the year 1900 is a leap year

## Summary
这篇文章说明 Excel 故意保留了“1900 年是闰年”的错误设定，主要是为了兼容 Lotus 1-2-3 的日期序列系统。它讨论了修正该错误会带来的系统性兼容性代价，以及为何微软选择维持现状。

## Problem
- 解决的问题是：解释 Excel 为什么把 **1900 年错误地当作闰年**，以及是否应该修正这一历史错误。
- 这很重要，因为 Excel 的日期系统广泛用于工作表、公式和跨软件数据交换；改动底层日期规则会影响大量现有文件与计算结果。
- 当前实际影响很有限：主要是 **1900 年 3 月 1 日之前** 的日期在 `WEEKDAY` 等函数中可能返回错误结果。

## Approach
- 核心机制很简单：Excel **延续了 Lotus 1-2-3 的日期序列设计**，把 1900 年按闰年处理，以保持序列日期和历史文件兼容。
- 微软没有提出新算法，而是做了一个 **兼容性优先的工程权衡**：接受一个已知的历史错误，避免破坏现有工作簿和跨程序日期互操作。
- 文中通过对比“修正错误”与“维持现状”的后果来论证该选择：前者会导致大范围日期偏移、函数结果变化和兼容性破坏，后者只留下少见的边缘问题。
- 文章还明确限定了错误范围：**只有 1900 年** 被特殊错误处理；其他闰年规则（包括像 2100 这样的世纪年非闰年）Excel 都能正确处理。

## Results
- 未提供实验数据或基准测试，因此**没有定量结果**可报告。
- 文章的最强结论是：如果修正该行为，**几乎所有现有 Excel 工作表中的日期都会减少 1 天**，并需要大量人工修复相关公式。
- 文章还声称：修正后某些函数（如 **`WEEKDAY`**）会对历史日期返回不同值，从而导致部分工作表公式行为改变。
- 另一个明确结论是：修正会**破坏 Excel 与其他使用相同序列日期系统程序之间的兼容性**。
- 保持现状时，文中指出只有 **1 个主要已知问题**：`WEEKDAY` 对 **1900 年 3 月 1 日之前** 的日期结果不正确，而这种使用场景“很少见”。

## Link
- [https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year)
