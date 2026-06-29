---
source: hn
url: https://www.wshoffner.dev/blog/greywall
published_at: '2026-03-30T23:01:53'
authors:
- ticktockbent
topics:
- ai-agent-sandboxing
- code-assistant-security
- least-privilege
- filesystem-isolation
- developer-tools
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# The Blackwall Between Your AI Agent and Your Filesystem

## Summary
## 概要
greywall 是一个不给 AI 编程代理完整用户权限的无容器沙箱，而是把文件系统、网络和 syscall 访问收紧到一个配置文件范围内。它面向 Claude Code、Cursor、Codex 和 Aider 这类工具里常见的安全缺口。

## 问题
- AI 编程代理通常和开发者使用同样的权限，所以一条错误命令、一个不安全的依赖，或者一次幻觉出来的 shell 操作，都可能碰到 SSH 密钥、shell 配置、云凭证，或者主目录里的任何文件。
- 现有隔离方案往往要用 Docker 或虚拟机，这会增加配置成本、卷挂载摩擦，以及日常编码工作里的工具链故障。
- 更轻量的最小权限层很重要，因为当前代理环境里的失败影响范围常常就是整个机器账户。

## 方法
- greywall 是一个单二进制沙箱，在不使用 Docker 或虚拟机的情况下应用默认拒绝控制。
- 在 Linux 上，它结合 bubblewrap 命名空间、seccomp 过滤器、Landlock 文件系统规则和 eBPF 跟踪；在 macOS 上，它生成带有选择性文件和网络访问权限的 Seatbelt 配置文件。
- 它内置了 13 个代理的配置文件，并支持学习模式，用 `strace` 跟踪真实文件访问，再把这些跟踪结果转成可复用的最小权限配置文件。
- 它的命令拦截会解析 shell 结构，包括管道、`&&`、`||`、子 shell 和带引号的字符串，所以即使命令被 shell 语法包起来，也能拦住。
- 这个设计在缺少某个内核特性时会回退到可用路径，所以沙箱仍然能运行，只是保护会减弱，而不是直接失败。

## 结果
- 这段摘录没有给出基准分数或受控的安全评估指标。
- 声称的实现规模：大约 17,400 行 Go，4 个直接依赖，以及分布在 13 个文件里的 151 个测试。
- 声称的产品覆盖：13 个 AI 代理的内置配置文件，包括 Claude Code、Cursor、Codex 和 Aider。
- 声称的 syscall 覆盖：seccomp 阻止了 30 多个危险 syscall，例如 `ptrace`、`mount`、`reboot`、`bpf` 和 `perf_event_open`。
- 声称的项目成熟度信号：大约 109 到 110 个 GitHub 星标、23 天内 8 个版本，以及几小时内合并的外部贡献。
- 报告的限制：原子文件写入可能出问题，因为临时文件和目标文件在沙箱里可能落到不同的文件系统上；文中还提到 WSL 的 DNS 问题和 AppArmor 与 TUN 设备的冲突。

## Problem

## Approach

## Results

## Link
- [https://www.wshoffner.dev/blog/greywall](https://www.wshoffner.dev/blog/greywall)
