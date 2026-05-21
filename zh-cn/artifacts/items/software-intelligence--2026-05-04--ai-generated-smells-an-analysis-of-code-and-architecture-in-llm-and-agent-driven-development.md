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
论文认为，LLM 和智能体生成的代码可能通过功能测试，但仍带有可维护性债务。研究对象包括单文件编码任务中的代码异味，以及 MetaGPT 生成的代码仓库。

## 问题
- 功能正确性基准会漏掉长方法、高耦合、不稳定依赖、God Class 结构等代码异味。
- 这些缺陷会提高维护成本，增加重构风险，并可能隐藏在可运行的 AI 生成软件中。
- 论文考察在项目复杂度增长时，提示词和智能体协作是否会减少这些缺陷。

## 方法
- 实验 I 使用 Gemini 2.5 Pro、Llama 3.3 70B、deepseek-coder-v2 16B、qwen3-coder 30B 和 qwen3-coder 480B，在零样本和少样本提示条件下，为 90 个 CodeContest 问题生成 Python 解法。
- 同样的 90 个问题各使用一份已验证的人类 Python 提交作为基线。
- 实验 II 使用 MetaGPT 和 Qwen-Coder 480B，为 5 个应用场景创建完整的 Python 代码仓库，每个场景包含 4 个需求递增阶段。
- PyExamine 检测代码、结构和架构异味；cloc 测量总代码行数；研究还记录了总文件数和 Agent Action Count。
- 核心机制很简单：在受控任务规模下生成代码，对每个产物运行同一个静态异味检测器，并按模型、提示词、正确性和代码量比较异味数量与类型。

## 结果
- 实验 I 覆盖 90 个问题、5 个 LLM 变体、2 种提示条件和一个人类基线；摘录没有给出精确的异味数量表或通过率。
- 对于算法任务，论文称 qwen3-coder 480B 等更强模型在处理更难逻辑时会产生更多 Long Method 膨胀；人类提交更常出现 Temporal Fields。
- 实验 II 覆盖 5 个场景 × 4 个阶段 = 20 个 MetaGPT 项目；论文称异味模式转向 Too Many Branches、Potential Improper API Usage、Unstable Dependency 和 God Class 结构。
- 论文称总代码行数几乎可以完美预测架构衰退，但摘录没有给出系数、p 值或回归表。
- 论文称少样本或详细提示不会减少可维护性衰退，功能正确性与结构质量脱钩；摘录没有给出数值效应量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02741v1](https://arxiv.org/abs/2605.02741v1)
