---
source: hn
url: https://www.rfc-editor.org/rfc/rfc4180
published_at: '2026-03-14T23:04:40'
authors:
- basilikum
topics:
- csv-format
- mime-type
- data-interoperability
- file-format-spec
- abnf
relevance_score: 0.18
run_id: materialize-outputs
---

# RFC 4180 – CSV (2005)

## Summary
这篇RFC不是提出新算法，而是为长期被广泛使用但缺少正式定义的CSV格式提供一个共同约定，并正式注册了 `text/csv` MIME 类型。它的价值在于减少不同程序对CSV的歧义解释，提升数据交换互操作性。

## Problem
- CSV被广泛用于电子表格和数据转换，但此前**没有统一、正式的规范**，导致不同实现对格式细节有不同理解。
- IANA此前**没有正式注册CSV对应的MIME类型**，而不同系统已经开始使用不一致的类型标识，影响网络传输和软件兼容性。
- 这种不一致会让解析器、导入导出工具和操作系统在处理表头、换行、引号、逗号转义等问题时出现互操作风险。

## Approach
- 文档总结了“多数实现大致遵循”的CSV约定，并把它写成一组**清晰的文本规则**：每条记录一行、字段用逗号分隔、可选表头、字段数应一致。
- 它规定了**引号处理机制**：含逗号、换行或双引号的字段应放入双引号中；字段内部的双引号用两个双引号转义。
- 它给出了**ABNF语法**，把CSV结构形式化为 `file/header/record/field` 等规则，便于实现者据此编写解析器。
- 它正式注册了 **`text/csv`** 媒体类型，并定义了可选参数 **`charset`** 和 **`header`**（`present`/`absent`）。
- 对实现建议采取保守生成、宽松接收的策略，因为现实世界中仍存在大量不完全一致的CSV实现。

## Results
- 最核心的成果是**正式注册了 MIME 类型 `text/csv`**，解决了此前“CSV常用但无官方MIME注册”的问题。
- 文档提供了**7条具体格式规则**，覆盖记录换行、末行换行可选、可选表头、字段分隔、引号包裹、特殊字符处理和双引号转义。
- 给出了完整的**ABNF语法定义**，包括 `file = [header CRLF] record *(CRLF record) [CRLF]` 等正式描述，可直接指导实现。
- 定义了**2个可选MIME参数**：`charset` 与 `header`；其中 `header` 的有效值是 **`present`** 或 **`absent`**。
- 文中**没有实验数据、基准测试或性能指标**，因此没有可报告的准确率、速度、数据集或对比基线结果。
- 最强的具体主张是：该RFC为CSV提供了一个共同定义，并通过 `text/csv` 注册显著改善实现间的互操作基础。

## Link
- [https://www.rfc-editor.org/rfc/rfc4180](https://www.rfc-editor.org/rfc/rfc4180)
