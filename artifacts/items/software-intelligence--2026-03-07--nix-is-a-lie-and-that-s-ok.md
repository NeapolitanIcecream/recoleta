---
source: hn
url: https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok
published_at: '2026-03-07T23:25:21'
authors:
- todsacerdoti
topics:
- nix
- reproducible-builds
- linux-graphics
- runtime-linking
relevance_score: 0.18
run_id: materialize-outputs
---

# Nix is a lie, and that's ok

## Summary
这篇文章指出，Nix 虽然宣称摆脱 FHS 路径以实现纯粹可复现，但在图形驱动场景中实际上依赖了一个全局约定路径，因此“纯粹性”存在例外。作者认为这不是失败，而是为兼容真实硬件与缓存效率所做的务实折中。

## Problem
- Nix 的核心承诺之一是避免 `/usr/lib`、`/lib64` 这类 FHS 约定路径，以提升可复现性和隔离性。
- 但 GPU 图形栈中的 `libGL.so` 必须与宿主机内核模块和物理硬件匹配，构建时无法预先打包到大多数 derivation 中。
- 若在 NixOS 中为每个 derivation 注入正确的 `libGL.so`，会导致大规模重建并削弱二进制缓存价值；而在非 NixOS Linux 上，这又导致长期存在的运行时缺库问题，影响实际可用性。

## Approach
- NixOS 和 Home Manager 采用了一种**有意引入的不纯性**：提供全局路径 `/run/opengl-driver/lib`，让程序在运行时到这里查找 `libGL.so`。
- 这本质上重新引入了类似 FHS 的“按约定找库”机制，但只针对图形驱动这一难以纯化的边界条件。
- 对非 NixOS 用户，社区常见做法包括使用 `nixGL` 在运行时通过 `$LD_LIBRARY_PATH` 注入驱动库、手工修改 `$LD_LIBRARY_PATH`，或自行创建 `/run/opengl-driver` 并软链接宿主系统驱动。
- 核心机制可以简单理解为：**不要把 GPU 驱动库预先封进每个包里，而是在运行时从宿主机约定位置借用正确版本**。

## Results
- 文中**没有提供正式实验或基准测试数字**。
- 给出的最具体事实性结果是：非 NixOS 用户运行依赖图形的 Nix 应用时，常见报错为 `libGL.so.1: cannot open shared object file: No such file or directory`。
- 文中指出相关问题在 issue `#9415` 中自 **2015 年**起已被记录，说明这是一个长期未彻底解决的兼容性问题。
- 作者的主要结论是：通过 `/run/opengl-driver/lib` 这类全局路径，Nix 在避免“为所有用户和所有 derivation 触发大规模 rebuild”与保持图形程序可运行之间取得了务实平衡。

## Link
- [https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok](https://fzakaria.com/2026/03/07/nix-is-a-lie-and-that-s-ok)
