---
source: hn
url: https://github.com/ncruces/wasm2go
published_at: '2026-03-05T23:43:06'
authors:
- atkrad
topics:
- webassembly
- go-transpiler
- static-translation
- compiler-tooling
- code-generation
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Ncruces/wasm2go: A WASM to Go translator

## Summary
This is a tool that directly translates WebAssembly (Wasm) modules into a single Go source file. Its goal is to convert specific Wasm modules into compilable, callable Go code with high fidelity while relying only on the Go standard library. It emphasizes semantic correctness and the quality of the generated assembly rather than human readability of the generated code.

## Problem
- When integrating Wasm modules into Go projects, common approaches depend on runtimes, interpreters, or extra dependencies; this tool attempts to turn Wasm directly into a self-contained Go package.
- General-purpose Wasm support covers a very broad scope, but many real-world scenarios only need a “useful enough” subset produced by `clang`, so a more focused translation strategy can trade breadth for practicality.
- Preserving semantics is important: Wasm and Go differ significantly in control flow, type systems, floating-point representation, memory access, and more, and mishandling these differences can lead to inconsistent behavior.

## Approach
- The core mechanism is **static source translation**: given a Wasm module as input, it outputs a single Go source file; the generated package exports a `Module` struct and a `New` initialization function, Wasm exports become methods on `Module`, and imports are mapped to interfaces accepted by `New`.
- It supports only a practical subset of Wasm: covering most Wasm 1.0 features and part of Wasm 2.0 (such as bulk memory, reference types, nontrapping float-to-int, sign-extension, and multi-values), while explicitly not supporting some features such as SIMD and imported tables/globals.
- To preserve semantic correctness, the translation uses a **stack-to-register** style, turning Wasm’s stack-based execution into Go variables; control flow is expressed with `goto` and labels; differences between `bool` and `int32`, numeric literals, floating-point operations, and special values (such as `-0`, `Inf`, and `NaN`) are handled explicitly.
- On little-endian CPUs, it can optionally use `unsafe` to generate faster code; the author emphasizes that the generated code still follows `unsafe` rules and that all memory accesses are bounds-checked. Parameters can also be used to select big-endian or little-endian versions and whether to canonicalize NaN.

## Results
- In terms of output form, the tool can convert a Wasm module into a **single Go source file**, with **no dependencies other than the Go standard library**.
- In terms of support scope, it claims to cover a **“useful subset”** produced by `clang`: including **most Wasm 1.0 features** and **5 categories** of Wasm 2.0 subfeatures (bulk memory, reference types, nontrapping float-to-int, sign-extension, and multi-values).
- In terms of performance claims, the text does not provide benchmark numbers; the strongest quantitative statement is that for **little-endian CPUs**, `unsafe` can generate **faster** code, but no specific speedup percentages, datasets, or baseline comparisons are provided.
- In terms of engineering integration, it can generate both **big-endian** and **little-endian** versions and select between them via **build tag**; it also provides **1** NaN canonicalization switch (`-nanbox`).
- In terms of security boundaries, the author explicitly assumes the input Wasm is **trusted** and recommends at least running a verifier check on untrusted modules first; this indicates the goal is not sandboxed execution, but source translation for controlled inputs.

## Link
- [https://github.com/ncruces/wasm2go](https://github.com/ncruces/wasm2go)
