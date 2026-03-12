---
source: arxiv
url: http://arxiv.org/abs/2603.01494v1
published_at: '2026-03-02T06:06:34'
authors:
- Manisha Mukherjee
- Vincent J. Hellendoorn
topics:
- code-llm-safety
- retrieval-augmented-generation
- secure-code-generation
- stack-overflow
- inference-time-revision
relevance_score: 0.94
run_id: materialize-outputs
---

# Inference-Time Safety For Code LLMs Via Retrieval-Augmented Revision

## Summary
本文提出 SOSecure：一种针对代码大模型的**推理时安全层**，先为已生成代码检索相关的 Stack Overflow 安全讨论，再引导模型进行安全修订。它的核心价值是无需重训练即可利用不断更新的社区知识，提升代码生成安全性与可解释性。

## Problem
- 代码 LLM 常会生成**功能正确但存在漏洞**的代码，尤其在高风险软件开发场景中会带来真实安全隐患。
- 仅依赖训练数据会导致模型**难以及时适应新漏洞、弃用 API 和变化中的安全规范**，而重训练成本高且更新慢。
- 单纯提示模型自检，或只给出 CWE 标签，通常**缺少具体、可执行的安全推理上下文**，修复效果有限。

## Approach
- 提出 **SOSecure**：在代码生成之后运行的检索增强修订流程，而不是训练期改模或生成前注入知识。
- 从 **Stack Overflow** 构建面向安全的知识库，筛选明确提及安全风险、漏洞或不安全实践的答案及评论，并做轻量质量控制（至少有 1 个 upvote）。
- 对模型生成的代码用 **BM25 词法检索** 找到相似代码模式对应的社区安全讨论；作者认为在 `shell=True`、`pickle.loads`、`debug=True` 这类安全关键标记上，BM25 比稠密检索更可靠。
- 将检索到的讨论作为**建议性上下文**放入修订提示中，要求 LLM 判断是否需要修改；这些内容不会被直接拷贝进代码，也允许模型保持原样。
- 该机制强调三点：**可解释性**（修订依据来自人类社区解释）、**鲁棒性**（无需重训练即可吸收新知识）、**安全对齐**（在部署前做实时干预）。

## Results
- 在 **SALLM** 上，Fix Rate 从 **49.1%（Prompt-only）** 提升到 **71.7%（SOSecure）**，相对 **GPT-4+CWE 的 58.5%** 也更高；增幅为 **+22.6 个百分点**；**Intro Rate = 0.0%**。
- 在 **LLMSecEval** 上，Fix Rate 从 **56.5%** 提升到 **91.3%**，超过 **GPT-4+CWE 的 69.6%**；增幅 **+34.8 个百分点**；**Intro Rate = 0.0%**。
- 在 **LMSys** 真实对话数据上，Fix Rate 从 **37.5%** 提升到 **96.7%**，高于 **GPT-4+CWE 的 45.8%**；增幅 **+59.2 个百分点**；**Intro Rate = 0.0%**。
- 在 **LMSys 消融实验** 中，**Revision-only = 41.2%**，明显低于 **SOSecure = 96.7%**，说明提升主要来自**社区检索上下文**而非单纯让模型自我修订。
- 在 **C 语言 LLMSecEval** 子集上，**SOSecure = 73.3% Fix Rate**，优于 **Prompt-only 的 53.3%** 和 **GPT-4+CWE 的 60.0%**；**Intro Rate = 0.0%**，显示一定跨语言泛化能力。
- 论文的主要突破性主张是：**推理时、社区知识驱动的安全修订**能在多个数据集上显著提高漏洞修复率，同时**未引入新的静态分析可见漏洞**。

## Link
- [http://arxiv.org/abs/2603.01494v1](http://arxiv.org/abs/2603.01494v1)
