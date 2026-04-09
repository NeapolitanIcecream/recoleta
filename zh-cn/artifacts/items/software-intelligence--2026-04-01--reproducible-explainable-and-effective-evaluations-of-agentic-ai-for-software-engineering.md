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
这篇论文研究软件工程中的 agentic AI 系统是如何被评估的，并指出当前做法难以复现，也难以解释。论文提出了具体的报告规则，以及一种基于轨迹的评估方法，核心是发布和分析 Thought-Action-Result (TAR) 日志。

## 问题
- 软件工程智能体的评估通常依赖黑盒 LLM 行为、随机输出和不完整的报告，这使结果难以复现和比较。
- 在作者对 18 篇近期 SE 论文的审查中，只有 1 篇论文与相关的现有最强 agentic 基线进行了比较，因此许多声称的提升是相对于更弱的基线得出的，例如传统方法、朴素提示或非智能体模型。
- 重新运行智能体评估成本很高，因为 API 调用、重复试验和提示敏感性都会改变结果并提高复现实验的成本。

## 方法
- 论文分析了来自 ICSE 2025/2026、FSE 2025、ASE 2025 和 ISSTA 2025 的 18 篇论文，并提取出常见的评估模式：所用基线、消融实验、失败分析、成本分析和可复现性细节。
- 论文建议采用最低报告标准：发布 prompts、temperature 设置和精确的 LLM 版本，以便让评估可复现。
- 论文还建议，文章应发布智能体的 Thought-Action-Result 轨迹，或其摘要版本，这样后续工作就能检查智能体成功或失败的原因，而不是只看到最终汇总分数。
- 对于较长轨迹，论文建议用 LLM 摘要做自动分析，分 3 步进行：总结每次运行、比较同一次运行中的不同智能体，然后汇总多次运行中重复出现的优点和缺点。
- 一个概念验证案例研究使用了来自漏洞修复检测智能体的开放 TAR 轨迹，并比较了基于 Qwen3-235B、Llama-3.3-70B-Instruct 和 Gemma-3-27B 构建的智能体，分析器使用 Kimi K2.5 Instant。

## 结果
- 文献回顾结果：共分析了 18 篇 agentic SE 论文；其中 11/18 使用多智能体设置。
- 基线结果：只有 1/18 的论文与现有 agentic AI 基线进行了比较；13/18 包含消融研究。
- 可复现性结果：所有审查论文都给出了 LLM 家族名称，但只有少数论文提供了精确的版本标识符，例如 GPT-3.5-0125。
- 成本/报告结果：一些论文报告了 API 或 token 成本，也有一些做了 temperature 敏感性测试或重复试验，但这篇论文没有给出覆盖全部 18 项研究的完整量化基准表。
- 案例研究结果：该概念验证比较了 10 个随机抽样的失败 Qwen3-235B 运行，并与相同案例上的 Gemma-3-27B 和 Llama-3.3-70B-Instruct 对应运行进行对比；更强的智能体解决了部分 Qwen 失败的案例。
- 论文没有声称得到新的最先进任务分数。它最具体的主张是方法层面的：自动化 TAR 分析可以从共享轨迹中恢复可解释的智能体差异，例如验证行为、主要失败模式以及各模型的优势。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01437v1](http://arxiv.org/abs/2604.01437v1)
