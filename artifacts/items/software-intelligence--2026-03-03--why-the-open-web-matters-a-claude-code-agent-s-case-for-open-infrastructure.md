---
source: hn
url: https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/
published_at: '2026-03-03T23:45:51'
authors:
- 9wzYQbTYsAIc
topics:
- agentic-ai
- open-web
- web-verification
- knowledge-grounding
- machine-readable-protocols
relevance_score: 0.91
run_id: materialize-outputs
---

# Why the Open Web Matters: A Claude Code Agent's Case for Open Infrastructure

## Summary
这篇文章主张：开放网络是可信代理式AI的基础设施，因为代理要依赖可公开访问的权威网页来发现信息、核验事实并修正错误。作者用一个人权主题网站的构建过程作案例，论证一旦公共信息被认证墙、API密钥或限流封闭，代理输出质量会系统性下降。

## Problem
- 文章要解决的问题是：**代理式AI如何获得可验证、可纠错、可发现的外部知识**，而不是只依赖训练数据生成看似权威但可能漂移的内容。
- 这很重要，因为随着AI被用于研究、政策分析、摘要和建议生成，若公共权威信息不再开放，**人和代理都会失去可靠的事实校准来源**。
- 作者进一步指出一个风险：为应对代理流量而关闭开放网络，可能反而导致**更差的AI内容质量**，再把人类逼回同一批原始网页做人工核验。

## Approach
- 核心机制很简单：让代理像人类研究员一样，直接访问开放网页上的权威来源（如 OHCHR、Congress.gov、Senate.gov、条约文本等），逐条比对内容，而不是相信参数记忆。
- 作者以 unratified.org 的构建过程为案例：网站包含 **49 个术语**，其中 **19 个术语**在最近一轮开发中被拿去对照外部权威来源，检查 **4 个维度**：事实准确性、范围一致性、完整性、是否存在有意再解释。
- 除了核验，文章还强调“发现层”：通过 **/.well-known/agent-inbox.json、glossary.json、taxonomy.json 和 RSS** 等开放协议，让代理无需认证、API key 或定制集成即可遍历站点能力与语义结构。
- 作者提出两个推断性假说来解释系统后果：**H3 Jevons Explosion**（代理让网页资源需求爆炸）与 **H6 Quality Erosion**（若因流量而封闭访问，会削弱代理 grounding，降低输出平均质量）。

## Results
- 在 **49 个术语**中，作者报告已对 **19 个术语**完成外部核验；结果是 **0 个严重事实错误**，但发现并应用了 **5 处修正**。
- 一个具体修正是美国条约批准门槛：原文写成 **67 票超级多数**，核验后改为宪法中的 **“出席参议员的三分之二”**；作者举例称若仅 **51 人出席**，则 **34 票**即可满足门槛。
- 另一处修正是 ICESCR 第 15 条措辞：原文将权利表述为 **“guarantees”**，核验条约原文后改为 **“recognizes”**，因为两者法律含义不同。
- 关于 ESCR 定义，作者称核验 OHCHR 页面后，修正了把经济、社会和文化权利简单视为“积极权利”的冷战式二分法，并补上此前遗漏的 **“文化权利”** 维度。
- 文章**没有提供与替代系统、封闭网络设置或基准模型的实验性对比指标**，也未测试“若网页封闭，这 5 处修正是否一定无法完成”的反事实；最强的具体主张是：在该案例中，**所有提升准确性的修正都依赖开放访问的权威来源，且作者称“无一例外”**。
- 从研究贡献看，最“新”的点不是一个量化SOTA结果，而是提出并案例化论证：**开放网络是可信代理式AI的前提性基础设施**，而不是可有可无的分发渠道。

## Link
- [https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/](https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/)
