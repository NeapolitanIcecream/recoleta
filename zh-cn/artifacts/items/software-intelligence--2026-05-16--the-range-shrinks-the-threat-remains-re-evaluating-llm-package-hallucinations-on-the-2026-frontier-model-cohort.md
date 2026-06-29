---
source: arxiv
url: https://arxiv.org/abs/2605.17062v1
published_at: '2026-05-16T16:08:52'
authors:
- Aleksandr Churilov
topics:
- llm-code-generation
- package-hallucination
- software-supply-chain
- slopsquatting
- code-intelligence
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort

## Summary
## 摘要
本文测量了五个 2026 年具备代码能力的 LLM 的包名幻觉，发现幻觉率已收敛到约 5%–6%，但 slopsquatting 风险仍然存在。最重要的新发现是有 127 个不存在的包名被五个模型全部幻觉出来，说明存在共享的攻击面。

## 问题
- 生成代码的 LLM 有时会在安装命令或导入语句中建议并不存在的 PyPI 或 npm 包。
- 攻击者可以先注册这些名字，等开发者安装恶意包，从而形成软件供应链风险。
- 这篇论文想回答的是，更新的前沿模型是否比 Spracklen 等人 2024 年的模型组降低了这种风险。

## 方法
- 研究在 Claude Sonnet 4.6、Claude Haiku 4.5、GPT-5.4-mini、Gemini 2.5 Pro 和 DeepSeek V3.2 上复现了 Spracklen 等人的包名幻觉方法。
- 它运行了 199,845 个 Python 和 JavaScript 提示词，使用的提示集与早期工作相同，来自 Stack Overflow 和 LLM 合成提示。
- 研究从安装命令和 import 语句中提取包名，再与 PyPI 和 npm 主列表比对。
- 它报告了幻觉率、置信区间、模型两两差异、语言拆分，以及独特幻觉名称的重叠情况。

## 结果
- 总体幻觉率从 Claude Haiku 4.5 的 4.62% 到 GPT-5.4-mini 的 6.10%；Spracklen 2024 年的范围是 5.2%–21.7%。
- 模型间差距从 2024 年那组的 16.5 个百分点缩小到这组 2026 年模型的 1.48 个百分点，收窄了 11 倍。
- 论文识别出 127 个被五个模型都幻觉出来的包名：其中 109 个在 PyPI 上，18 个在 npm 上。
- 对每个模型来说，Python 的幻觉率都高于 JavaScript：Python 范围是 5.49% 到 7.27%，JavaScript 范围是 2.62% 到 3.78%。
- Claude Haiku 4.5 的幻觉率低于 Claude Sonnet 4.6，分别为 4.62% 和 5.41%，经 Holm 校正后的差距为 0.79 个百分点。
- DeepSeek V3.2 和 GPT-5.4-mini 在幻觉名称上的重叠最高，Jaccard 相似度 J = 0.343；平均两两 Jaccard 值为 0.222.

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17062v1](https://arxiv.org/abs/2605.17062v1)
