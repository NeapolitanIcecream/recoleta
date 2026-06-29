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
COBOLAssist 是一个由编译器引导的修复循环，用于 LLM 生成的 COBOL 代码。它研究 LLM 在 COBOL 中常见的编译错误类型，并表明把编译器错误反馈给模型可以提高编译成功率和测试通过率。

## 问题
- LLM 生成的 COBOL 经常编译失败，因为 COBOL 的程序结构固定、语法严格，而且公开训练数据有限。
- 这很重要，因为 COBOL 仍在运行关键的企业和政府系统，而有经验的 COBOL 开发者越来越难找。
- 以往的 COBOL 生成工作主要衡量模型表现，没有关注对生成的 COBOL 编译错误进行自动修复。

## 方法
- 论文先用 876 个生成程序、980 个编译错误、两名标注者和 Cohen's kappa 0.9，建立了一个面向 COBOL 的 LLM 生成代码编译错误分类体系。
- 它把错误分为三类：不完整代码错误、语法错误和类型相关错误。
- COBOLAssist 先生成 COBOL 代码，用 GnuCOBOL 编译，再读取编译器错误日志，并提示 LLM 修改代码。
- 这个修复循环会重复，直到代码通过编译或达到最大迭代次数。
- 评估使用 COBOLEval 基准，共 146 个任务和多个模型：GPT-3.5、GPT-4、GPT-4o-mini、GPT-4o，以及多个 mAInframer 变体。

## 结果
- 在错误分析中，程序结构使用错误是 LLM 生成 COBOL 中占比最大的错误类，为 35.1%，高于先前工作里人类编写 COBOL 的 19.8%。
- 这项研究报告了两种只出现在 LLM 生成 COBOL 中的错误类型：内置函数使用错误，占 17.2%；不完整块结束，占 5.6%。
- COBOLAssist 把 GPT-4o-mini 的编译成功率从 29.5% 提高到 64.38%。
- COBOLAssist 把 GPT-4o 的编译成功率从 41.8% 提高到 95.89%。
- 论文报告 mAInframer-34B 达到 97.94% 的编译成功率，是评估模型中最高的 CSR，但功能正确性仍然有限。
- 功能正确性也有提升：GPT-4 的 pass@1 从 9.1 升到 22.6，GPT-4o 的 pass@1 在 COBOLEval 上从 16.4 升到 29.45。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03978v1](http://arxiv.org/abs/2604.03978v1)
