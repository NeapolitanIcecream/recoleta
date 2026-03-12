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
relevance_score: 0.05
run_id: materialize-outputs
---

# Inference-Time Safety For Code LLMs Via Retrieval-Augmented Revision

## Summary
本文提出 SOSecure：一种针对代码大模型的**推理时安全层**，先检索与生成代码相似的 Stack Overflow 安全讨论，再让模型据此修订代码。其意义在于无需重训即可利用不断更新的社区安全知识，提升代码生成的可信性与安全性。

## Problem
- 代码 LLM 虽然能生成可运行代码，但常会复现过时或危险的实现模式，导致安全漏洞进入真实软件开发流程。
- 仅靠训练时数据或重训练难以及时适应新漏洞、API 变化和安全规范更新，因此部署后的模型容易持续输出不安全代码。
- 现有提示或仅给 CWE 标签的方法缺少可解释、可操作的安全推理依据，难以稳定修复隐含漏洞。

## Approach
- 核心方法很简单：**代码先生成，再做一次“安全复查+改写”**；复查时不只靠模型自己想，而是先从 Stack Overflow 中找相似代码模式的安全讨论。
- 作者构建了一个面向安全的 Stack Overflow 知识库，筛选明确提到漏洞、风险用法、弃用接口等内容的答案和评论，并做了轻量质量过滤（至少有一次 upvote）。
- 检索阶段使用 **BM25** 而非稠密向量检索，因为代码安全往往依赖具体 API、参数或标志位（如 `shell=True`、`pickle.loads`、`debug=True`），词法匹配更可靠。
- 系统把检索到的讨论作为**建议性上下文**放入修订提示中，让 LLM 判断是否需要修改；这些社区内容不会被直接拷贝进代码，也允许模型保持原样不改。
- 该机制是模型无关、无需微调/重训的推理时干预层，强调可解释性、对新安全知识的适应性，以及在部署前实时拦截不安全输出。

## Results
- 在 **SALLM** 上，Fix Rate 从 **49.1%（Prompt-only）** 提升到 **71.7%（SOSecure）**，比仅给漏洞标签的 **GPT-4+CWE 58.5%** 更高，增幅 **+22.6 个百分点**；**Intro Rate = 0.0%**。
- 在 **LLMSecEval** 上，Fix Rate 从 **56.5%** 提升到 **91.3%**，高于 **GPT-4+CWE 69.6%**，增幅 **+34.8 个百分点**；**Intro Rate = 0.0%**。
- 在真实用户对话数据 **LMSys** 上，Fix Rate 从 **37.5%** 提升到 **96.7%**，高于 **GPT-4+CWE 45.8%**，增幅 **+59.2 个百分点**；**Intro Rate = 0.0%**。
- 在 LMSys 消融实验中，**Revision-only 41.2%**、**GPT-4+CWE 45.8%**、**SOSecure 96.7%**，说明主要增益来自**社区讨论检索**，而不是单纯让模型自我修订。
- 在 **C 语言** 的 LLMSecEval 子集上，SOSecure 的 Fix Rate 为 **73.3%**，优于 **Prompt-only 53.3%** 和 **GPT-4+CWE 60.0%**，且 **Intro Rate = 0.0%**，表明方法不局限于 Python。
- 论文的核心突破性主张是：**无需重训，仅靠推理时检索+修订，就能显著提高代码安全修复率，同时在静态分析下不引入新漏洞。**

## Link
- [http://arxiv.org/abs/2603.01494v1](http://arxiv.org/abs/2603.01494v1)
