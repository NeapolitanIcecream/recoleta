---
source: arxiv
url: http://arxiv.org/abs/2604.01437v1
published_at: '2026-04-01T22:24:08'
authors:
- Jingyue Li
- "Andr\xE9 Storhaug"
topics:
- agentic-ai-evaluation
- software-engineering
- llm-agents
- reproducibility
- trajectory-analysis
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering

## Summary
## 摘要
本文研究软件工程中的 agentic AI 系统是如何被评估的，并指出当前做法难以复现，也难以解释。文中提出了具体的报告规范，以及一种围绕发布和分析 Thought-Action-Result（TAR）日志的轨迹式评估方法。

## 问题
- 软件工程代理的评估常依赖黑箱 LLM 行为、随机输出和不完整报告，这让结果难以复现和比较。
- 作者对 18 篇近期 SE 论文的回顾显示，只有 1 篇论文将结果与相关的、最先进的 agentic 基线进行比较，因此许多所谓的提升其实是相对于更弱的基线，比如传统方法、朴素提示或非代理模型。
- 重新运行代理评估的成本很高，因为 API 调用、重复试验和提示敏感性都会改变结果，并增加复现成本。

## 方法
- 论文分析了来自 ICSE 2025/2026、FSE 2025、ASE 2025 和 ISSTA 2025 的 18 篇论文，并提取了常见评估模式：所用基线、消融实验、失败分析、成本分析和可复现性细节。
- 论文建议一个最低报告标准：公开 prompts、temperature 设置和准确的 LLM 版本，以便复现评估。
- 论文还建议公开代理的 Thought-Action-Result 轨迹，或这些轨迹的摘要版本，这样后续工作就能查看代理为什么成功或失败，而不只是看到最终汇总分数。
- 对于较长的轨迹，论文建议用 LLM 摘要做自动分析，分 3 步进行：先总结每次运行，再在同一次运行上比较不同代理，最后跨多次运行汇总重复出现的优点和缺点。
- 一个概念验证案例研究使用了来自漏洞修复检测代理的开放 TAR 跟踪，并比较了基于 Qwen3-235B、Llama-3.3-70B-Instruct 和 Gemma-3-27B 的代理，分析器使用 Kimi K2.5 Instant。

## 结果
- 文献综述结果：分析了 18 篇 agentic SE 论文；其中 11/18 使用了多代理设置。
- 基线结果：只有 1/18 篇论文与现有的 agentic AI 基线比较；13/18 篇包含消融研究。
- 可复现性结果：所有被审查的论文都写明了 LLM 系列，但只有少数论文给出精确版本标识，例如 GPT-3.5-0125。
- 成本/报告结果：一些论文报告了 API 或 token 成本，有些还做了 temperature 敏感性分析或重复试验，但本文没有给出覆盖全部 18 项研究的完整量化基准表。
- 案例研究结果：概念验证比较了 10 个随机抽样的、失败的 Qwen3-235B 运行，以及这些相同案例上对应的 Gemma-3-27B 和 Llama-3.3-70B-Instruct 运行；更强的代理解决了 Qwen 失败的一些案例。
- 论文没有声称取得了新的任务最优分数。它的主要具体主张是方法论上的：自动化 TAR 分析可以从共享轨迹中恢复可解释的代理差异，例如验证行为、主要失败模式和各模型的优势。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01437v1](http://arxiv.org/abs/2604.01437v1)
