---
source: arxiv
url: https://arxiv.org/abs/2606.25195v1
published_at: '2026-06-23T21:39:05'
authors:
- Rupam Patir
- Keyan Guo
- Haipeng Cai
- Hongxin Hu
topics:
- secure-code-generation
- code-intelligence
- software-security
- coding-agents
- benchmarking
- llm-evaluation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# SoK: AI Secure Code Generation: Progress, Pitfalls, and Paths Forward

## Summary
## 摘要
论文认为，评估 AI 安全代码生成时，应看模型是否理解安全编码原则，以及是否能把这些知识转化为可运行、抗利用的代码。论文提出 Kauge，这是一种评估方法，用来区分安全编码知识、代码执行能力，以及两者之间的差距。

## 问题
- 现有安全代码生成基准通常只给生成的程序打分，因此通过/失败结果可能掩盖真正原因：模型是不知道规则、把规则用错了位置，还是在阻止利用时破坏了功能。
- 这一点很重要，因为编码智能体和 LLM 现在会大规模编写和修复软件，不安全的生成代码可能进入真实应用。
- 基于静态分析的检查可能漏掉可利用漏洞，也可能奖励只满足检查器的代码；因此，可执行的功能测试和漏洞利用测试能提供更强的信号。

## 方法
- Kauge 以 OWASP 和 CERT 的安全编码原则作为度量单位，因为这些原则描述了代码应实现的防御行为。
- 该方法有 3 层：Knowledge 测试模型是否用自然语言理解安全编码原则；Actuation 测试生成代码是否具备功能并能抵抗利用；Gap 检查代码是否实现了与相关原则对应的防御机制。
- 作者构建了一个 NLU 基准，包含 6,382 道经过验证的固定答案问题，这些问题来自 456 条源规则。
- 这些问题覆盖 4 个推理维度：陈述性推理、因果推理、程序性推理和上下文推理。
- 他们还构建了漏洞利用到原则防御的映射和一个 SCP 合规性判定器，然后在 CWEval 上测试模型和编码智能体的函数级安全性，在 BaxBench 上测试完整 Web 应用的安全性。

## 结果
- 摘录没有给出准确率、相关系数、p 值或逐模型表格，因此无法根据所提供文本对其统计结论做数值核验。
- 论文称，安全编码原则理解能力是 3 类代码结果的强统计预测因素：功能正确性、安全性，以及功能和安全同时正确。
- 研究报告了持续存在的知识-执行差距：模型常能识别相关安全编码原则，却未能在正确的代码边界实现正确防御。
- 在 Knowledge 层，当前系统在 OWASP 和 CERT 原则上的得分远高于随机水平，主要弱点是较低层级 CERT C/C++ 规则的因果推理；摘录未提供具体分数。
- 在 Actuation 层，函数级失败分为两类：代码不可运行，以及代码可运行但可被利用；应用级任务则常在安全测试前失败，因为生成的后端无法运行。
- 论文识别出 4 类差距情形：按原则成功实现、通过其他方式实现安全、合规但仍有漏洞，以及直接执行失败。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25195v1](https://arxiv.org/abs/2606.25195v1)
