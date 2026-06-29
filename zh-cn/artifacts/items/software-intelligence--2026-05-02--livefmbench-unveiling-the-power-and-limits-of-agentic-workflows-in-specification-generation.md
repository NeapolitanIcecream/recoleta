---
source: arxiv
url: https://arxiv.org/abs/2605.01394v1
published_at: '2026-05-02T11:31:33'
authors:
- Dong Xu
- Jialun Cao
- Guozhao Mo
- Junjie Hu
- Cheng Wen
- Hongyu Lin
- Xianpei Han
- Shengchao Qin
- Cong Tian
- Shing-Chi Cheung
- Le Sun
- Yaojie Lu
topics:
- formal-specification
- code-intelligence
- llm-evaluation
- agentic-workflows
- program-verification
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation

## Summary
## 摘要
LiveFMBench 评估了 LLM 和 agentic pipeline 为 C 程序生成 ACSL 形式化规格的效果。论文指出，当前系统会随着采样、推理模式和 agent 工作流而提升，但如果不剔除不忠实输出，测得的准确率会被抬高。

## 问题
- 为 C 程序编写正确的形式化规格成本高，需要掌握契约、前置条件、后置条件和循环不变式。
- 以往的 LLM 评估可能混入来自 GitHub 或旧基准的数据泄漏，因此报告的准确率可能同时包含真实能力和记忆。
- 当模型改动程序或断言，而不是补充有效规格时，自动证明器也可能被蒙过，这会让朴素通过率偏高。

## 方法
- 作者构建了 LiveFMBench，包含 630 个带 ACSL 标注的 C 程序：270 个 2025 年之前的程序和 360 个新收集的 SV-COMP 2025 程序，用来降低污染风险。
- 他们在直接提示、支持推理的 thinking mode，以及 AutoSpec 风格的 agentic pipeline 下评估了 15 个开源 LLM。
- 他们使用 Frama-C v27.1、Alt-Ergo 和 Z3 检查生成的 ACSL 规格是否能证明目标断言。
- 他们测量 pass@1、pass@5 和 pass@32，并通过检查 AST 等价性和保留原始断言表达式来筛除不忠实输出。
- 他们按类型标注失败，包括缺失规格、错误的前置/后置条件、有缺陷的循环不变式，以及误用验证器。

## 结果
- 朴素评估会高估直接提示的表现：在过滤不忠实输出后，真实的规格生成准确率下降了约 20%。
- 更多采样有帮助：平均来看，pass@5 约为 pass@1 的 2 倍，pass@32 约为 pass@1 的 3 倍。
- 根据模型和设置不同，thinking mode 相对提升成功率 19.40% 到 2465.52%。
- Qwen3-32B 从 thinking mode 中获益明显，pass@5 从 6.33 升到 27.44。
- 在较低采样预算和更难的数据集上，agentic pipeline 的帮助最大；随着采样增加，它的优势会缩小。
- 失败分析发现，错误的循环不变式是最常见的错误类型；agentic pipeline 减少了断言错误，但摘录没有给出具体降幅。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01394v1](https://arxiv.org/abs/2605.01394v1)
