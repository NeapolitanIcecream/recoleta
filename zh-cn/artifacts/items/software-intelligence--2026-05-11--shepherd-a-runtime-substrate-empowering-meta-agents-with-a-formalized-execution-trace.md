---
source: arxiv
url: https://arxiv.org/abs/2605.10913v1
published_at: '2026-05-11T17:50:51'
authors:
- Simon Yu
- Derek Chong
- Ananjan Nandi
- Dilara Soylu
- Jiuding Sun
- Christopher D Manning
- Weiyan Shi
topics:
- agent-runtime
- multi-agent-systems
- code-intelligence
- execution-tracing
- agent-rl
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace

## Summary
## 总结
Shepherd 是一个面向元代理的运行时，它把代理执行记录成带类型、类似 Git 的轨迹，这样监督者就能检查、分叉、重放和修改运行中的代理。论文报告称，它比 Docker 风格的快照分支更快，并且在实时编码监督、工作流优化和强化学习训练中带来任务提升。

## 问题
- 基于 LLM 的代理系统现在会使用元代理，在执行过程中监督、编辑或训练其他代理。
- 现有运行时大多只暴露对话记录、工具日志或环境快照，这让在精确状态下回退、分支、重放或干预运行中的代理变得困难。
- 这很重要，因为多代理编码、工作流搜索和代理强化学习会在每条备选路径都要完整重跑时浪费时间。

## 方法
- Shepherd 把代理当作带类型的任务，输入和输出也带类型，因此元代理可以传递它、调用它、替换它，或把它和其他任务组合起来。
- 每次模型调用、工具调用、文件系统写入和环境动作都会变成追加式执行轨迹中的一个带类型效应。
- 这条轨迹的工作方式类似 Git：每个动作是一个提交，每次分叉是一条分支，合并会保留子分支，丢弃会移除它而不改变父分支。
- 分叉时，代理进程和文件系统会一起复制，并带有写时复制隔离，这样备选后续路径可以从同一个过去状态运行。
- 核心操作用 Lean 形式化的代数效应演算来定义，重放会保留精确的提示前缀，以便调用方的提示缓存复用。

## 结果
- 在 Terminal-Bench 2.0 镜像上，Shepherd 在 42 MB 到 5.8 GB 的不同镜像大小下分叉耗时为 134–143 ms；Docker commit 需要 658–725 ms，而完整根文件系统复制在 5.8 GB 镜像上最高要 53,462 ms。
- 在 5.8 GB 镜像上，Shepherd 回退需要 147 ms，而 Docker commit 为 828 ms，完整复制为 25,943 ms。
- 在 5.8 GB 镜像上，当 K=4 条分支时，Shepherd 报告磁盘开销为 30 KB，内存开销为 25.7 MB，每条分支额外存储 10 KB。
- 在 Anthropic Claude Haiku 4.5 上，重放在 8 个 Terminal-Bench 2.0 任务中的提示缓存命中率约为 95%。
- 实时监督者把 CooperBench 配对编码通过率从 28.8% 提高到 54.7%，接近报告的 57.2% 单人上限。
- 反事实元优化相比 MetaHarness 和 GEPA 最多高 11 分，且端到端时间最多低 58%；Tree-RL 则把 Qwen3.5-35B-A3B 上的 TerminalBench-2 从 34.2% 提高到 39.4%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10913v1](https://arxiv.org/abs/2605.10913v1)
