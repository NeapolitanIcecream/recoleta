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
language_code: en
---

# Proposal for Union Types in C#

## Summary
This is a C# language proposal whose goal is to add union types natively to the language, allowing a value to safely represent "one of a finite set of types." It integrates construction, pattern matching, exhaustiveness checking, and nullability analysis into a unified mechanism.

## Problem
- C# has long lacked native union types, making it difficult for developers to directly express that "a value can only come from a closed set of types."
- Without language-level support, pattern matching cannot reliably perform exhaustiveness checking, and API design becomes more verbose and more error-prone.
- This matters because it affects type safety, readability, error-handling modeling (such as `Result<T>`/`Option<T>`), and the overall pattern-matching experience.

## Approach
- Use the `[Union]` attribute to mark a class/struct as a union type; case types are determined by the parameter types of single-parameter constructors or static `Create` factory methods.
- The compiler provides four core behaviors for unions: implicit conversions from case types to the union, pattern matching that automatically "unwraps" the contents, switch exhaustiveness checking based on case types, and enhanced nullability tracking.
- The unified minimum convention is the basic union pattern: there must be creation members and an `object? Value` property; optional `HasValue`/`TryGetValue(out T)` provide a "non-boxing" access path, making pattern matching more efficient.
- It also provides shorthand syntax `union Name(T1, T2, ...)`, which lowers to a normal `struct`: automatically generating `[Union]`, an `IUnion` implementation, a `Value` property, and constructors for each case.
- The design separates "union types" from "union declarations": the former allows existing types to adapt into this model, while the latter provides an opinionated concise declaration syntax.

## Results
- This document is a language design proposal rather than an experimental paper, and **does not provide benchmarks, datasets, or quantitative metrics**, so there are no precise performance or accuracy numbers to report.
- Its stated core capabilities include: `switch` can be considered exhaustive when all case types are covered, with no fallback required; if `Value` may be null, the compiler will still warn about unhandled `null`.
- It specifies clear conversion precedence rules: user-defined implicit conversions take priority over union conversion; for explicit casts, explicit user-defined conversions take priority; without an explicit cast, union conversion may take priority over explicit user-defined conversions.
- It clarifies matching optimization rules: if there is a `TryGetValue(out T)` suitable for the case type, the compiler uses it first; otherwise, null checks prefer `HasValue`; failing that, it falls back to reading `Value`.
- The proposal also records several approved design decisions, for example: union declarations lower to a normal `struct` rather than a `record struct`; pattern matching for Nullable<union> "drills down" has been approved; `IUnion<TUnion>` has been removed.

## Link
- [https://github.com/dotnet/csharplang/blob/main/proposals/unions.md](https://github.com/dotnet/csharplang/blob/main/proposals/unions.md)
