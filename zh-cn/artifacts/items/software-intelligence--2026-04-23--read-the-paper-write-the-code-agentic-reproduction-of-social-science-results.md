---
source: arxiv
url: http://arxiv.org/abs/2604.21965v1
published_at: '2026-04-23T17:59:18'
authors:
- Benjamin Kohler
- David Zollikofer
- Johanna Einsiedler
- Alexander Hoyle
- Elliott Ash
topics:
- llm-agents
- scientific-reproducibility
- paper-to-code
- social-science
- code-generation
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Read the Paper, Write the Code: Agentic Reproduction of Social-Science Results

## Summary
## 总结
本文测试 LLM 代理能否仅凭论文中的方法描述和原始数据，复现已发表的社会科学结果，而不接触作者代码或报告的数值。基于 48 篇经人工验证可复现的论文，更强的代理配置能恢复许多已发表系数，但成功率高度依赖模型、脚手架，以及论文对方法说明的完整程度。

## 问题
- 论文研究的是，代理能否根据一篇论文及其数据重新实现经验分析，而在编码时看不到原始代码、结果或完整 PDF。
- 这之所以重要，是因为按理说传达方法细节的是论文，而不是代码仓库，论文应当足以支持独立复现。
- 以往的社会科学基准通常把原始代码也提供给代理；这项工作把目标收紧到论文到代码的复现，并使用确定性的评估，而不是让 LLM 评分。

## 方法
- 作者构建了一个四步流程：从论文包中提取方法、数据和结果，隐藏原始结果表，让代理编写新的 Python 代码填充这些表，然后将复现出的单元格与原始结果逐项比较。
- 方法提取会把论文转成结构化描述，包含数据集、筛选条件、变量构造和每张表对应的模型设定，同时去掉数值结果。
- 重新实现的代理在隔离工作区中运行，只能看到提取出的方法、表格模板和数据。它们不能访问原始代码或论文。作者会审计运行过程，检查是否访问了禁止文件或硬编码输出。
- 评估是确定性的、按单元格进行：比较符号、百分比偏差，以及系数相对于原始标准误的差距。他们也按偏差给出字母等级。
- 错误归因步骤会追踪失败来源，判断是缺少数据、论文与代码不一致、提取错误，还是代理错误。

## 结果
- 数据集：来自 I4Replication 的 48 篇论文、222 张表、14,214 个表格单元，其中包括 5,149 个系数和 4,253 个标准误。
- 在论文和表格层面，完成率都很高：代理对 92% 到 100% 的论文、82% 到 97% 的表格产出可用结果。单元格完成率整体在 52% 到 72% 之间；系数完成率平均为 82%，标准误完成率为 80%。
- 对复现出的系数，符号一致率介于 78%（SWE-Agent + GPT-5.4）到 91%（OpenCode + GPT-5.4）之间。文中给出的朴素正号基线是 68%。
- 最好的配置 OpenCode + GPT-5.4，将 80% 以上的复现系数落在原始 95% 置信区间内。表现最差的配置也超过 50%。
- 引言写道，对前三个最好的代理，复现系数与原始系数在符号上一致的比例超过 85%，落在 95% 置信区间内的比例超过 70%。
- OpenCode + GPT-5.4 是表现最好的系统，优于带 Opus 4.6 的 Claude Code、带 GPT-5.3/5.4 的 Codex CLI，以及带 GLM-5 的 OpenCode。作者报告说，脚手架选择影响很大，而 OpenCode 的优势伴随着更高的 token 使用量、成本和运行时间。
- 根因分析显示，很多失败来自论文表述不够具体，较小一部分来自提取错误，或代理没有按提取出的办法执行。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21965v1](http://arxiv.org/abs/2604.21965v1)
