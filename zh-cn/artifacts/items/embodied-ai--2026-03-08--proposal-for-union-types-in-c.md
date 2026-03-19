---
source: hn
url: https://github.com/dotnet/csharplang/blob/main/proposals/unions.md
published_at: '2026-03-08T23:37:02'
authors:
- azhenley
topics:
- csharp
- union-types
- pattern-matching
- type-system
- language-design
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Proposal for Union Types in C#

## Summary
这是一份 C# 语言提案，而非机器人/AI 论文；它提出在 C# 中原生支持 union types，使编译器能够理解“一个值来自有限类型集合”并据此做隐式转换、模式匹配和穷尽性检查。其价值在于提升类型安全、代码表达力与模式匹配体验。

## Problem
- C# 长期缺少一等 union types，开发者很难直接表达“值只能是若干封闭类型之一”。
- 这会导致模式匹配无法可靠做穷尽性检查，往往需要手写样板代码、回退分支或借助类层次/`object` 包装。
- 缺少语言级 nullability 和匹配语义支持，也使现有替代方案在安全性、可读性和性能上不理想。

## Approach
- 提出 `[Union]` 标注的类/结构体模式：只要类型暴露规定的创建成员（单参数构造函数或工厂方法）和 `Value` 属性，编译器就把它视为 union type。
- 每个 case type 都能**隐式转换**到 union；对 union 做模式匹配时，编译器会自动“解包”到底层 `Value`，从而像直接匹配内部值一样使用 `is`/`switch`。
- 对 `switch` 表达式加入**穷尽性规则**：当所有 case types 都被覆盖时，无需额外 fallback；同时增强对内部值 null 状态的可空性分析。
- 为性能提供可选的**non-boxing access pattern**：`HasValue` + 针对每个 case 的 `TryGetValue(out T)`，让编译器在模式匹配时优先走强类型访问，减少依赖 `object? Value`。
- 再额外提供简洁的 `union` 声明语法，自动降级为普通 `struct` + 生成的构造函数与 `Value` 属性，覆盖大多数常见用例，同时保留手写实现的灵活性。

## Results
- 文本中**没有实验性定量结果**，没有数据集、基准测试、准确率/速度等数值比较；这是语言设计提案，不是实证论文。
- 主要可验证主张是语义层面的：union 值在 `switch` 中只要覆盖全部 case types，即可被视为穷尽匹配，无需默认分支。
- 提案明确了 2 类访问模式：基础模式要求 `1` 个 `Value` 属性 + 至少 `1` 个单参数创建成员；可选高效模式要求 `1` 个 `HasValue` 和每个 case `1` 个 `TryGetValue(out T)`。
- `union` 声明会生成 `1` 个 `struct`、`1` 个 `object? Value` 属性，以及**每个 case type 1 个公共构造函数**；例如 `union Pet(Cat, Dog)` 会生成 `2` 个构造函数。
- 设计决议包含若干具体规则：仅接受 by-value 或 `in` 参数作为创建成员；`TryGetValue` 选择时只考虑 identity/reference/boxing 隐式转换；显式/隐式用户自定义转换与 union conversion 的优先级也被明确定义。

## Link
- [https://github.com/dotnet/csharplang/blob/main/proposals/unions.md](https://github.com/dotnet/csharplang/blob/main/proposals/unions.md)
