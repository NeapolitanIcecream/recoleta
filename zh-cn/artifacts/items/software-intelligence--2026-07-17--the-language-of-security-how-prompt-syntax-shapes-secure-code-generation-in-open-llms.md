---
source: arxiv
url: https://arxiv.org/abs/2607.15937v1
published_at: '2026-07-17T13:20:21'
authors:
- Matteo Cicalese
- Antonio Della Porta
- Stefano Lambiase
- Emanuele Iannone
- Torge Hinrichs
- Riccardo Scandariato
- Fabio Palomba
topics:
- secure-code-generation
- open-llms
- prompt-engineering
- code-security
- static-analysis
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# The Language of Security: How Prompt Syntax Shapes Secure Code Generation in Open LLMs

## Summary
## 摘要
本文研究细粒度的提示语法是否会改变开放式大语言模型生成代码的安全性。论文提出通过解析器驱动的提示扰动，识别可能增加漏洞风险的句法元素。

## 问题
- 大语言模型生成的代码通常包含安全漏洞，而以往的提示工程研究主要关注高层指令和专有模型。
- 论文考察移除特定从句、守卫条件、限定语或其他句法成分是否会改变漏洞发生率；这一问题关系到更安全且更具可复现性的自托管代码生成。

## 方法
- 作者解析了来自 LLMSecEval 的 150 条安全相关提示，并通过每次仅移除一个句法成分来创建变体。
- 他们按照成分类型、粒度和句中位置描述每次移除，然后分析单个特征及其组合。
- 他们使用 Qwen 2.5 32B、Athene-V2 72B 和 Phi-4 14.7B，在 C、Java 和 Python 中生成代码。
- 他们使用 CodeQL 的默认语言查询套件进行标注：当检测到至少一个 CWE 时，将代码片段标记为存在漏洞；同时采用卡方检验、Cramer’s V、Barnard 精确检验、风险比和 Benjamini-Hochberg 校正。

## 结果
- 实验包含 150 条基线提示，以及每种语言的 4,320 条提示变体；涵盖 C、Java 和 Python 的提示共 12,960 条。
- 三个开放式模型总共生成了 40,230 个代码解答。
- 摘录显示，开头从句、句末成分的移除，以及省略守卫条件、限定语或概念绑定，都与更高的漏洞率相关。
- 由于实证结果部分在所提供的文本中被截断，摘录未提供确切的漏洞率、统计显著性数值、效应量、风险比或按模型和语言划分的比较结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15937v1](https://arxiv.org/abs/2607.15937v1)
