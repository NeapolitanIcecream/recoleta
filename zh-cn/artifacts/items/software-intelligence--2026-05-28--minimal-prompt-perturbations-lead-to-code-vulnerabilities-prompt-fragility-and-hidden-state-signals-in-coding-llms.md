---
source: arxiv
url: https://arxiv.org/abs/2605.29737v1
published_at: '2026-05-28T10:30:28'
authors:
- Alexander Sternfeld
- Andrei Kucharavy
- Ljiljana Dolamic
topics:
- coding-llms
- code-security
- prompt-fragility
- hidden-state-probing
- cweval
- software-foundation-models
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Minimal Prompt Perturbations Lead to Code Vulnerabilities: Prompt Fragility and Hidden-State Signals in Coding LLMs

## Summary
## 摘要
这篇论文表明，细微的提示词编辑就能让编码 LLM 生成有漏洞的代码。它还发现，某些漏洞类型可以在生成代码之前，从提示词的隐藏状态中预测出来。

## 问题
- LLM 编码助手被用于编写可能直接交付的代码，但普通的提示词变化就可能改变生成代码是否安全。
- 先前关于提示词扰动的研究主要衡量功能正确性，没有量化拼写错误和 token 编辑对安全性的影响。
- 只看安全测试会产生误导，因为没有完成任务的代码看起来可能是安全的，所以论文把功能性和安全性一起评估。

## 方法
- 研究使用 CWEval。这个基准把每个任务配上一项功能测试和一项安全测试，覆盖 C、C++、Go、JavaScript 和 Python 中的 31 种 CWE 类型。
- 研究测试了 CodeLlama-70B、DeepSeek-Coder-33B 和 Qwen3-Coder-30B，温度设为 0。
- 研究用单字符替换、在一个 token 内的三字符替换，以及按 token embedding 相似度选出的整 token 替换来扰动提示词。
- 研究在 transformer 层的最后一个 token hidden state 上训练逻辑回归和两层 MLP probe，预测一次生成是否功能正确，以及是否同时功能正确且安全。
- probe 训练使用 80% 开发集、5 折交叉验证和 20% 留出测试集。

## 结果
- 在原始提示词上，Qwen3-Coder-30B 的 func-sec 表现最好：C 为 33.3%，C++ 为 52.4%，Go 为 38.6%，JavaScript 为 43.5%，Python 为 56.0%。CodeLlama-70B 更低：同样语言上分别为 10.0%、19.0%、14.0%、26.1% 和 40.0%。
- 单字符扰动就能把安全代码变成有漏洞的代码。在一个 DeepSeek-Coder-33B 的 Python CWE-022 案例里，把第 26/102 个 token 中的“otherwise,”改成“otherwiseV”后，tar.extractall 周围的路径遍历防护被移除，像 ../../etc/passwd 这样的条目就能写到目标路径之外。
- 温度为 0 的生成几乎稳定：324 个模型-CWE 组合里，只有 2 个在三次生成中的评估不一致。
- hidden-state probe 在各模型上对“功能正确且安全”这一联合目标的平均留出集 AUC 约为 0.70。
- 输入处理类漏洞比 secure-defaults 类漏洞更容易预测：平均 AUC 为 0.753 ± 0.038，而后者为 0.674 ± 0.037，Mann-Whitney U = 68，p = 0.009。
- 按 CWE 细分时，probe 的高 AUC 包括资源耗尽 0.857、命令注入 0.830 和 SQL 注入 0.780。低 AUC 包括弱加密（DSA）0.584 和签名验证 0.588。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29737v1](https://arxiv.org/abs/2605.29737v1)
