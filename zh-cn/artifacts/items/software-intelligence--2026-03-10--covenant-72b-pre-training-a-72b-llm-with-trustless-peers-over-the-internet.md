---
source: hn
url: https://twitter.com/tplr_ai/status/2031388295972929720
published_at: '2026-03-10T22:51:03'
authors:
- rzk
topics:
- distributed-training
- llm-pretraining
- trustless-compute
- decentralized-ai
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Covenant-72B: Pre-Training a 72B LLM with Trustless Peers Over-the-Internet

## Summary
该条目指向一则 X/Twitter 帖子，但当前提供的正文只有“需要启用 JavaScript”的占位信息，几乎没有论文内容可供分析。基于标题，论文似乎讨论通过互联网中的无信任对等节点来预训练一个 72B 大语言模型，但具体方法与结果无法从给定文本中确认。

## Problem
- 试图解决如何在**不依赖中心化可信集群**的情况下，利用互联网上的分布式、无信任 peers 共同完成超大模型（72B）预训练。
- 这一问题之所以重要，是因为大模型训练通常需要昂贵、集中式基础设施；若能用开放互联网协作训练，可能显著降低进入门槛并提升去中心化程度。
- 但给定文本未提供论文正文，因此无法确认其具体研究问题定义、威胁模型或系统约束。

## Approach
- 从标题推测，核心机制是让多个**互联网上的无信任对等节点**共同参与 72B LLM 的预训练，而不要求节点之间彼此可信。
- 最简单理解：把原本在单一受控集群里做的训练任务，拆分并协调到很多互联网参与方上，同时需要某种机制来处理不可靠或潜在恶意节点。
- 由于提供内容缺失，无法确认其具体采用了哪些技术，例如参数同步、梯度验证、容错、激励设计、带宽优化或安全协议。
- 也无法确认“Covenant-72B”是从零训练、继续预训练，还是其他训练范式。

## Results
- 给定文本**没有任何可核实的定量结果**，因此无法提取指标、数据集、基线或对比数值。
- 从标题能确认的最强具体声明只有：作者声称完成了一个名为 **Covenant-72B** 的 **72B 参数 LLM** 预训练工作，并且训练设置涉及“**trustless peers over-the-Internet**”。
- 无法确认其训练吞吐、收敛质量、成本、稳定性、安全性，或相对传统集中式训练的提升幅度。

## Link
- [https://twitter.com/tplr_ai/status/2031388295972929720](https://twitter.com/tplr_ai/status/2031388295972929720)
