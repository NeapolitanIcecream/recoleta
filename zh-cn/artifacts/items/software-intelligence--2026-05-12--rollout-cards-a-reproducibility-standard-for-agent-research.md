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
## 摘要
论文主张，智能体研究应发布运行轨迹记录、视图、报告规则和省略字段，而不只发布头部得分。论文提出 rollout cards，并通过审计和重新评分测试说明，报告选择会改变智能体基准测试的结论。

## 问题
- 智能体评测常常只发布得分，不发布支撑这些得分的运行轨迹记录，后续研究者因此无法检查模型动作、工具调用、失败情况、计时或环境状态。
- 不同评分和报告规则会给同一智能体行为分配不同分数，导致系统之间的比较不可靠。
- 这个问题影响软件智能体、工具使用智能体、多智能体系统和安全研究，因为重新运行前沿模型的轨迹成本可能很高，原始模型、工具和环境设置也可能已经不存在。

## 方法
- rollout card 存储每个 episode 的证据：任务、环境状态、观测、模型输出、工具调用、工具结果、产物、计时、终止状态和失败信息。
- 每张卡声明用于报告得分的视图、计算该得分的报告规则，以及 drops manifest，列出该得分使用或省略了哪些字段、行或结构。
- 作者在开源强化学习 gym Ergon 中实现该规范，同时说明其他系统也可以输出同一 bundle 格式。
- 他们通过把公开智能体产物转换为 rollout-card 导出，并在不同公开报告规则下对固定基准测试输出重新评分，来测试这个想法。

## 结果
- 在对 50 个热门训练和评测代码库的审计中，没有一个在头部准确率或得分旁报告失败、出错或跳过的 rollout。
- 审计发现 37 处报告规则差异，涉及任务成功率、成本/token 统计和计时。例子包括：提示模板导致 MMLU 最高相差 24.6 个百分点，缓存 token 统计相差 2.0 倍，Aider 案例中同一模型家族的成本相差 14.41 美元，以及匹配硬件上的运行时间相差 3.1 倍。
- 论文发布了 21 个 rollout-card 导出：17 个轨迹发布导出，以及 4 个分析性或恢复视图的非轨迹导出，覆盖工具使用、软件工程、网页交互、多智能体协调、安全和搜索。
- 对固定基准测试产物重新评分后，报告得分最高变化 20.9 个绝对百分点，并且可能在 tau-bench 上交换 GPT-4o 和 Claude 3.5 Sonnet 的排名。
- 在 MLE-Bench 上，改变 medal/pass 报告定义后，通过率从 34.2% 变为 13.3%。
- 对公开 rollout 的重新分析发现了具体隐藏信号：在 GAP 中，4,855 个文本安全样本里有 1,002 个，即 20.64%，仍然进行了不安全的工具调用；在 MAESTRO 中，失败运行的中位数为 48 个 span 和 78,523 个 token，成功运行为 10 个 span 和 11,586 个 token；在 COPRA miniF2F 日志中，全部 44 次一步尝试都成功，而 864 次较长尝试中只有 74 次成功。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12131v1](https://arxiv.org/abs/2605.12131v1)
