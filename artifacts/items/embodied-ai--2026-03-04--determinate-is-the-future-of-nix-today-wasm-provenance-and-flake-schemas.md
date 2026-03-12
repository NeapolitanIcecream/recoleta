---
source: hn
url: https://determinate.systems/blog/determinate-nix-future/
published_at: '2026-03-04T23:20:21'
authors:
- biggestlou
topics:
- nix
- webassembly
- software-supply-chain
- provenance
- flake-schemas
relevance_score: 0.01
run_id: materialize-outputs
---

# Determinate is the future of Nix today: Wasm, provenance, and flake schemas

## Summary
这篇文章介绍了 Determinate Nix 的三项关键更新：Wasm/WASI、构建产物 provenance、以及 flake schemas，目标是把 Nix 从“构建工具”推进为更通用、更安全、更可扩展的平台。核心价值在于提升表达复杂逻辑的能力、增强供应链可验证性，并放开 flakes 的结构约束。

## Problem
- 传统 Nix 生态被认为发展停滞，且缺少统一清晰的未来路线。
- 用 Nix 语言编写高性能、可测试、复杂的求值与构建逻辑很困难，尤其在大规模企业和单体仓库场景中。
- 现有 Nix 的供应链信息主要停留在依赖图层面，缺乏对构建来源的可验证 provenance；同时 flakes 的输出结构过于僵化。

## Approach
- 引入 **Wasm** 用于 evaluation、**WASI** 用于 realization，让用户把原本难以在 Nix 中实现的复杂逻辑转移到 Rust 等成熟语言中，再从 Nix 无缝调用。
- 通过 Wasm/WASI 支持在 Nix 工作流中直接实现诸如解析 `go.mod/go.sum`、处理 YAML、以及更复杂的系统逻辑，而不必依赖大量 Nix 表达式或包装层。
- 增加实验性的 **provenance** 支持：为 store paths 自动记录并签名其来源信息，并在推送到 FlakeHub Cache 时存储这些元数据。
- 引入 **flake schemas**，允许开发者自定义 flake 输出结构，并让 `nix flake show` 等工具以语义化方式展示这些自定义输出。

## Results
- 文章未提供标准基准测试、数据集或性能指标，因此**没有定量结果**可报告。
- 最强的具体发布声明是：本周上线三项能力——**Wasm/WASI 支持**、**实验性 provenance 存储与签名**、以及 **flake schemas**。
- 作者声称 Wasm/WASI 将显著扩展 Nix 的适用范围，使复杂逻辑可由 Rust 等语言实现，并可覆盖 evaluation 与 realization 两个阶段，但**未给出吞吐、延迟或开发效率数字**。
- provenance 方面，当前已可附加如 **GitHub Actions workflow** 的构建来源信息，并计划进一步扩展到 **TPM attestation** 级别的机器身份与状态验证，但**尚未提供覆盖率或安全收益量化结果**。
- flake schemas 被描述为对 flakes 结构灵活性的“重大改进”，能把原本显示为 `unknown` 的输出变成可解释的语义结构，但**没有用户研究或兼容性统计数据**。

## Link
- [https://determinate.systems/blog/determinate-nix-future/](https://determinate.systems/blog/determinate-nix-future/)
