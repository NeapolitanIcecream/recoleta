---
source: arxiv
url: https://arxiv.org/abs/2604.25737v1
published_at: '2026-04-28T15:04:46'
authors:
- Noam Tarshish
- Nofar Selouk
- Daniel Hodisan
- Bar Ezra Gafniel
- Yuval Elovici
- Asaf Shabtai
- Eliya Nachmani
topics:
- instructed-code-editing
- multi-agent-systems
- code-intelligence
- llm-verification
- automated-program-repair
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# SAFEdit: Does Multi-Agent Decomposition Resolve the Reliability Challenges of Instructed Code Editing?

## Summary
## 摘要
SAFEdit 是一个用于按指令编辑代码的 GPT-4.1 多智能体系统。它声称通过把每次编辑拆分为规划、最小代码修改、真实测试执行和最多 3 轮修复，提高了 EditBench 任务成功率。

## 问题
- 按指令编辑代码要求模型根据自然语言请求修改现有代码，同时保留无关行为；这很重要，因为开发者助手经常编辑现有文件，而不是编写全新程序。
- EditBench 显示这项任务很难：40 个被评估模型中有 39 个的任务成功率低于 60%，在信息最充分的 HIGHLIGHT 设置下，已报告的最佳单模型基线达到 64.8%。
- 常见失败包括误读指令、修改无关代码、遗漏受影响的调用点，以及在测试失败后缺少有依据的修复步骤。

## 方法
- SAFEdit 使用 3 个专门智能体：Planner 编写结构化编辑计划，Editor 只应用必要修改，Verifier 在沙箱中运行真实单元测试。
- Planner 不编写代码。它提取可见代码实体，说明编辑意图，确定目标位置，列出所需修改，并记录约束。
- Editor 把计划视为事实来源，并尝试保留格式、结构和无关代码。
- 失败测试会进入 Failure Abstraction Layer，该层把原始日志转换为失败测试、异常类型、期望值、实际值和建议修复动作等字段。
- 编辑-测试-修复循环最多运行 3 次，使用与 ReAct 基线相同的 GPT-4.1 骨干模型和测试基础设施。

## 结果
- 在 5 种自然语言和 3 种可见性变体的 445 个 EditBench 任务上，评估生成了 1,335 个任务-变体实例。
- SAFEdit 在主要报告对比中的 TSR 为 68.6%，高于 claude-sonnet-4 的 64.8%，提升 +3.8 个百分点。
- SAFEdit 优于已实现的 ReAct 单智能体基线：68.6% 对 60.0%，在相同 GPT-4.1 设置下提升 +8.6 个百分点。
- 根据论文的消融结论，迭代优化循环相比首轮性能增加 +17.4 个百分点。
- 过滤后的数据集在英语、波兰语、西班牙语、中文和俄语这几种指令语言中各包含 89 个任务。
- 论文还声称，与集中式单智能体推理基线相比，其失败分析显示 SAFEdit 的指令级幻觉更少，且没有回归错误，但摘录未提供完整类别计数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25737v1](https://arxiv.org/abs/2604.25737v1)
