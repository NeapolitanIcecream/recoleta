---
source: hn
url: https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok
published_at: '2026-03-07T23:25:21'
authors:
- todsacerdoti
topics:
- nix
- reproducible-builds
- graphics-drivers
- fhs
- linux-packaging
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# Nix is a lie, and that's ok

## Summary
这篇文章指出：Nix 宣称摆脱 FHS 路径以实现可复现性，但在图形驱动场景中实际上重新引入了类似 FHS 的全局约定路径。核心观点不是提出新系统，而是解释这种“不纯”为什么在工程上是可接受且必要的。

## Problem
- Nix 的设计目标是避免依赖 `/usr/lib`、`/lib64` 这类 FHS 约定路径，以提高构建与运行的可复现性。
- 但 GPU 图形栈中的 `libGL.so` 必须与宿主机内核模块和实际硬件匹配，应用在构建时无法预知未来运行机器的驱动环境。
- 如果让每个 derivation 都内置正确的 `libGL.so`，会导致大规模 rebuild，并让 NixOS binary cache 的复用价值大幅下降；而在非 NixOS 上，这又会直接造成 `libGL.so.1: cannot open shared object file` 的运行错误。

## Approach
- 文章解释 Nix/NixOS 的实际工程做法：承认图形驱动是用户态与内核态之间的“硬边界”，无法完全用纯式打包抽象掉。
- NixOS 与 Home Manager 因此引入一个有意的不纯全局路径 `/run/opengl-driver/lib`，让 derivation 在运行时从该位置查找 `libGL.so`。
- 这本质上重新引入了类似 FHS 的“按约定找库”机制，但避免了为每种驱动组合重建所有包的代价。
- 对非 NixOS 用户，常见替代方案包括 `nixGL` 通过 `LD_LIBRARY_PATH` 注入库、手工设置 `LD_LIBRARY_PATH`、或自己创建 `/run/opengl-driver` 并软链接系统驱动。

## Results
- 文章没有提供实验数据、基准测试或正式定量结果。
- 最强的具体主张是：非 NixOS 上的图形应用问题长期存在，对应 issue `#9415` 自 **2015** 年起一直存在。
- 文章给出的关键工程结论是：为避免“每个用户/驱动组合都触发 massive rebuilds”，NixOS 选择使用 `/run/opengl-driver/lib` 这一全局路径作为折中。
- 具体故障表现被明确给出：运行依赖图形的 Nix 应用时，可能出现 `libGL.so.1: cannot open shared object file: No such file or directory`。
- 结论性观点是：Nix 并未完全消灭 FHS 式约定；在 GPU 驱动这一场景中，“必要时允许不纯性”比坚持绝对纯度更实用。

## Link
- [https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok](https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok)
