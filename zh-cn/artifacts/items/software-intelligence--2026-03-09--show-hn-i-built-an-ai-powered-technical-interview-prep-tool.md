---
source: hn
url: https://crackr.dev/
published_at: '2026-03-09T23:32:17'
authors:
- wa5ina
topics:
- voice-ai
- technical-interview
- coding-practice
- ai-feedback
- developer-tools
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: I built an AI-powered technical interview prep tool

## Summary
这是一个面向技术面试训练的语音 AI 工具，模拟资深工程师进行实时提问、追问、提示与评分。它把语音对话、真实编码环境和赛后复盘整合在一起，目标是提升候选人的面试表现而不仅是刷题能力。

## Problem
- 技术面试准备通常只练题目本身，缺少**真实面试中的口头表达、压力应对、追问互动和反馈**。
- 传统练习工具往往是表单式或静态题库，无法像真实面试官那样**实时听、问、质疑、给提示并评分**。
- 这很重要，因为候选人是否拿到 offer，不仅取决于是否写出答案，还取决于**如何解释思路、处理 dead ends、在压力下沟通和编码**。

## Approach
- 核心方法是一个**实时语音 AI 面试官**：它会说话、听你回答、根据你的表现继续追问或指出问题，尽量复现资深工程师面试官的互动方式。
- 使用 **Claude** 负责推理、追问和反馈生成；用 **WebRTC** 实现低延迟双向语音；在 **Monaco Editor** 中提供接近 VS Code 的真实编码体验。
- 练习流程是：选择目标公司/主题/编程语言 → 进入语音面试 → 在编辑器中写代码并运行测试 → 结束后获得**五个维度的评分卡**和具体失分反馈。
- 简单说，它不是给你一道题然后等提交，而是像真人一样一边听你讲解、一边看你写代码、必要时施压或给提示，最后做结构化复盘。

## Results
- 文本**没有提供正式实验、基准数据或离线评测结果**，因此没有可核验的准确率、提升幅度或与竞品/人工面试的量化对比。
- 明确的系统性能声明包括：**WebRTC 实现 sub-100ms 双向实时语音**。
- 产品能力声明包括：提供**1 次免费面试**；付费按 credit 计费，**1 credit = 15 分钟 session**；价格示例为 **10 credits 每次 $1.00、25 credits 每次 $0.88、50 credits 每次 $0.78**。
- 功能层面的最强主张是：AI 能像真实高级工程师一样**实时追问、指出死路、在卡住时给提示，并在结束后输出五维评分与书面反馈**。
- 还宣称练习支持**目标公司、主题和语言自适应**，并在 **Monaco/VS Code 风格环境**中进行，而不是玩具式界面。

## Link
- [https://crackr.dev/](https://crackr.dev/)
