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
- reproducible-builds
- vm-image
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Nix on Windows –- proof-of-concept demo

## Summary
这是一个把 **Nix 包管理器带到 Windows** 的概念验证：它在 Linux 上离线构建一个可启动的 Windows ValidationOS 镜像，并预装可运行的 Nix。其意义在于展示了无需 Windows 安装流程、无需 Windows 工具链，也能以较确定性的方式为 Windows 提供 Nix 环境。

## Problem
- 目标问题：如何在 **Windows 上运行 Nix**，同时避免依赖完整 Windows 安装、许可证、手工配置或原生 Windows 构建工具。
- 这很重要，因为 Nix 强调可复现、声明式的软件构建；若能覆盖 Windows，可扩展到跨平台开发、测试和自动化交付场景。
- 具体障碍是 ValidationOS 缺少 `shell32.dll` 中 Nix 需要的 `SHGetKnownFolderPath`，导致 Nix 不能直接运行。

## Approach
- 在 Linux 上**交叉编译** `nix.exe` 及其依赖，使用 `pkgsCross.mingwW64`，完全不需要 Windows 工具链。
- 基于微软免费、轻量的 **ValidationOS**，从 ISO 提取出 VHDX，再用 `guestfish` 和 `chntpw` **离线注入**文件与注册表修改，而不是在构建时启动虚拟机。
- 注入启动脚本以关闭防火墙、配置 SSH 密钥，并修改 Winlogon，让 `cmd.exe` 默认进入 `C:\nix\bin`。
- 为绕过缺失的 `shell32.dll`，作者没有修改 Nix 本体，而是提供一个**最小 stub DLL**，仅实现 `SHGetKnownFolderPath`，通过读取 `LOCALAPPDATA`、`APPDATA`、`ProgramData` 等环境变量返回路径。
- 将该 stub DLL 放在 `nix.exe` 旁边，利用 Windows DLL 搜索顺序优先加载，从而让 Nix 在该最小 Windows 环境中工作。

## Results
- 成功构建并启动一个约 **~1GB** 的 ValidationOS Windows 镜像，且该镜像**数秒内启动**；文中未给出更严格的启动时间基准比较。
- 整个镜像构建过程被宣称为**deterministic**：构建时**不会启动 VM**，而是直接离线修改磁盘镜像；但文中没有提供可复现性测试数字或哈希对比结果。
- 演示中可通过 **SSH** 登录到 Windows VM，并执行 `C:\nix\bin\nix-build C:\demo.nix`，说明预装 Nix 可实际运行。
- 示例 derivation 会通过 `cmd.exe` 执行 `echo Hello`，并把结果写入 **Nix store**，作为端到端功能验证。
- 没有提供标准数据集、性能指标、吞吐量、成功率或相对现有 Windows Nix 方案的定量对比；最强的具体结论是：**Linux 上可离线生成并启动带 Nix 的最小 Windows VM，且能远程执行 Nix 构建。**

## Link
- [https://github.com/nix-windows/nix-windows-demo](https://github.com/nix-windows/nix-windows-demo)
