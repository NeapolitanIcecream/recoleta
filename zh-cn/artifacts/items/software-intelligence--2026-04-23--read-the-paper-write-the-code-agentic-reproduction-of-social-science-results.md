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
## 摘要
这篇论文测试：LLM 代理能否只根据论文中的方法描述和原始数据，在看不到作者代码和论文中报告数值的情况下，复现已发表的社会科学结果。在 48 篇经人工验证可复现的论文上，较强的代理配置可以恢复许多已发表的系数，但成功率很大程度上取决于模型、scaffold，以及论文对方法说明得是否完整。

## 问题
- 论文研究的是：代理能否仅根据论文及其数据，重新实现一项实证分析，而在编写代码时看不到原始代码、结果或完整 PDF。
- 这很重要，因为科学研究的方法应当由论文而不是代码仓库来传达，并且应当足以支持独立复现。
- 此前社会科学基准通常会向代理提供原始代码；这项工作考察更严格的“从论文到代码”的复现，并使用确定性的评估，而不是让 LLM 来打分。

## 方法
- 作者构建了一个四步流程：从论文材料包中提取方法、数据和结果信息；遮蔽原始结果表；让代理编写新的 Python 代码来填充这些表；然后将复现出的单元格与原始结果逐一比较。
- 方法提取会把论文转换成结构化描述，包含数据集、筛选条件、变量构造和各个表对应的模型设定，同时移除数值结果。
- 重新实现的代理在隔离工作区中运行，只能访问提取出的方法、表格模板和数据。它们不能访问原始代码或论文。作者还审计运行过程，检查是否存在违规文件访问或硬编码输出。
- 评估是确定性的，粒度到单元格：他们比较符号、百分比偏差，以及对系数来说按原始标准误缩放后的差距。他们还根据偏差给出字母等级。
- 错误归因步骤会把失败追溯到数据缺失、论文与代码不一致、提取错误，或代理失误。

## 结果
- 数据集：来自 I4Replication 的 48 篇论文、222 张表、14,214 个表格单元，其中包括 5,149 个系数和 4,253 个标准误。
- 论文和表格层面的完成率都很高：代理为 92% 到 100% 的论文、82% 到 97% 的表生成了可用结果。整体单元格完成率在 52% 到 72% 之间；系数完成率平均为 82%，标准误完成率为 80%。
- 在成功复现的系数中，符号一致率从 78%（SWE-Agent + GPT-5.4）到 91%（OpenCode + GPT-5.4）不等。论文给出的“正号”朴素基线为 68%。
- 最佳配置 OpenCode + GPT-5.4 能让超过 80% 的复现系数落在原始 95% 置信区间内。表现最差的配置也超过 50%。
- 引言指出，对表现最好的三个代理来说，复现系数与原始系数的符号一致率超过 85%，落在 95% 置信区间内的比例超过 70%。
- OpenCode + GPT-5.4 是表现最好的系统，优于 Claude Code with Opus 4.6、Codex CLI with GPT-5.3/5.4，以及 OpenCode with GLM-5。作者报告说，scaffold 的选择影响很大，而 OpenCode 的优势伴随着高得多的 token 使用量、成本和运行时间。
- 根因分析显示，许多失败来自论文说明不足，较小一部分来自提取错误或代理没有按提取出的方法执行。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21965v1](http://arxiv.org/abs/2604.21965v1)
