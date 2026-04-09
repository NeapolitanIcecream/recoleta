---
source: arxiv
url: http://arxiv.org/abs/2603.28345v1
published_at: '2026-03-30T12:14:24'
authors:
- Zihao Xu
- Xiao Cheng
- Ruijie Meng
- Yuekang Li
topics:
- llm-program-analysis
- taint-analysis
- program-slicing
- code-security
- nl-pl-boundary
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Crossing the NL/PL Divide: Information Flow Analysis Across the NL/PL Boundary in LLM-Integrated Code

## Summary
## 摘要
这篇论文研究了程序分析中的一个新盲点：数据从代码进入 LLM 提示词，再以文本、JSON、SQL 或代码的形式返回。论文提出了一套分类体系，用来描述输入占位符有多少信息能跨过这条边界，并表明这套分类有助于污点分析和后向切片。

## 问题
- 现有程序分析依赖函数调用如何把输入转换为输出的摘要，但 LLM 调用不提供这类摘要，因为从提示词到输出的过程不透明，而且依赖上下文。
- 这会在自然语言/编程语言边界上破坏污点分析、切片、依赖跟踪和变更影响分析，而这既影响安全，也影响基础开发工具。
- 在集成 LLM 的应用中，攻击者控制的输入可能穿过提示词，并在 SQL、shell 命令或代码等可执行输出中再次出现，从而带来注入等安全风险。

## 方法
- 论文将 NL/PL 边界定义为这样一个位置：程序运行时的值被插入提示词，随后影响被代码消费的 LLM 输出。
- 论文沿两个维度建立了一个包含 24 个标签的分类体系：信息保留程度（从 L0 完全阻断到 L4 词法保留）以及输出模态或形式，包括自然语言、结构化数据和可执行产物。
- 这套分类建立在定量信息流理论之上，并且按每个占位符、每个调用点应用，因此同一个变量在不同提示词上下文中可能得到不同标签。
- 为了构建和测试这套分类，作者从 Python 代码中重建真实的 LLM 调用点，推断占位符取值，生成模型输出，并对来自 4,154 个文件的 9,083 个占位符-输出对进行标注。
- 在污点传播任务中，他们使用两阶段流程：先用基于分类的过滤来预测占位符是否应跨越 LLM 边界传播，再由一个 LLM 验证器检查剩余情况。

## 结果
- 标注数据集覆盖来自 4,154 个真实 Python 文件的 9,083 个占位符-输出对。
- 人工标注者在一个包含 200 对样本的子集上达到 Cohen's kappa = 0.79，GPT 生成的标签与人工共识的一致性为 kappa = 0.82。
- 覆盖率接近完整：9,083 对中只有 1 对无法分类，约为 0.01%。
- 在污点传播预测上，两阶段流程在来自 62 个包含 sink 的文件、共 353 对由专家标注的样本上达到 F1 = 0.923。
- 论文报告了在 6 个真实 OpenClaw prompt-injection TypeScript 案例上的跨语言验证，但摘录没有给出该设置下的数值结果。
- 在后向切片中，基于该分类的过滤使包含非传播占位符的文件平均切片大小减少了 15%，并且四个阻断类标签覆盖了几乎所有非传播情况。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28345v1](http://arxiv.org/abs/2603.28345v1)
