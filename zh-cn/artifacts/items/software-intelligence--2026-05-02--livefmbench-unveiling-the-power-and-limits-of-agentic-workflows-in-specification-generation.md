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
LiveFMBench 评估 LLM 和智能体式流水线为 C 程序生成 ACSL 形式化规约的能力。论文称，当前系统在增加采样、使用推理模式和采用智能体工作流时表现会提升，但如果不过滤不忠实输出，测得的准确率会被高估。

## 问题
- 为 C 程序编写正确的形式化规约成本高，并且需要掌握契约、前置条件、后置条件和循环不变式等专业知识。
- 以往的 LLM 评估可能包含来自 GitHub 或旧基准的数据泄漏，因此报告的准确率可能混合了真实能力和记忆结果。
- 当模型修改程序或断言，而不是添加有效规约时，自动证明器可能被误导，这会使朴素通过率偏高。

## 方法
- 作者构建了 LiveFMBench，其中包含 630 个带 ACSL 标注的 C 程序：270 个 2025 年前的程序，以及 360 个新收集的 SV-COMP 2025 程序，用于降低污染风险。
- 他们在直接提示、启用推理的思考模式，以及 AutoSpec 风格的智能体式流水线下评估了 15 个开源 LLM。
- 他们使用 Frama-C v27.1、Alt-Ergo 和 Z3 检查生成的 ACSL 规约能否证明目标断言。
- 他们测量 pass@1、pass@5 和 pass@32，然后通过检查 AST 等价性并保留原始断言表达式来过滤输出的忠实性。
- 他们按类型标注失败，包括缺失规约、错误的前置/后置条件、有缺陷的循环不变式，以及验证器误用。

## 结果
- 朴素评估会高估直接提示的性能：过滤不忠实输出后，真实规约生成准确率下降约 20%。
- 更多样本有帮助：pass@5 平均约为 pass@1 的 2 倍，pass@32 平均约为 pass@1 的 3 倍。
- 根据模型和设置不同，思考模式使成功率相对提升 19.40% 到 2465.52%。
- Qwen3-32B 从思考模式中获得明显收益，pass@5 从 6.33 升至 27.44。
- 智能体式流水线在低采样预算和较难数据集上帮助最大；随着采样增加，其优势会缩小。
- 失败分析发现，错误的循环不变式是最常见的错误类型；智能体式流水线减少了断言错误，但摘录未给出具体降幅。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01394v1](https://arxiv.org/abs/2605.01394v1)
