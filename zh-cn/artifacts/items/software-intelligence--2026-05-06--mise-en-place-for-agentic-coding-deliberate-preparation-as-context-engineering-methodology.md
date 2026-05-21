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
MEP 是一种准备优先的智能体编码方法，要求开发者先写上下文、规格说明和任务记录，再让智能体写代码。论文的证据来自一个黑客松案例，因此这些主张有参考价值，但尚未通过对照组验证。

## 问题
- AI 编码智能体可以快速生成代码，但上下文不足会导致代码偏离需求，并带来调试、重构和安全风险。
- 论文引用了 GitHub Copilot 研究，其中报告任务完成速度提升 21-55%；还引用了 Veracode 2025 报告，其中称 45% 的 AI 生成代码存在安全缺陷。
- 这一点重要，因为当产品意图、架构和领域知识仍停留在隐性层面时，智能体的速度可能把成本转移到验证和返工上。

## 方法
- 阶段 1，上下文奠基：用结构化 Markdown 文档记录隐性领域知识，供智能体读取。
- 阶段 2，协作式规格说明：通过人与智能体对话，写出包含界面、交互、数据流、质量标准和排除项的设计产物。
- 阶段 3，任务拆解：把规格说明转换为带依赖关系的 JSON 任务记录，并附上验收标准，然后把可独立执行的任务分配给并行智能体。
- 该方法借鉴了逆向设计和隐性知识外化；论文把相关技能称为 context fluency。

## 结果
- 在 2026 年 1 月的一场黑客松中，约有 12 支团队，构建时间窗口为 5 小时；实践者在实现前花了约 2 小时做准备。
- 准备阶段产出了 10 份规划文档、9,386 个词、一份产品规格说明和 64 条结构化任务记录。
- 四个并行子智能体在 184 分钟内实现了各个功能区域；43 个任务被关闭，中位关闭时间为 5.9 分钟。
- 最终系统包含 43 个 TypeScript/TSX 文件和 8,496 行源代码，并作为一个全栈教育平台完成部署。
- 按词数与代码行数计算，规划与代码的比例为 1.10:1；论文报告的准备时间与智能体主动实现时间比例约为 5.7:1。
- 部署和打磨阶段在 52 分钟内产生了 9 次提交；缺陷任务的中位解决时间为 1.2 分钟，实现任务为 9.7 分钟。论文报告架构返工接近零，但没有对照基线，因此不能证明因果关系。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05400v1](https://arxiv.org/abs/2605.05400v1)
