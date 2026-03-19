---
source: hn
url: https://renderling.xyz/articles/introducing-wgsl-rs.html
published_at: '2026-03-04T23:26:21'
authors:
- efnx
topics:
- wgsl
- rust
- shader-transpilation
- webgpu
- graphics-tooling
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Wgsl-Rs

## Summary
This article introduces **wgsl-rs**: a procedural macro library for writing WGSL shaders using a subset of Rust syntax. Its main goal is to use stable Rust to generate both CPU-runnable code and readable WGSL, thereby lowering the barrier to using Rust-GPU.

## Problem
- The existing **Rust-GPU** approach is powerful, but it depends on a custom compiler backend, a specific toolchain, and a particular `spirv-std` version, making installation and maintenance costly.
- Common pain points in shader development include: complex dual CPU/GPU compilation workflows, cumbersome SPIR-V linking, errors that often surface only in deep compilation stages, and inconvenient debugging and testing.
- These issues slow down graphics/shader development, especially for developers who want to unify CPU and GPU logic with Rust.

## Approach
- It proposes **wgsl-rs**: add `#[wgsl]` to a Rust module, and the procedural macro will **preserve the original Rust code so it runs normally on the CPU**, while also **transpiling the same code into WGSL** for GPU use.
- Use `#[vertex]`, `#[fragment]`, and `#[compute]` to mark entry points, and use macros like `uniform!` and `get!` to declare/read bindings on both the Rust and WGSL sides.
- The generated WGSL is **human-readable**, with structure and naming kept as close to the Rust as possible, making manual inspection and debugging easier.
- For standalone modules, it uses **naga** at compile time to validate WGSL and map errors back to Rust source locations; for cross-module cases, it automatically generates `#[test]`s and validates via `cargo test`.
- An optional `linkage-wgpu` feature can also automatically generate `wgpu`-related boilerplate, such as buffer descriptors, bind group layouts, shader module helpers, and more.

## Results
- The article **does not provide standard benchmarks, datasets, or performance metrics**, nor does it give quantitative results such as throughput, latency, or compile time.
- The strongest concrete engineering claim is that, compared with Rust-GPU, `wgsl-rs` eliminates the need for a **custom compiler backend, a nightly toolchain, and the SPIR-V intermediate step**, and can be used directly with `cargo add wgsl-rs`.
- The author positions it as a solution that delivers roughly **"80% of the benefit for 20% of the work"**, and adds that the real effort may be closer to **10% or 5%**; this is an experiential statement, not an experimental result.
- One concrete example is provided: the same Rust shader code can both call `hello_triangle::vtx_main(0)` directly on the CPU and automatically generate corresponding WGSL, demonstrating the “single source, dual target” capability.
- It claims to enable **compile-time or test-time shader validation**, **CPU unit testing of shader logic**, and **automatic generation of wgpu boilerplate**, thereby significantly improving the development experience, though the article does not quantify these benefits.

## Link
- [https://renderling.xyz/articles/introducing-wgsl-rs.html](https://renderling.xyz/articles/introducing-wgsl-rs.html)
