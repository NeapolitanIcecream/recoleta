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
## 概述
本文研究程序分析中的一个新盲区：数据从代码进入 LLM 提示词后，又以文本、JSON、SQL 或代码的形式返回。文中提出一套分类法，用来描述输入占位符跨过这道边界后保留了多少信息，并展示这套分类法如何帮助污点分析和反向切片。

## 问题
- 现有程序分析依赖调用如何把输入转换为输出的摘要，但 LLM 调用没有这类摘要，因为提示词到输出的过程是不可见且依赖上下文的。
- 这会让污点分析、切片、依赖跟踪和变更影响分析在自然语言/编程语言边界处失效，这对安全和基础开发工具都很重要。
- 在集成 LLM 的应用中，攻击者控制的输入可以穿过提示词，再以可执行输出的形式出现，比如 SQL、shell 命令或代码，从而带来注入等安全风险。

## 方法
- 论文把 NL/PL 边界定义为运行时程序值被插入提示词、随后又影响被代码消费的 LLM 输出的那个点。
- 它构建了一个包含 24 个标签的分类法，覆盖两个维度：信息保留程度（从 L0 阻断到 L4 词法保留）和输出模态或形式，包括自然语言、结构化数据和可执行工件。
- 这套分类法以定量信息流理论为基础，并按每个调用点、每个占位符单独标注，因此同一个变量在不同提示上下文里可以得到不同标签。
- 为了构建和测试这套分类法，作者从 Python 代码中还原真实的 LLM 调用点，推断占位符值，生成模型输出，并标注了来自 4,154 个文件的 9,083 对占位符-输出样本。
- 在污点传播上，他们使用两阶段流程：先用基于分类法的过滤器判断占位符是否应跨越 LLM 边界传播，再由 LLM 验证器检查剩余情况。

## 结果
- 标注数据集包含来自 4,154 个真实 Python 文件的 9,083 对占位符-输出样本。
- 人工标注者在 200 对样本上得到 Cohen's kappa = 0.79，GPT 生成的标签与人工一致性达到 kappa = 0.82。
- 覆盖率接近完整：9,083 对样本中只有 1 对无法分类，约为 0.01%。
- 在污点传播预测上，这个两阶段流程在 62 个含 sink 的文件中 353 对专家标注样本上达到 F1 = 0.923。
- 论文报告了在 TypeScript 中对 6 个真实 OpenClaw 提示注入案例的跨语言验证，但节选没有给出该设置的数值结果。
- 在反向切片上，基于分类法的过滤让含有不传播占位符的文件的切片大小平均减少 15%，而 4 个阻断标签覆盖了几乎所有不传播案例。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28345v1](http://arxiv.org/abs/2603.28345v1)
