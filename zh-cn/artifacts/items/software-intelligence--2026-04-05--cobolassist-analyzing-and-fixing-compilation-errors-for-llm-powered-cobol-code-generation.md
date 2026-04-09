---
source: arxiv
url: http://arxiv.org/abs/2604.03978v1
published_at: '2026-04-05T05:51:54'
authors:
- Anh T. V. Dau
- Shin Hwei Tan
- Jinqiu Yang
- Nghi D. Q. Bui
- Anh Tuan Nguyen
topics:
- cobol-code-generation
- compiler-guided-repair
- llm-debugging
- legacy-software
- code-intelligence
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation

## Summary
## 摘要
COBOLAssist 是一个由编译器反馈引导的修复循环，用于修复 LLM 生成的 COBOL 代码。该研究分析了 LLM 在 COBOL 中会产生哪些编译错误，并表明把编译器错误反馈给模型后，可以提高编译成功率和测试通过率。

## 问题
- LLM 生成的 COBOL 经常无法通过编译，因为 COBOL 的程序结构严格、语法要求严，并且公开训练数据有限。
- 这很重要，因为 COBOL 仍在支撑关键的商业和政府系统，而有经验的 COBOL 开发者越来越少。
- 以往关于 COBOL 代码生成的工作主要衡量模型表现，没有重点研究如何自动修复生成代码中的编译错误。

## 方法
- 论文首先基于 876 个生成程序、980 个编译错误、两名标注者和 0.9 的 Cohen's kappa，构建了一个面向 LLM 生成 COBOL 代码的编译错误分类体系。
- 它将错误分为三大类：代码不完整错误、语法错误和类型相关错误。
- COBOLAssist 先生成 COBOL 代码，用 GnuCOBOL 编译，获取编译器错误日志，再提示 LLM 修改代码。
- 这一修复循环会重复进行，直到代码编译通过或达到最大迭代次数。
- 评估使用 COBOLEval 基准，共 146 个任务，并测试了多个模型：GPT-3.5、GPT-4、GPT-4o-mini、GPT-4o 和 mAInframer 各变体。

## 结果
- 在错误分析中，程序结构使用错误是 LLM 生成 COBOL 中占比最大的错误类别，为 35.1%；而在先前工作的人类编写 COBOL 中，这一比例是 19.8%。
- 研究指出，两类错误是本研究中 LLM 生成 COBOL 特有的：内置函数使用错误，占 17.2%；代码块结束不完整，占 5.6%。
- COBOLAssist 将 GPT-4o-mini 的编译成功率从 29.5% 提高到 64.38%。
- COBOLAssist 将 GPT-4o 的编译成功率从 41.8% 提高到 95.89%。
- 论文报告 mAInframer-34B 的编译成功率达到 97.94%，是所有评估模型中最高的 CSR，但函数正确性有限。
- 函数正确性也有提升：GPT-4 在 COBOLEval 上的 pass@1 从 9.1 提高到 22.6，GPT-4o 的 pass@1 从 16.4 提高到 29.45。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03978v1](http://arxiv.org/abs/2604.03978v1)
