---
source: hn
url: https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year
published_at: '2026-03-15T23:34:35'
authors:
- susam
topics:
- spreadsheet-compatibility
- date-serialization
- leap-year-bug
- legacy-software
relevance_score: 0.06
run_id: materialize-outputs
language_code: zh-CN
---

# Excel incorrectly assumes that the year 1900 is a leap year

## Summary
这篇文章说明：Excel 将 1900 年错误地当作闰年并非单纯缺陷，而是为兼容 Lotus 1-2-3 而保留的历史设计选择。它讨论了修正该行为的代价与收益，结论是保留现状更合理。

## Problem
- 要解决的问题是：解释 Excel 为什么错误地把 1900 年视为闰年，以及这个历史错误为什么没有被修复。
- 这件事重要，因为日期序列系统会影响大量电子表格、公式结果和与其他软件的兼容性。
- 如果处理不当，修改该行为会让现有文档中的日期整体错位，并破坏既有工作流。

## Approach
- 核心机制很简单：Excel 沿用了 Lotus 1-2-3 的日期序列系统，把 1900 年按闰年处理，以保持文件和日期计算的兼容性。
- 文章采用的是兼容性权衡分析，而不是提出新算法：比较“修正错误”与“保留历史行为”各自带来的系统性影响。
- 它指出，修正后几乎所有现有工作表中的日期都会减少 1 天，相关日期公式也可能需要人工调整。
- 同时，像 `WEEKDAY` 这样的函数结果会变化，并且 Excel 与其他使用相同日期序列的软件之间会失去兼容性。
- 因而微软选择保留该特例，只接受一个较小范围的问题：1900 年 3 月 1 日之前的日期星期值可能不正确。

## Results
- 文中没有提供实验数据、基准测试或标准评测指标，因此没有定量结果可报告。
- 最强的具体结论是：若修正该问题，**几乎所有**当前 Excel 工作表和其他文档中的日期都会**减少 1 天**。
- 另一个具体影响是：`WEEKDAY` 函数会对 **1900 年 3 月 1 日之前** 的日期返回错误值；微软称该问题较少见，因为大多数用户不会使用这一区间的日期。
- 文章明确说明：除 **1900 年** 外，Excel 对其他闰年处理正确，包括像 **2100 年** 这样“世纪年但不是闰年”的情况。
- 核心主张不是性能突破，而是产品决策：为保持与 Lotus 1-2-3 及相关日期系统的兼容性，保留这一历史行为比修复它的总体代价更低。

## Link
- [https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year)
