---
source: hn
url: https://github.com/dotnet/csharplang/blob/main/proposals/unions.md
published_at: '2026-03-08T23:37:02'
authors:
- azhenley
topics:
- csharp-language
- union-types
- pattern-matching
- type-system
- nullability
relevance_score: 0.52
run_id: materialize-outputs
language_code: zh-CN
---

# Proposal for Union Types in C#

## Summary
这是一份 C# 语言提案，目标是为语言原生加入 union types，使一个值可以安全地表示“有限几种类型之一”。它把构造、模式匹配、穷尽性检查和可空性分析整合成一套统一机制。

## Problem
- C# 长期缺少原生 union types，导致开发者很难直接表达“值只可能来自一组封闭类型”。
- 没有语言级支持时，模式匹配无法可靠地做穷尽性检查，API 设计也更冗长、更易出错。
- 这很重要，因为它影响类型安全、可读性、错误处理建模（如 `Result<T>`/`Option<T>`）以及模式匹配体验。

## Approach
- 通过 `[Union]` 属性把 class/struct 标记为 union type；case types 由单参数构造函数或静态 `Create` 工厂方法的参数类型确定。
- 编译器为 union 提供四类核心行为：从 case type 到 union 的隐式转换、对内容自动“解包”的模式匹配、基于 case types 的 switch 穷尽性检查、以及增强的可空性跟踪。
- 统一的最小约定是 basic union pattern：必须有创建成员和 `object? Value` 属性；可选的 `HasValue`/`TryGetValue(out T)` 提供“non-boxing”访问路径，让模式匹配更高效。
- 额外提供简写语法 `union Name(T1, T2, ...)`，其 lowering 为普通 `struct`：自动生成 `[Union]`、`IUnion` 实现、`Value` 属性和各 case 构造函数。
- 设计上把“union types”与“union declarations”分离：前者允许现有类型适配进入该模式，后者提供意见化的简洁声明方式。

## Results
- 该文档是语言设计提案而非实验论文，**未提供基准测试、数据集或量化指标**，因此没有准确的性能/精度数字可报告。
- 它声明的核心能力包括：`switch` 在覆盖全部 case types 时可视为穷尽，无需 fallback；若 `Value` 可能为 null，编译器仍会对未处理的 `null` 给出警告。
- 它给出明确的转换优先级规则：用户自定义隐式转换优先于 union conversion；显式 cast 时显式用户转换优先；无显式 cast 时 union conversion 可优先于显式用户转换。
- 它明确了匹配优化规则：若存在适配 case type 的 `TryGetValue(out T)`，编译器优先用它；否则对 `null` 检查优先用 `HasValue`；再退化到读取 `Value`。
- 提案还记录了若干已批准设计决议，例如：union declaration 降低为普通 `struct` 而非 `record struct`；Nullable<union> 的模式匹配“向下钻取”已获批准；`IUnion<TUnion>` 已被移除。

## Link
- [https://github.com/dotnet/csharplang/blob/main/proposals/unions.md](https://github.com/dotnet/csharplang/blob/main/proposals/unions.md)
