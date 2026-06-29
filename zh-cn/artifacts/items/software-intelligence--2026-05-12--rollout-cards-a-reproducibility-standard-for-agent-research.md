---
source: arxiv
url: https://arxiv.org/abs/2605.12131v1
published_at: '2026-05-12T13:54:31'
authors:
- Charlie Masters
- Ziyuan Liu
- Stefano V. Albrecht
topics:
- agent-reproducibility
- rollout-traces
- evaluation-standards
- software-agents
- multi-agent-systems
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Rollout Cards: A Reproducibility Standard for Agent Research

## Summary
## 总结
本文主张，智能体研究应公布 rollout 记录、视图、报告规则和省略字段，而不只是头条分数。作者提出 rollout cards，并通过审计和重新评分测试表明，报告方式的选择会改变智能体基准的结论。

## 问题
- 智能体评测常常只公布分数，而不公布这些分数背后的 rollout 记录，因此后续研究者无法检查模型动作、工具调用、失败、时序或环境状态。
- 不同的评分和报告规则会给同一种智能体行为分配不同分数，这让系统之间的比较不可靠。
- 这个问题会影响软件智能体、工具使用智能体、多智能体系统和安全研究，因为重新运行前沿 rollout 的成本可能很高，而且原始模型、工具和环境配置可能已经不存在。

## 方法
- rollout card 记录每个 episode 的证据：任务、环境状态、观测、模型输出、工具调用、工具结果、产物、时序、终止状态和失败情况。
- 每张卡都声明用于已报告分数的视图、计算该分数的报告规则，以及一个 drops manifest，列出分数使用或省略了哪些字段、行或结构。
- 作者把这个规范实现到 Ergon，一个开源强化学习 gym，同时说明其他系统也可以输出同样的 bundle 格式。
- 他们通过把公开智能体产物转换成 rollout-card 导出，并在不同公开报告规则下重新评分固定基准输出来测试这个想法。

## 结果
- 在对 50 个常用训练和评测仓库的审计中，没有一个在头条准确率或分数旁边报告失败、出错或被跳过的 rollout。
- 审计发现了 37 处报告规则差异，涉及任务成功率、成本/token 计费和时序。例子包括：MMLU 因提示模板带来最高 24.6 个百分点的差距、缓存 token 计费差异为 2.0 倍、Aider 案例中同一模型家族的成本差异为 14.41 美元，以及在匹配硬件上的 3.1 倍运行时差距。
- 论文公开了 21 个 rollout-card 导出：17 个带轨迹的发布导出和 4 个分析或恢复视图的非轨迹导出，覆盖工具使用、软件工程、网页交互、多智能体协调、安全和搜索。
- 对固定基准产物重新评分后，报告分数最高变化达到 20.9 个绝对百分点，并且在 tau-bench 上可能互换 GPT-4o 和 Claude 3.5 Sonnet 的排名。
- 在 MLE-Bench 上，改变 medal/pass 的报告定义后，pass rate 从 34.2% 变为 13.3%。
- 对公开 rollout 的再分析发现了具体的隐藏信号：在 GAP 中，4,855 个 text-safe 样本里有 1,002 个，也就是 20.64%，仍然发出了不安全的工具调用；在 MAESTRO 中，失败运行的中位 spans 为 48、tokens 为 78,523，而成功运行分别为 10 和 11,586；在 COPRA miniF2F 日志中，所有 44 个一步尝试都成功，而更长的 864 次尝试里只有 74 次成功。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12131v1](https://arxiv.org/abs/2605.12131v1)
