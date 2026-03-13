---
source: arxiv
url: http://arxiv.org/abs/2603.10063v1
published_at: '2026-03-09T22:13:00'
authors:
- Fan Zhang
- Daniel Kreuter
- Javier Fernandez-Marques
- BloodCounts Consortium
- Gregory Verghese
- Bernard Butler
- Nicholas Lane
- Suthesh Sivapalaratnam
- Joseph Taylor
- Norbert C. J. de Wit
- Nicholas S. Gleadall
- "Carola-Bibiane Sch\xF6nlieb"
- Michael Roberts
topics:
- federated-learning
- healthcare-ai
- data-governance
- access-control
- privacy-preserving-ml
relevance_score: 0.03
run_id: materialize-outputs
---

# Building Privacy-and-Security-Focused Federated Learning Infrastructure for Global Multi-Centre Healthcare Research

## Summary
FLA^3 是一个面向医疗多中心联邦学习的治理增强型基础设施，在“数据不出院”的前提下，把认证、授权和审计作为运行时强制执行的一等公民。论文重点证明：在跨国、受监管的真实医疗环境中，联邦学习不仅要保护数据，还必须可执行地保证谁能参与、何时参与、为何参与。

## Problem
- 医疗多机构研究需要更大、更异构的数据，但跨境共享患者数据受到 GDPR、HIPAA 等法规严格限制，导致很多有价值的 AI 模型难以训练。
- 现有联邦学习框架大多只解决“数据留在本地”，却没有在运行时强制执行治理要求，如**认证、基于研究项目的授权、时效控制、审计留痕**，因此在真实临床部署中可能依然构成未授权处理。
- 这很重要，因为即使原始数据从未离开医院，只要过期审批节点继续参与、或未授权机构加入训练，整个研究都可能合规失效并损害患者与机构信任。

## Approach
- 提出 **FLA^3 (FL with AAA)**：在联邦学习编排层直接集成 **authentication, authorisation, accounting**，而不是只依赖组织流程或静态配置。
- 采用 **XACML 兼容的属性基访问控制（ABAC）**：系统会在每个关键联邦学习生命周期节点检查机构身份、研究 ID、角色、审批状态和时间有效期；如果策略求值失败或上下文缺失，则默认拒绝（fail-closed）。
- 设计 **study-scoped federation**：每个研究被视为独立联邦，拥有自己的参与机构集合、策略和时间窗口，避免“某研究获批就可访问所有研究”。
- 加入 **加密审计/accounting**：对安全相关操作生成带密码学签名的审计记录，使参与行为可追责、可审计、可归因。
- 在实现上基于 **Flower** 扩展，并与个性化联邦学习方法 **FedMAP** 兼容，以应对医疗数据的非 IID 异质性，同时适配医院常见的仅出站网络环境。

## Results
- **真实部署可行性**：平台已部署到 **BloodCounts! Consortium 的 5 家机构、4 个国家**（英国、荷兰、印度、冈比亚），论文称在现实网络限制和监管约束下，治理策略能够正确执行。
- **临床效用评估**：在 **INTERVAL** 数据上进行模拟联邦实验，覆盖 **54,446 个样本、35,315 名受试者、25 个中心**。
- 论文核心性能声明是：**FLA^3 的预测性能与集中式训练相当**，同时严格执行治理约束。
- 还声称：在与 **FedMAP** 集成后，治理机制**不会降低个性化联邦学习性能**，且联邦训练**显著优于单机构独立训练**。
- **未提供明确数值指标**：摘录中没有给出 AUROC、准确率、误差值或相对提升百分比，也未列出与具体基线的详细数值比较；最强的定量证据主要是部署规模（5 家机构/4 国）和数据规模（54,446 样本/25 中心）。

## Link
- [http://arxiv.org/abs/2603.10063v1](http://arxiv.org/abs/2603.10063v1)
