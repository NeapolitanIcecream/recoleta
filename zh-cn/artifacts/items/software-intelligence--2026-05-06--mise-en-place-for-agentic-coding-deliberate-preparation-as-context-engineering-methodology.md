---
source: arxiv
url: https://arxiv.org/abs/2605.05400v1
published_at: '2026-05-06T19:33:08'
authors:
- Andrew Zigler
topics:
- agentic-coding
- context-engineering
- code-intelligence
- multi-agent-software-engineering
- human-ai-interaction
- software-specification
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Mise en Place for Agentic Coding: Deliberate Preparation as Context Engineering Methodology

## Summary
## 摘要
MEP 是一种面向 agentic coding 的先准备后编码方法，要求开发者先写上下文、规格和任务记录，再让 agent 写代码。论文的证据只来自一个黑客松案例，所以这些结论有用，但还没有和对照组验证。

## 问题
- AI 编码 agent 产码很快，但上下文不足会导致代码偏离目标、调试、重构和安全风险。
- 论文引用了 GitHub Copilot 的研究，报告任务完成速度提升 21–55%，还引用了 Veracode 2025 报告，称 45% 的 AI 生成代码包含安全缺陷。
- 这很重要，因为当产品意图、架构和领域知识仍然隐含时，agent 的速度会把成本转移到验证和返工上。

## 方法
- 第 1 阶段，语境奠基：把默认存在于人脑中的领域知识写进结构化 Markdown 文档，供 agent 读取。
- 第 2 阶段，协同规格化：通过人和 agent 的对话，写出包含界面、交互、数据流、质量标准和排除项的设计产物。
- 第 3 阶段，任务拆分：把规格转成带依赖关系的 JSON 任务记录和验收标准，然后把独立任务分配给并行 agent。
- 该方法借鉴了 backward design 和隐性知识外显化；论文把相关能力称为 context fluency。

## 结果
- 在 2026 年 1 月的一场黑客松中，约 12 支队伍、5 小时开发窗口里，实践者在实现前花了约 2 小时准备。
- 准备阶段产出了 10 份规划文档、9,386 个词、1 份产品规格和 64 条结构化任务记录。
- 4 个并行子 agent 在 184 分钟内实现了功能区域；43 个任务完成，任务关闭的中位时间是 5.9 分钟。
- 最终系统包含 43 个 TypeScript/TSX 文件和 8,496 行源代码，作为一个全栈教育平台部署上线。
- 按词数和代码行数计算，规划到代码的比例是 1.10:1；论文还报告了约 5.7:1 的准备阶段与活跃 agent 实现阶段比例。
- 部署和打磨用了 52 分钟、9 次提交；修复 bug 的任务中位完成时间是 1.2 分钟，实现类任务是 9.7 分钟。论文报告架构返工接近于零，但没有对照基线，因此不能证明因果关系。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05400v1](https://arxiv.org/abs/2605.05400v1)
