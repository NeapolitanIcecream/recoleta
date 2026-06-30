---
source: arxiv
url: https://arxiv.org/abs/2606.30182v1
published_at: '2026-06-29T11:57:32'
authors:
- Tom Adamczewski
- David Owen
- David Rein
- Florian Brand
- Giles Edkins
- Allen Hart
- Daniel O'Connell
topics:
- code-intelligence
- software-benchmarks
- autonomous-coding
- program-synthesis
- ai-agents
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# MirrorCode: AI can rebuild entire programs from behavior alone

## Summary
## 摘要
MirrorCode 是一个基准，用来测试 AI agent 能否在没有源代码的情况下，仅根据行为重建完整的命令行程序。论文称，在规格说明精确且推理预算较大的情况下，前沿 agent 已经能完成一些耗时较长的软件重实现任务。

## 问题
- 当前的编程基准大多测试短任务，因此对较大型软件项目中的自主工作只能提供较弱证据。
- 一次性演示，例如 AI 构建编译器或浏览器，难以比较，因为其中的人类指导程度和完成度并不清楚。
- 这个问题很重要，因为长周期自主编程比小型 bug 修复或孤立函数更接近真实的软件生产。

## 方法
- MirrorCode 让 agent 获得一个现有 CLI 程序的仅执行访问权限、文档和可见输入输出测试，但不提供源代码或互联网访问。
- agent 使用六种语言之一编写替代程序：Python、C、Rust、Go、OCaml 或 Ada。
- 评分使用端到端测试：替代程序必须精确匹配原程序的 `stdout` 和 `stderr`。
- 隐藏测试平均占测试总数的 34%，用于检查 agent 是否实现了行为，而不是记住可见用例。
- 该基准包含 25 个目标程序，覆盖 Unix 工具、数据序列化、查询工具、生物信息学、解释器、静态分析、密码学和压缩；其中 22 个目标已发布，3 个为私有。

## 结果
- Claude Opus 4.7 的报告分数最高：在 MirrorCode 上，100% 解决率的平均分为 56%。GPT-5.5 得分 44%，Gemini 3.1 Pro Preview 得分 32%。
- 在 ≥99% 测试通过阈值下，Claude Opus 4.7 得分 77%，GPT-5.5 得分 57%，Gemini 3.1 Pro Preview 得分 44%。
- 在 25 个目标程序中，17 个至少有一次运行取得满分，另有 4 个有一次运行超过 99%。
- Claude Opus 4.7 在 14 小时内以 251 美元重实现了 `gotree`，这是一个约 16,000 行 Go 代码、包含 40 多个命令的生物信息学工具包；它通过了 2,001 个测试中的 2,000 个，即 99.95%。作者估计，不使用 AI 的人类工程师需要 2–17 周。
- 论文报告称，Opus 4.7 还重实现了 `pkl`，这是 Apple 的一种配置语言，代码量约 60,000 行。
- 最难的任务仍未解决：25 个目标中有 8 个从未达到 100%，25 个中有 4 个从未达到 99%，而 `ruff` 的最佳运行在隐藏测试上只达到 67%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30182v1](https://arxiv.org/abs/2606.30182v1)
