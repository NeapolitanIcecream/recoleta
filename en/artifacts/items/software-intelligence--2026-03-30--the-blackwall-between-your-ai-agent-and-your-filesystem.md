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
language_code: en
---

# The Blackwall Between Your AI Agent and Your Filesystem

## Summary
greywall is a container-free sandbox for AI coding agents that cuts filesystem, network, and syscall access down to a profile instead of giving the agent your full user permissions. It targets a common safety gap in tools like Claude Code, Cursor, Codex, and Aider.

## Problem
- AI coding agents usually run with the same permissions as the developer, so a bad command, unsafe dependency, or hallucinated shell action can touch SSH keys, shell config, cloud credentials, or any file in the home directory.
- Existing isolation often means Docker or VMs, which add setup cost, volume-mount friction, and toolchain breakage for routine coding work.
- A lighter least-privilege layer matters because the failure scope of current agent setups is often the whole machine account.

## Approach
- greywall is a single-binary sandbox that applies deny-by-default controls without Docker or VMs.
- On Linux it combines bubblewrap namespaces, seccomp filters, Landlock filesystem rules, and eBPF tracing; on macOS it generates Seatbelt profiles with selective file and network access.
- It ships with built-in profiles for 13 agents and supports a learning mode that traces real file access with `strace` and turns that trace into a reusable least-privilege profile.
- Its command blocking parses shell structure, including pipes, `&&`, `||`, subshells, and quoted strings, so blocked commands can still be caught when they are wrapped in shell syntax.
- The design uses fallback behavior when a kernel feature is missing, so the sandbox can still run with reduced protection rather than fail outright.

## Results
- The excerpt does not report benchmark scores or controlled security evaluation metrics.
- Claimed implementation scope: about 17,400 lines of Go, 4 direct dependencies, and 151 tests across 13 files.
- Claimed product coverage: built-in profiles for 13 AI agents, including Claude Code, Cursor, Codex, and Aider.
- Claimed syscall coverage: seccomp blocks 30+ dangerous syscalls such as `ptrace`, `mount`, `reboot`, `bpf`, and `perf_event_open`.
- Claimed project maturity signals: about 109 to 110 GitHub stars, 8 releases in 23 days, and a merged external contribution in a few hours.
- Reported limits: atomic file writes can break because temp files and targets may land on different filesystems inside the sandbox; WSL DNS issues and AppArmor conflicts with TUN devices are also named.

## Link
- [https://www.wshoffner.dev/blog/greywall](https://www.wshoffner.dev/blog/greywall)
