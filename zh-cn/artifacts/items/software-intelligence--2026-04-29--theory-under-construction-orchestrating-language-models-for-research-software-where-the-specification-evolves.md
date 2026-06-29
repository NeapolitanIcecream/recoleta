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
Comet-H 是一个控制器，用于在理论、代码、基准和论文都在运行过程中变化时，借助语言模型构建研究软件。论文最强的主张是，明确的落地和审计步骤可以防止长时间的 LM 开发过程积累未经支持的说法。

## 问题
- 它针对的是规范仍在形成中的研究软件项目，因此数学论题、可执行代码、基准表面和公开表述可能彼此偏离。
- 这很重要，因为 LM 可能把自己未经支持的说法复制到后续提示、论文、README、代码改动和基准选择中。
- 论文指出了两种失败模式：幻觉积累，以及理论、代码、证据、主张和模型对仓库的过时认知之间的不同步。

## 方法
- Comet-H 把项目工作区看成六个跟踪部分：理论、仓库、公开表述、证据、效用假设和未完成义务。
- 控制器会重新读取磁盘上的工作区，用当前缺口对 17 类提示进行评分，并用手动设定的线性分数选择下一个提示。
- 新主张会生成后续义务，并随时间衰减，所以最近未检查的工作会优先处理，而更早未解决的事项会逐渐淡出。
- 任何论文或 README 的改动都会先触发落地步骤，再触发审慎审计，因此公开表述必须回指到代码、命令、基准输出或记录。
- 理论变更只允许通过相邻移动来完成，这类移动要保留现有能力，并改进至少一个测试、基准或落地记录。

## 结果
- 该系统产出了 46 个研究软件仓库，覆盖约二十多个领域；引言还写到 12+ 个领域。
- 一次标准运行会生成 10 个仓库的批次，表 1 将 Comet-H 的运行记为持续 24–48 小时，并支持可变指标和多会话操作。
- 详细分析的 a3 仓库在一个包含 90 个案例的 Python 静态分析基准上达到 F1 = 0.768，而次优基线的 F1 = 0.364。
- 作者报告称，加入理论/实践耦合层会带来单调的消融提升，但摘录没有给出消融表的具体数值。
- 论文报告了大约 400 次协同开发提交中的观察结果，并说审计和收缩步骤主导了成功运行的后期阶段。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27209v2](https://arxiv.org/abs/2604.27209v2)
