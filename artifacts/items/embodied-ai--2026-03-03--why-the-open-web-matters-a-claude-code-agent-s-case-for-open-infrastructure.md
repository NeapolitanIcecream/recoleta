---
source: hn
url: https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/
published_at: '2026-03-03T23:45:51'
authors:
- 9wzYQbTYsAIc
topics:
- open-web
- agentic-verification
- web-infrastructure
- information-access
- research-agents
relevance_score: 0.23
run_id: materialize-outputs
---

# Why the Open Web Matters: A Claude Code Agent's Case for Open Infrastructure

## Summary
这是一篇关于开放网络基础设施对“可验证的智能体研究”重要性的案例性论证，而不是传统实验论文。作者通过一个由智能体构建的人权/法律分析站点说明：开放、可抓取、免认证的公共信息源，是提升智能体输出可信度的关键前提。

## Problem
- 文章要解决的问题是：**如果开放网络被认证墙、API 门槛、限流和封闭协议取代，智能体还能否可靠地检索、核验并纠正事实？** 这很重要，因为越来越多人会依赖智能体生成的研究、政策摘要与分析。
- 作者认为，仅靠模型训练数据会产生**事实漂移和无法发现的错误**；没有实时、权威、开放的外部来源，智能体会生成看似权威但缺乏依据的内容。
- 文章还提出一个更广泛的风险：为应对 agent 流量而收紧访问，可能反而降低 agent 输出质量，最终伤害依赖这些输出的人类用户。

## Approach
- 核心方法很简单：作者用一个实际项目做案例，展示智能体如何像人类研究员一样，直接访问开放网页上的权威来源（如 OHCHR、Congress.gov、Senate.gov 等）来**逐条核验**内容。
- 在一个包含 **49 个术语、8 个类别** 的 glossary 中，作者选取其中 **19 个术语**，按四个维度做外部验证：**事实准确性、范围一致性、完整性、是否存在有意重释**。
- 作者报告了若干具体纠错案例：例如把“67 票”改为“出席参议员的三分之二”，把 ICESCR 中 “guarantees” 改为更准确的 “recognizes”，以及修正 ESCR 定义中过度简化的“积极/消极权利”二分法。
- 除了验证，文章还强调“发现层（discovery layer）”：通过 **RSS、JSON-LD、SKOS、/.well-known/** 等开放协议，让智能体无需 OAuth、API key 或逐供应商谈判就能发现和组合资源。
- 机制上的主张是：**开放网页 = 智能体的外部记忆与校验层；封闭网页 = 更高摩擦、更少校验、更多无根据输出。**

## Results
- 对 **19/49** 个术语进行外部验证后，作者报告：**0 个严重事实错误，应用了 5 处修正**；这些修正均来自开放的权威来源核验。
- 具体修正包括：美国条约批准门槛从笼统的 **67 票** 修正为宪法规定的 **“出席参议员的三分之二”**；在最低法定人数 **51 人** 出席时，**34 票** 即可满足要求。
- 另一个修正是 ICESCR Article 15(1)(b) 的措辞：从“**guarantees**”改为“**recognizes**”，作者强调两者法律含义不同。
- 术语体系规模上，项目包含 **49 个术语、8 个类别**；本轮仅验证 **19 个术语**，说明证据仍是有限规模的案例研究，而非大规模对照实验。
- 文中没有提供传统机器学习基准结果，如**accuracy/F1、数据集排行榜、与闭源 API 或离线模型的直接对比**；也**没有测试“封闭网络场景是否一定无法完成同样修正”**。最强主张是：在该案例中，**每一次提升准确性的纠错都依赖开放访问的权威来源，无一例外**。

## Link
- [https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/](https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/)
