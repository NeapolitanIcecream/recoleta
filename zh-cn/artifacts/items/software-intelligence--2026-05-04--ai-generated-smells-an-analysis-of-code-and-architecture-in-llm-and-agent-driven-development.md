---
source: arxiv
url: https://arxiv.org/abs/2605.02741v1
published_at: '2026-05-04T15:41:13'
authors:
- Yuecai Zhu
- Nikolaos Tsantalis
- Peter C. Rigby
topics:
- llm-code-generation
- code-maintainability
- technical-debt
- static-analysis
- multi-agent-software-engineering
- ai-generated-code-smells
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# AI-Generated Smells: An Analysis of Code and Architecture in LLM and Agent-Driven Development

## Summary
## 摘要
论文认为，LLM 和智能体生成的代码可以通过功能测试，但仍然带有可维护性债务。它研究了单文件编码任务和 MetaGPT 生成的代码仓库中的代码异味。

## 问题
- 功能正确性基准会漏掉代码异味，例如长方法、高耦合、不稳定依赖和上帝类结构。
- 这很重要，因为这些缺陷会提高维护成本，让重构更冒险，也可能藏在能正常运行的 AI 生成软件里。
- 论文问的是，随着项目复杂度上升，提示词和智能体协作能否减少这些缺陷。

## 方法
- 实验 I 用 Gemini 2.5 Pro、Llama 3.3 70B、deepseek-coder-v2 16B、qwen3-coder 30B 和 qwen3-coder 480B，在 zero-shot 和 few-shot 提示下，为 90 个 CodeContest 题目生成 Python 解答。
- 这 90 个题目也各使用了一份经过验证的人工 Python 提交作为基线。
- 实验 II 使用 MetaGPT 和 Qwen-Coder 480B，为 5 个应用场景生成完整的 Python 仓库，每个场景都有 4 个逐步提高要求的阶段。
- PyExamine 检测代码、结构和架构层面的异味；cloc 测量总代码行数；研究还记录了总文件数和 Agent Action Count。
- 核心机制很直接：在受控任务规模下生成代码，对每个产物运行同一个静态异味检测器，再按模型、提示、正确性和代码量比较异味数量与类型。

## 结果
- 实验 I 覆盖 90 个题目、5 个 LLM 变体、2 种提示条件和一个人工基线；摘录没有给出具体的异味计数表或通过率。
- 对算法任务，论文称 qwen3-coder 480B 这类更强的模型在处理更难逻辑时会产生更多 Long Method 膨胀；人工提交更常出现 Temporal Fields。
- 实验 II 覆盖 5 个场景 × 4 个阶段 = 20 个 MetaGPT 项目；论文称异味模式会转向 Too Many Branches、Potential Improper API Usage、Unstable Dependency 和 God Class 结构。
- 论文称总代码行数几乎可以完美预测架构退化，但摘录没有给出系数、p 值或回归表。
- 论文还称 few-shot 或更详细的提示不会减少可维护性退化，功能正确性和结构质量也彼此脱钩；摘录没有给出数值效应大小。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02741v1](https://arxiv.org/abs/2605.02741v1)
