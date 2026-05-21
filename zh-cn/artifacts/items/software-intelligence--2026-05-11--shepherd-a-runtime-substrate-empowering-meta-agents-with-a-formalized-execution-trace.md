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
## 摘要
Shepherd 是一个面向元智能体的运行时，它把智能体执行记录为带类型、类似 Git 的轨迹，让监督者可以检查、分叉、重放和修改正在运行的智能体。论文报告称，它的分支创建速度快于 Docker 式快照，并在实时编码监督、工作流优化和强化学习训练任务上带来提升。

## 问题
- LLM 智能体系统现在会使用元智能体，在执行过程中监督、编辑或训练其他智能体。
- 现有运行时大多只暴露对话记录、工具日志或环境快照，因此很难在保留精确状态的情况下，对正在运行的智能体回退、分叉、重放或介入。
- 这会影响多智能体编码、工作流搜索和智能体强化学习，因为每条替代路径都需要完整重跑，会浪费时间。

## 方法
- Shepherd 把智能体视为带类型输入和输出的带类型任务，因此元智能体可以传递它、调用它、替换它，或把它与其他任务组合。
- 每次模型调用、工具调用、文件系统写入和环境动作都会成为追加式执行轨迹中的一个带类型 effect。
- 这条轨迹的工作方式类似 Git：每个动作是一个 commit，每次 fork 是一个 branch，merge 会保留子分支，discard 会移除子分支且不改变父分支。
- Fork 会用写时复制隔离同时复制智能体进程和文件系统，因此替代后续执行可以从同一个过去状态开始运行。
- 核心操作用 Lean 机械化验证的代数 effect 演算来规定，重放会保留精确的 prompt 前缀，以便复用提供商的 prompt cache。

## 结果
- 在 Terminal-Bench 2.0 镜像上，Shepherd 对 42 MB 到 5.8 GB 的不同镜像大小执行 fork 需要 134–143 ms；Docker commit 需要 658–725 ms，完整根文件系统复制在 5.8 GB 镜像上最高需要 53,462 ms。
- 在 5.8 GB 镜像上，Shepherd revert 需要 147 ms，而 Docker commit 需要 828 ms，完整复制需要 25,943 ms。
- 对 5.8 GB 镜像上的 K=4 个分支，Shepherd 报告磁盘开销为 30 KB、RAM 开销为 25.7 MB，每个分支的存储为 10 KB。
- 在 8 个 Terminal-Bench 2.0 任务上，Anthropic Claude Haiku 4.5 的重放达到约 95% 的 prompt-cache 命中率。
- 实时监督者把 CooperBench 结对编码通过率从 28.8% 提高到 54.7%，接近论文报告的 57.2% 单人上限。
- 反事实元优化比 MetaHarness 和 GEPA 最多高 11 分，wall-clock 最多降低 58%；Tree-RL 将 Qwen3.5-35B-A3B 在 TerminalBench-2 上的成绩从 34.2% 提高到 39.4%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10913v1](https://arxiv.org/abs/2605.10913v1)
