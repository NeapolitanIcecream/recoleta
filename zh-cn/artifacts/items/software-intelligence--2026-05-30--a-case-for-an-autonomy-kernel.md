---
source: hn
url: https://autonomykernel.org/
published_at: '2026-05-30T23:29:32'
authors:
- offbeatport
topics:
- autonomy-kernel
- agent-runtime
- ai-agents
- agent-governance
- auditability
- human-ai-interaction
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# A case for an Autonomy Kernel

## Summary
## 概要
本文主张建立一个 autonomy kernel：在自主代理下方放一个稳定的运行时，用来控制权限、记录动作、保留状态，并让 principal 随时停止代理。

## 问题
- 现在的代理常常只是受 prompt 约束的会话，但用户越来越希望它们带着真实权限连续工作数天。
- 代理工具缺少一个共享层，用来命名正在运行的工作、授予有限范围的权限、审计动作、保留连续性，以及收回权限。
- 这很重要，因为长时间运行的代理需要可追责、可停止，并且能在不同模型和供应商之间迁移。

## 方法
- 核心模型有 3 层：agent 是进程，model 是其中的推理引擎，kernel 是两者下方的运行时。
- 权限从 1 个 principal 开始。目的沿着 principal、intent、goal、task、process、action 传递；权力沿着 policy、capability、lease、syscall 传递。
- 在任何 action 运行前，kernel 都会检查它是否同时具有可追踪的目的和明确授予的权限。
- kernel 保持小体量，并负责 5 个机制：execution、identity、authority、communication 和 auditing。
- memory 是对 audit record 的精选、可擦除投影；audit record 才是持久的事实来源。

## 结果
- 这段摘录没有给出基准测试、数据集、实现结果或定量比较。
- 它提出了 9 条面向自主系统的设计主张，包括可丢弃的 agents、可替换的 models、可追踪的 intent、明确的 authority、完整的审计能力、principal 主权、受治理的 memory 和小型 kernel。
- 它定义了 3 项标准化承诺：稳定且有版本的边界、带有保证退出能力的可移植状态，以及不可转移的问责。
- 它主张每个 action 在执行前都必须对应 1 个 principal 和 1 条可恢复的授权路径。
- 它还主张采用方式可以是增量式的：现有工具应当在无需重写的情况下运行在 kernel 之上，但这段摘录没有提供采用数据。

## Problem

## Approach

## Results

## Link
- [https://autonomykernel.org/](https://autonomykernel.org/)
