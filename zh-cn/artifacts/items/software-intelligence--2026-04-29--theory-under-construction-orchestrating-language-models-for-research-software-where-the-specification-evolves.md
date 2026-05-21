---
source: arxiv
url: https://arxiv.org/abs/2604.27209v2
published_at: '2026-04-29T21:28:17'
authors:
- Halley Young
- "Nikolaj Bj\xF6rner"
topics:
- llm-orchestration
- code-intelligence
- research-software
- software-agents
- multi-agent-engineering
- automated-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves

## Summary
## 摘要
Comet-H 是一个控制器，用于在理论、代码、基准测试和论文都会在运行过程中变化时，使用语言模型构建研究软件。论文最有力的主张是，显式的溯源和审计步骤可以防止长时间的 LM 开发运行不断积累缺乏支持的声明。

## 问题
- 它面向规格仍在形成中的研究软件项目，因此数学论点、可执行代码、基准测试面和公开声明可能彼此偏离。
- 这一点很重要，因为 LM 可能把自己缺乏支持的声明复制到后续提示、论文、README、代码修改和基准选择中。
- 论文命名了两种失败模式：幻觉累积，以及理论、代码、证据、声明和模型对仓库的过时理解之间的不同步。

## 方法
- Comet-H 将项目工作区视为六个被跟踪的部分：理论、仓库、公开声明、证据、效用假设和未完成义务。
- 控制器重新读取磁盘上的工作区，根据当前缺口对 17 个提示家族打分，并用手工设定的线性分数选择下一个提示。
- 新声明会产生后续义务，这些义务会随时间衰减，因此近期未检查的工作会获得优先级，而旧的未解决事项会淡出。
- 任何论文或 README 变更都会触发一次溯源步骤，然后进行一次审慎审计，因此公开声明必须指向代码、命令、基准输出或账本。
- 理论变更只允许通过相邻移动进行，这些移动必须保留现有能力，并改进至少一个测试、基准或溯源记录。

## 结果
- 该系统在约二十多个领域生成了 46 个研究软件仓库；引言中也写到 12 个以上领域。
- 一次标准运行会生成 10 个仓库的批次，表 1 将 Comet-H 运行列为持续 24–48 小时，带有可变指标和多会话操作。
- 深入研究的 a3 仓库在一个包含 90 个案例的 Python 静态分析基准上达到 F1 = 0.768，而次优基线为 F1 = 0.364。
- 作者报告称，加入理论/实践耦合层后，消融结果单调提升，但摘录没有给出消融表的数值。
- 论文报告了约 400 次编排式开发提交中的观察结果，并称审计和收缩过程主导了成功运行的后期阶段。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27209v2](https://arxiv.org/abs/2604.27209v2)
