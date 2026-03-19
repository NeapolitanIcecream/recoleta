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
- build-systems
- provenance
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# Determinate is the future of Nix today: Wasm, provenance, and flake schemas

## Summary
这篇文章介绍了 Determinate Nix 的三项新能力：Wasm/WASI、制品来源证明（provenance）和 flake schemas，目标是把 Nix 从“构建工具”推进为更通用、更可信、更可扩展的平台。核心主张是解决 Nix 在表达复杂逻辑、供应链可验证性和 flakes 扩展性上的长期瓶颈。

## Problem
- Nix 生态被作者认为长期停滞，缺少清晰未来路线，难以满足大规模团队的复杂需求。
- 复杂评估/构建逻辑很难直接用 Nix 表达和测试，导致高性能、可维护的定制逻辑实现成本高。
- 现有 Nix 更强调可复现性，但对“制品具体来自哪里、由谁/何时/在哪台机器构建”的来源证明能力不足；同时 flakes 输出结构过于固定，限制了项目表达力。

## Approach
- 引入 **Wasm** 与 **WASI** 支持：把原本难以用 Nix 写好的逻辑转移到 Rust 等成熟语言中实现，再从 Nix 无缝调用；Wasm 主要用于 evaluation，WASI 用于 realisation 并提供文件系统访问。
- 通过 Wasm/WASI，用户可在 Nix 中实现更复杂的任务，例如解析 `go.mod`/`go.sum`、处理 YAML、在 flake 中实现 IP 地址管理等。
- 增加实验性的 **provenance** 机制：为 store paths 自动记录并签名来源数据，并在推送到 FlakeHub Cache 时存储这些信息。
- 引入 **flake schemas**：允许团队定义自有的 flake 输出结构，使 `nix flake show` 等工具能以语义化方式展示非标准输出，而不再只显示 `unknown`。

## Results
- 文章没有提供系统性的基准测试或标准数据集结果，因此**没有定量性能提升数字**。
- 明确的落地结果是：**Wasm/WASI 支持已发布到 Determinate Nix**，并被描述为“最激进的变化”“最具变革性的一批改动之一”。
- **provenance 已有实验性支持**：可为 store paths 存储来源数据，并且对推送到 **FlakeHub Cache** 的路径自动签名与保存来源信息。
- 具体已用案例：作者称其内部已将 **GitHub Actions 工作流数据**附加到构建产物上，以追踪“何时、何地构建”。
- 未来增强方向包括 **TPM 可证明(attestable) 机器信息**，以支持基于构建机器身份与状态的信任/不信任决策。
- **flake schemas 本周随产品发布**，核心改进是让 flakes 可表达超出 `packages`、`nixosConfigurations`、`devShells` 等预定义类别的输出，并在工具中得到有意义展示。

## Link
- [https://determinate.systems/blog/determinate-nix-future/](https://determinate.systems/blog/determinate-nix-future/)
