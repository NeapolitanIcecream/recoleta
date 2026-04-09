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
## 摘要
greywall 是一个面向 AI 编码代理的无容器沙箱。它把文件系统、网络和系统调用访问收缩到配置文件允许的范围，而不是直接给代理完整的用户权限。它针对 Claude Code、Cursor、Codex 和 Aider 这类工具中常见的安全缺口。

## 问题
- AI 编码代理通常以与开发者相同的权限运行，因此错误命令、不安全的依赖，或幻觉出的 shell 操作，都可能接触 SSH 密钥、shell 配置、云凭证，或主目录中的任何文件。
- 现有隔离方案通常要用 Docker 或虚拟机，这会给日常编码工作带来额外配置成本、卷挂载摩擦和工具链损坏。
- 更轻量的最小权限层很重要，因为当前代理配置一旦出错，影响范围往往就是整个机器账户。

## 方法
- greywall 是一个单二进制沙箱，在不使用 Docker 或虚拟机的情况下实施默认拒绝控制。
- 在 Linux 上，它结合了 bubblewrap 命名空间、seccomp 过滤器、Landlock 文件系统规则和 eBPF 跟踪；在 macOS 上，它生成 Seatbelt 配置文件，按选择开放文件和网络访问。
- 它内置了 13 种代理的配置文件，并支持学习模式：用 `strace` 跟踪真实文件访问，再把这些跟踪结果转成可复用的最小权限配置文件。
- 它的命令拦截会解析 shell 结构，包括管道、`&&`、`||`、子 shell 和带引号的字符串，因此即使命令包在 shell 语法里，仍然能拦截被禁止的命令。
- 当内核功能缺失时，这个设计会使用回退行为，因此沙箱仍可在保护减弱的情况下运行，而不是直接失败。

## 结果
- 摘录中没有给出基准分数或受控安全评估指标。
- 声称的实现规模：约 17,400 行 Go 代码，4 个直接依赖，13 个文件中的 151 个测试。
- 声称的产品覆盖范围：内置 13 个 AI 代理的配置文件，包括 Claude Code、Cursor、Codex 和 Aider。
- 声称的系统调用覆盖范围：seccomp 会阻止 30 多个危险系统调用，如 `ptrace`、`mount`、`reboot`、`bpf` 和 `perf_event_open`。
- 声称的项目成熟度信号：GitHub 约 109 到 110 个 stars，23 天内发布 8 个版本，几小时内合并外部贡献。
- 已报告的限制：原子文件写入可能失效，因为临时文件和目标文件在沙箱内可能落在不同文件系统上；文中也提到 WSL 的 DNS 问题，以及 AppArmor 与 TUN 设备的冲突。

## Problem

## Approach

## Results

## Link
- [https://www.wshoffner.dev/blog/greywall](https://www.wshoffner.dev/blog/greywall)
