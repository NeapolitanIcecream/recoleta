---
source: arxiv
url: https://arxiv.org/abs/2607.11348v1
published_at: '2026-07-13T10:08:24'
authors:
- Zahra Mousavi
- Chadni Islam
- M. Ali Babar
- Alsharif Abuadbba
- Kristen Moore
topics:
- code-intelligence
- software-security
- security-api-misuse
- developer-study
- human-ai-interaction
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# Understanding the Impact of AI Code Assistants on Security API Usage: An Empirical Study

## Summary
## 摘要
该研究考察了 GitHub Copilot 对专业开发者使用安全 API 的影响。44 名开发者分别完成两个 Java 任务，其中一个使用 Copilot，另一个不使用 AI 辅助。Copilot 提高了功能正确性，但没有显著改善安全 API 的使用情况。

## 问题
- SSL/TLS 和 OAuth 等安全 API 较为复杂，误用可能导致证书验证绕过、未授权访问等漏洞。
- 以往研究主要使用固定提示词测试 AI 生成的代码，因此开发者接受、修改或拒绝建议所产生的影响仍不明确。
- 该研究考察了 Copilot 是否会改变代码正确性、安全 API 误用情况，以及开发者识别不安全结果的能力。

## 方法
- 研究人员对 44 名专业 Java 开发者开展了被试内研究。每名开发者完成一个使用 Copilot 的任务和另一个不使用 AI 辅助的任务；任务顺序和 Copilot 的使用条件经过平衡安排。
- 任务使用 Java Secure Socket Extension 实现 SSL/TLS 通信，并使用 Google OAuth 实现 Gmail 的委托访问。
- 研究人员人工检查最终代码中的安全 API 误用和功能正确性，然后使用逻辑回归比较两种条件。两名评审者的一致性很高，Cohen's kappa 为 0.97。
- 研究还分析了 Copilot 提示词和任务后的自我评估，以衡量开发者的安全意识。

## 结果
- 与无辅助开发相比，Copilot 提高了功能正确性，尤其是在更复杂的安全 API 任务中。
- Copilot 小幅减少了某些不安全模式，但没有显著改善整体安全 API 使用情况。
- 44 名参与者中只有 2 人在 Copilot 提示词中明确考虑了安全问题。许多参与者没有意识到最终代码仍然不安全，即使研究人员已经说明会进行安全性评估。
- 在研究后的分析中，针对安全问题的提示词有助于纠正部分误用，但 Copilot 仍未能避免所有安全 API 错误。
- 摘录没有提供主要比较中功能正确率、误用率或统计效应量的确切数值；其中报告了研究规模、0.97 的评审者一致性，以及研究结果的定性方向。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11348v1](https://arxiv.org/abs/2607.11348v1)
