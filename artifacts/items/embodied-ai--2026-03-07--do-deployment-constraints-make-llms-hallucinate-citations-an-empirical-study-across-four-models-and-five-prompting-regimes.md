---
source: arxiv
url: http://arxiv.org/abs/2603.07287v1
published_at: '2026-03-07T17:14:05'
authors:
- Chen Zhao
- Yuan Tang
- Yitian Qian
topics:
- llm-hallucination
- citation-verification
- academic-writing
- prompting-evaluation
- reliability
relevance_score: 0.02
run_id: materialize-outputs
---

# Do Deployment Constraints Make LLMs Hallucinate Citations? An Empirical Study across Four Models and Five Prompting Regimes

## Summary
这篇论文实证研究了在不同部署约束下，LLM 生成学术引用时会多大程度地产生“看起来正确但无法验证”的文献。结论是：约束越强，尤其是时间窗口约束和组合约束，引用可验证性显著下降，而且格式合规并不代表引用真实。

## Problem
- 论文要解决的问题是：**现实部署中的提示约束**（如限定年份、要求综述式覆盖面、禁止声称记忆训练数据）会如何影响 LLM 生成引用的**可验证性**。
- 这很重要，因为 LLM 已被用于学术写作、系统综述和软件工程证据综合；如果模型捏造参考文献，错误会被带入研究、工具链和决策流程。
- 以往工作多只看单一提示设置或二分类“真实/伪造”，不足以刻画现实使用中大量“难以自动确认”的高风险引用。

## Approach
- 作者构建了一个**封闭书本（closed-book）**评测：不给检索，只让模型根据 144 个学术主张生成一段简短学术文字和结构化参考文献。
- 评测了 4 个模型（Claude Sonnet、GPT-4o、LLaMA 3.1–8B、Qwen 2.5–14B）在 5 种提示条件下的表现：Baseline、Temporal、Survey、Non-Disclosure、Combo，总计 **2,880 次运行、17,443 条引用**。
- 他们设计了一个**确定性验证流水线**：解析每条引用后，用 DOI/标题去查 **Crossref + Semantic Scholar**，再用标题、作者、年份、期刊等字段做加权相似度匹配。
- 每条引用被标为 **Existing / Unresolved / Fabricated** 三类，而不是强行二分类；其中 Unresolved 表示自动系统无法可靠判断，但人工审计显示其中相当一部分其实是伪造的。
- 流水线还做了人工验证：抽样 100 条引用，自动标注与人工标注的一致率 **75%**，Cohen’s **κ=0.63**，说明该自动评估可用但对 Unresolved 偏保守。

## Results
- **没有任何模型、任何条件下的 citation-level existence rate 超过 0.50**；全论文最高值是 **Claude Sonnet 在 Survey 条件下 0.475**，说明即便最好模型也不能保证大多数引用真实。
- Baseline 下，专有模型明显优于开源权重模型：Claude **0.381**、GPT-4o **0.235**，而 LLaMA **0.068**、Qwen **0.090**；专有 vs 开源差距为 **Δ=+0.229，95% CI [0.191, 0.266]**。
- **Temporal 是伤害最大的单一约束**：Claude existence rate 从 **0.381 降到 0.119**（**Δ=-0.261**），GPT-4o 从 **0.235 降到 0.019**（**Δ=-0.216**）；但时间违规率却极低，仅 **0.001–0.026**，说明模型“遵守年份格式”，却给不出真实可验证的文献。
- **Combo 条件最差**：Claude **0.106**、GPT-4o **0.005**、LLaMA **0.008**、Qwen **0.001**；同时模型仍平均生成 **7.38–7.99** 条引用，表现为“继续输出很多引用，但几乎不可验证”。
- **Survey 条件拉大了专有/开源差距**：该差距达到全 study 最大值 **Δ=+0.310 [0.274, 0.349]**。其中 Claude 反而从 **0.381 升到 0.475**（**Δ=+0.094**），而 Qwen 降到 **0.020**，且 fabricated rate 达到全篇最高 **0.547**。
- **Unresolved 是最大风险桶**：各设置下占比 **36%–61%**。人工审计中，35 条 Unresolved 里有 **16 条其实是 fabricated**、只有 **4 条是 existing**，表明论文报告的 fabricated rate 很可能还是保守估计。

## Link
- [http://arxiv.org/abs/2603.07287v1](http://arxiv.org/abs/2603.07287v1)
