---
source: hn
url: https://github.com/nix-windows/nix-windows-demo
published_at: '2026-03-12T23:58:52'
authors:
- Ericson2314
topics:
- nix
- windows
- cross-compilation
- deterministic-builds
- virtual-machine
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Nix on Windows –- proof-of-concept demo

## Summary
这是一个在 Linux 上离线构建并启动带有预装 Nix 的 Windows ValidationOS 虚拟机的概念验证。它证明了无需 Windows 授权、无需 Windows 工具链，也能以确定性方式在 Windows 环境中运行 Nix。

## Problem
- 该工作要解决的问题是：如何在**不依赖原生 Windows 安装、授权和构建工具**的情况下，把 Nix 带到 Windows 上并跑通最小可用流程。
- 这很重要，因为 Nix 的跨平台可复现构建价值很高，但 Windows 环境通常更难自动化、难以离线定制，也更依赖专有安装流程。
- 额外障碍是 ValidationOS 缺少 `shell32.dll`，而 Nix 依赖其中的 `SHGetKnownFolderPath` 来定位 `AppData`、`ProgramData` 等目录。

## Approach
- 核心方法很简单：在 Linux 上**交叉编译** Nix for Windows，然后把它**直接注入**到一个免费的轻量 Windows ValidationOS 磁盘镜像里，再用 QEMU 启动。
- 构建过程是**确定性的**：不会在构建阶段启动 VM，而是通过 `guestfish` 直接修改 VHDX/磁盘镜像内容。
- 镜像离线定制包括：注入启动脚本、关闭防火墙、配置 SSH key，并修改 Winlogon 注册表，使 `cmd.exe` 在 `C:\nix\bin` 中启动。
- 为绕过缺失的 `shell32.dll`，项目提供了一个最小的**stub DLL**，只实现 Nix 所需的 `SHGetKnownFolderPath`，通过读取环境变量返回目录路径；该 DLL 与 `nix.exe` 放在一起以利用 Windows DLL 搜索顺序。
- Nix 与该 stub DLL 都通过 Linux 上的 MinGW (`pkgsCross.mingwW64`) 交叉编译，整个镜像准备流程无需任何 Windows 工具。

## Results
- 成功构建并启动一个约 **~1GB** 的 Windows ValidationOS 镜像，文中称其可在**数秒内启动**。
- 成功通过 SSH 登录运行 Windows 上的 Nix：示例命令 `C:\nix\bin\nix-build C:\demo.nix` 可执行 `echo Hello` 并把结果写入 Nix store。
- 声称整个流程**无需 Windows license 或 installation**，并且**全部在 Linux 上完成**，包括交叉编译和磁盘镜像准备。
- 声称构建是**deterministic**，因为构建时不启动 VM，而是离线注入文件到磁盘镜像。
- 未提供标准学术基准、错误率、吞吐量或与其他 Windows Nix 方案的量化对比结果。

## Link
- [https://github.com/nix-windows/nix-windows-demo](https://github.com/nix-windows/nix-windows-demo)
