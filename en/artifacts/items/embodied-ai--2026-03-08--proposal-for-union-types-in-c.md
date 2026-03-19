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
language_code: en
---

# Proposal for Union Types in C#

## Summary
This is a C# language proposal, not a robotics/AI paper; it proposes native support for union types in C#, allowing the compiler to understand that "a value comes from a finite set of types" and, based on that, perform implicit conversions, pattern matching, and exhaustiveness checking. Its value lies in improving type safety, code expressiveness, and the pattern matching experience.

## Problem
- C# has long lacked first-class union types, making it difficult for developers to directly express that "a value can only be one of several closed types."
- This prevents pattern matching from reliably performing exhaustiveness checks, often requiring handwritten boilerplate, fallback branches, or wrappers based on class hierarchies/`object`.
- The lack of language-level nullability and matching semantics also makes existing alternatives less than ideal in terms of safety, readability, and performance.

## Approach
- Proposes a class/struct pattern annotated with `[Union]`: as long as the type exposes the required creation members (single-parameter constructors or factory methods) and a `Value` property, the compiler treats it as a union type.
- Each case type can be **implicitly converted** to the union; when pattern matching against a union, the compiler automatically "unwraps" to the underlying `Value`, enabling `is`/`switch` to be used as if directly matching the inner value.
- Adds an **exhaustiveness rule** for `switch` expressions: when all case types are covered, no additional fallback is needed; at the same time, nullability analysis of the inner value's null state is enhanced.
- Provides an optional **non-boxing access pattern** for performance: `HasValue` + a `TryGetValue(out T)` for each case, allowing the compiler to prefer strongly typed access during pattern matching and reduce reliance on `object? Value`.
- Also provides concise `union` declaration syntax, which is automatically lowered to a normal `struct` plus generated constructors and a `Value` property, covering most common use cases while preserving the flexibility of handwritten implementations.

## Results
- The text contains **no experimental quantitative results**, no datasets, benchmarks, or numerical comparisons of accuracy/speed; this is a language design proposal, not an empirical paper.
- The main verifiable claims are semantic: in a `switch`, a union value can be considered exhaustively matched as long as all case types are covered, without requiring a default branch.
- The proposal defines 2 access patterns: the basic pattern requires `1` `Value` property + at least `1` single-parameter creation member; the optional efficient pattern requires `1` `HasValue` and `1` `TryGetValue(out T)` for each case.
- A `union` declaration generates `1` `struct`, `1` `object? Value` property, and **1 public constructor per case type**; for example, `union Pet(Cat, Dog)` generates `2` constructors.
- The design decisions include several concrete rules: only by-value or `in` parameters are accepted as creation members; when selecting `TryGetValue`, only identity/reference/boxing implicit conversions are considered; the precedence of explicit/implicit user-defined conversions and union conversion is also clearly defined.

## Link
- [https://github.com/dotnet/csharplang/blob/main/proposals/unions.md](https://github.com/dotnet/csharplang/blob/main/proposals/unions.md)
