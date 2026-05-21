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
本文测量了 5 个具备代码能力的 2026 年 LLM 的包名幻觉，发现幻觉率已收敛到约 5–6%，但 slopsquatting 风险仍然存在。它最强的新主张是：5 个模型都会幻觉出同一组 127 个不存在的包名。

## 问题
- 生成代码的 LLM 有时会在安装命令或 import 语句中建议不存在的 PyPI 或 npm 包。
- 攻击者可以注册这些名称，并等待开发者安装恶意包，从而造成软件供应链风险。
- 论文研究较新的前沿模型是否比 Spracklen et al. 的 2024 年模型组降低了这一风险。

## 方法
- 研究在 Claude Sonnet 4.6、Claude Haiku 4.5、GPT-5.4-mini、Gemini 2.5 Pro 和 DeepSeek V3.2 上复现了 Spracklen et al. 的包幻觉方法。
- 研究运行了 199,845 个 Python 和 JavaScript 提示，使用与早期工作相同的 Stack Overflow 提示集和 LLM 合成提示集。
- 研究从安装命令和 import 语句中提取包名，然后用 PyPI 和 npm 主列表进行校验。
- 研究报告了幻觉率、置信区间、模型两两差异、语言分组结果，以及唯一幻觉名称的重叠情况。

## 结果
- 总体幻觉率从 Claude Haiku 4.5 的 4.62% 到 GPT-5.4-mini 的 6.10%；2024 年 Spracklen 研究中的范围为 5.2%–21.7%。
- 模型间差距从 2024 年模型组的 16.5 个百分点缩小到 2026 年模型组的 1.48 个百分点，缩窄了 11 倍。
- 论文识别出 127 个由 5 个模型共同幻觉出的包名：PyPI 上 109 个，npm 上 18 个。
- 每个模型的 Python 幻觉率都高于 JavaScript：Python 范围为 5.49% 到 7.27%，JavaScript 范围为 2.62% 到 3.78%。
- Claude Haiku 4.5 的幻觉率低于 Claude Sonnet 4.6，分别为 4.62% 和 5.41%；Holm 校正后的差距为 0.79 个百分点。
- DeepSeek V3.2 和 GPT-5.4-mini 在幻觉名称上的重叠最高，Jaccard 相似度 J = 0.343；两两 Jaccard 均值为 0.222。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17062v1](https://arxiv.org/abs/2605.17062v1)
