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
## 概要
SAFEdit 是一个用于指令驱动代码编辑的 GPT-4.1 多智能体系统。它把每次编辑拆成规划、最小化代码修改、真实测试执行，以及最多 3 轮修复，以此提升 EditBench 上的任务成功率。

## 问题
- 指令驱动代码编辑要求模型在保留无关行为的前提下，根据自然语言请求修改现有代码；这很重要，因为开发助手通常修改已有文件，而不是从头写新程序。
- EditBench 显示这项任务很难：40 个受评模型里有 39 个的任务成功率低于 60%，在最有信息量的 HIGHLIGHT 设置下，最佳已报告的单模型基线达到 64.8%。
- 常见失败包括误解指令、改动无关代码、漏掉受影响的调用点，以及在没有可靠修复步骤的情况下忽略测试失败。

## 方法
- SAFEdit 使用 3 个专门代理：Planner 写结构化编辑计划，Editor 只应用必要改动，Verifier 在沙箱里运行真实单元测试。
- Planner 不写代码。它提取可见代码实体，说明编辑意图，确定目标位置，列出所需修改，并记录约束。
- Editor 把计划当作唯一依据，尽量保留格式、结构和无关代码。
- 失败测试会经过一个 Failure Abstraction Layer，把原始日志转换成字段，例如失败测试、异常类型、期望值、实际值和建议修复动作。
- 编辑-测试-修复循环最多运行 3 次，使用与 ReAct 基线相同的 GPT-4.1 主模型和测试基础设施。

## 结果
- 在 5 种自然语言和 3 种可见性变体上的 445 个 EditBench 任务中，评估共得到 1,335 个任务-变体实例。
- SAFEdit 在主要报告比较中给出 68.6% 的 TSR，高于 claude-sonnet-4 的 64.8%，差值为 +3.8 个百分点。
- 在相同的 GPT-4.1 设置下，SAFEdit 也超过了已实现的 ReAct 单智能体基线，68.6% 对 60.0%，提升 +8.6 个百分点。
- 根据论文的消融结果，迭代修复循环比首轮性能高 +17.4 个百分点。
- 过滤后的数据集在英语、波兰语、西班牙语、中文和俄语上，每种指令语言各有 89 个任务。
- 论文还称，和集中式单智能体推理基线相比，SAFEdit 的失败分析显示指令级幻觉更少，也没有回归错误，但摘录没有给出完整类别计数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25737v1](https://arxiv.org/abs/2604.25737v1)
