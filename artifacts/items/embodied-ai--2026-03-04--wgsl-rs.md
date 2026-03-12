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
---

# Wgsl-Rs

## Summary
这篇文章介绍了 **wgsl-rs**：一个用 Rust 语法子集编写 WGSL 着色器的过程宏库。它主打用稳定版 Rust 同时生成可在 CPU 运行的代码和可读的 WGSL，从而降低 Rust-GPU 的使用门槛。

## Problem
- 现有 **Rust-GPU** 方案虽然强大，但依赖自定义编译后端、特定工具链与 `spirv-std` 版本，安装和维护成本高。
- 着色器开发常见痛点包括：CPU/GPU 双编译流程复杂、SPIR-V 链接繁琐、错误常在深层编译阶段才暴露、调试和测试不方便。
- 这些问题会拖慢图形/着色器开发效率，尤其对想用 Rust 统一 CPU 与 GPU 逻辑的开发者很重要。

## Approach
- 提出 **wgsl-rs**：给 Rust 模块加上 `#[wgsl]`，过程宏会**保留原 Rust 代码可在 CPU 上正常运行**，同时把同一份代码**转译成 WGSL** 供 GPU 使用。
- 使用 `#[vertex]`、`#[fragment]`、`#[compute]` 标注入口点，并通过 `uniform!`、`get!` 等宏同时声明/读取 Rust 与 WGSL 侧的绑定。
- 生成的 WGSL 是**人类可读**的，结构和命名尽量与 Rust 保持一致，便于人工检查和排错。
- 对独立模块，在编译期用 **naga** 做 WGSL 校验并把错误映射回 Rust 源码位置；跨模块情况则自动生成 `#[test]`，通过 `cargo test` 验证。
- 可选 `linkage-wgpu` 功能还能自动生成 `wgpu` 相关样板代码，如 buffer descriptors、bind group layouts、shader module helpers 等。

## Results
- 文章**没有提供标准基准、数据集或性能指标**，也没有给出吞吐、延迟、编译时间等定量结果。
- 最强的具体工程性主张是：相比 Rust-GPU，`wgsl-rs` 省去了 **自定义编译后端、nightly toolchain、SPIR-V 中间步骤**，可直接 `cargo add wgsl-rs` 开始使用。
- 作者将其定位为实现大约 **“80% 的收益、20% 的工作量”** 的方案，并补充说真实投入可能更接近 **10% 或 5%**；这是经验性表述，不是实验结果。
- 提供了一个具体示例：同一份 Rust 着色器代码既可在 CPU 直接调用 `hello_triangle::vtx_main(0)`，也可自动生成对应 WGSL，体现“单源码、双目标”能力。
- 声称可实现**编译期或测试期 shader 校验**、**CPU 单元测试 shader 逻辑**、以及**自动生成 wgpu 样板代码**，从而显著改善开发体验，但文中未量化这些收益。

## Link
- [https://renderling.xyz/articles/introducing-wgsl-rs.html](https://renderling.xyz/articles/introducing-wgsl-rs.html)
