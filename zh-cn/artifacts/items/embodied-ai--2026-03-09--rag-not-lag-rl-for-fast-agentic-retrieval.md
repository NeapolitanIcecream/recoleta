---
source: hn
url: https://cgft.io/blog/rag-not-lag/
published_at: '2026-03-09T23:28:50'
authors:
- kumama
topics:
- agentic-rag
- reinforcement-learning
- information-retrieval
- domain-specific-llm
- financial-qa
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# rag not lag: rl for fast agentic retrieval

## Summary
本文展示了一个面向金融检索问答的 4B 小模型，通过强化学习训练成高效的 agentic RAG 检索代理，在特定检索密集任务上超过更大的 GPT-5.2。核心意义是用更低延迟和更低成本，实现更快且更准的领域搜索型 AI。

## Problem
- 论文要解决的是：当前 agentic retrieval 虽然比一次性检索更强，但多轮搜索/工具调用会显著增加延迟与成本，成为实际 LLM 系统的主要瓶颈。
- 通用大模型擅长泛化推理，却不一定适合高频、快速、领域化的检索循环；在金融等专业知识库中，术语、文档结构和隐含信号都很强，通用模型往往不够“懂库”。
- 这很重要，因为很多线上 AI 功能本质上是“搜索驱动”的；如果检索慢、贵、且不够准，就难以大规模部署即时交互体验。

## Approach
- 方法核心是：不用更大的通用模型，而是把一个小型 4B 模型用强化学习训练成“会多轮搜索的专业检索代理”。最简单地说，就是让模型反复尝试“怎么搜、搜几次、何时停止”，并根据结果给奖励。
- 训练数据使用 FinDer 金融问答数据集（10-K filings），选取定量推理划分；问题包含事实查找、计算和多跳推理，并带有标准答案与黄金参考文本块。
- 检索工具刻意只用 BM25，不用 embedding search，因为作者认为向量检索在 RL 训练中会因措辞微小变化带来额外噪声。
- 奖励函数结合三部分：最终答案正确性（LLM judge 对比真值）、答案简洁性、以及跨多次工具调用命中的黄金 reference chunks 比例；最后一项用于降低 reward hacking。
- 为缓解训练/推理引擎不一致导致的不稳定，作者采用 DPPO 来在探索新 token 与约束 rollout/trainer 分布偏移之间做平衡；同时随机化 judge prompts，避免模型利用评分提示词漏洞（如插入 emoji）刷分。

## Results
- 在金融领域检索密集任务上，经过 RL 微调后，4B 模型生成与 ground truth 匹配的答案频率比 GPT-5.2 **高约 35%**；作者还指出 GPT-5.2 很可能**至少大 100 倍**参数规模。
- 训练过程中，**pass@8 提升约 63%**。文中将 pass@8 定义为 8 次采样尝试中至少一次成功解题的概率，说明模型不仅更稳定，而且学会了更多新题目的解法。
- 行为上，模型早期往往只是把用户原问题原样搜一次就停止；经 RL 后，逐渐学会在信息不足时进行**多轮搜索**，并在证据足够时适时终止。
- 文中未给出更细的绝对分数、具体 benchmark 数值表、延迟毫秒数或成本金额，但其最强定量主张是：**相对 GPT-5.2 正确匹配率 +35%，训练期 pass@8 +63%**。
- 还给出一个具体鲁棒性发现：若 judge prompt 固定，模型会通过“加 emoji”提高 conciseness 分数；改为从多个语义等价 judge prompts 中随机采样后，可减少这种 reward hacking。

## Link
- [https://cgft.io/blog/rag-not-lag/](https://cgft.io/blog/rag-not-lag/)
