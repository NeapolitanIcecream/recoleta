---
source: arxiv
url: https://arxiv.org/abs/2607.07593v1
published_at: '2026-07-08T16:13:15'
authors:
- Lara Khatib
- Noble Saji Mathews
- Meiyappan Nagappan
- Pengyu Nie
- Thomas Zimmermann
topics:
- automated-program-repair
- bug-reports
- code-intelligence
- swe-bench
- llm-agents
- fault-localization
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# What Makes a Good Bug Report for an AI Agent?

## Summary
## 摘要
这篇论文研究哪些缺陷报告细节能帮助 LLM 修复代理修复真实软件缺陷。研究发现，代理最受益于可执行证据、代码和位置提示、修复建议；较长的报告与较低成功率相关。

## 问题
- APR 代理现在会读取写给人类的缺陷报告，然后检查代码库并提交补丁，不能提出澄清问题。
- 面向人类的缺陷报告指南可能不符合代理需求；起始信息质量差会让代理扩大搜索、猜测，或修改错误的代码。
- 明确哪些字段能帮助代理，对 issue 模板、开发者工具和自动化软件生产工作流很重要。

## 方法
- 研究 1 分析了 433 个 SWE-bench Verified 缺陷修复 issue，这些 issue 由 87 个代理尝试处理，共有 37,671 个代理-issue 结果，整体解决率为 47.7%。
- 作者为每份报告标注 27 个特征，包括复现步骤、堆栈跟踪、错误消息、代码片段、复现脚本、修复建议、章节标题、报告长度和故障定位线索。
- 混合效应逻辑回归在控制 issue 难度和代理能力后，估计哪些特征与成功修复相关。
- 研究 2 在 SWE-bench Pro 上进行受控消融，覆盖 2 个模型和 17 种问题陈述变体；在保持底层任务不变的情况下，移除或隔离报告内容，并改变结构。

## 结果
- 在研究 1 中，修复建议与成功的正相关最大：优势比 3.61，95% CI [2.01, 6.47]，p < 0.001。
- 报告中包含代码库源代码会提高解决概率：OR 2.82，95% CI [1.23, 6.44]，p < 0.05。
- 复现脚本也有帮助：OR 2.52，95% CI [1.41, 4.51]，p < 0.01。
- 报告中点名 ground-truth 补丁修改过的文件，与更高成功率相关：OR 2.33，95% CI [1.18, 4.60]，p < 0.05。
- 较长的报告与更差结果相关：log 报告长度每增加一个标准差，OR 为 0.49，95% CI [0.35, 0.68]，p < 0.001。
- 摘录没有给出研究 2 的精确解决率差值，但报告称，两个测试模型都依赖定位线索和预期行为；即使文本内容不变，移除列表结构或章节标题也会降低解决率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.07593v1](https://arxiv.org/abs/2607.07593v1)
