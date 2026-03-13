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
- privacy-governance
- access-control
- auditability
- secure-infrastructure
relevance_score: 0.23
run_id: materialize-outputs
---

# Building Privacy-and-Security-Focused Federated Learning Infrastructure for Global Multi-Centre Healthcare Research

## Summary
本文提出 FLA^3，一个面向医疗联邦学习的“治理感知”基础设施，把认证、授权、审计（AAA）直接嵌入联邦学习编排层，以满足跨机构、跨司法辖区的隐私与合规要求。它的重点不是提升新模型精度，而是让真实世界医疗联邦学习在严格治理约束下可部署、可审计、且仍保持接近集中式训练的效能。

## Problem
- 医疗多中心研究需要跨机构联合训练，但原始数据跨境共享常受 GDPR、HIPAA 等法规限制，导致很多模型无法使用足够大且多样的数据训练。
- 现有联邦学习框架多停留在原型验证，通常假设参与方可信，缺少运行时可执行的治理机制：**谁能加入、能参加哪个研究、在什么时间窗口内、做哪些操作、如何留痕追责**。
- 在医疗场景里，即使数据不出院，若在审批过期后或在未获批准的研究中继续计算，依然构成未授权处理，可能使整个研究不合规甚至无效，因此这个问题很重要。

## Approach
- 提出 **FLA^3 (FL with AAA)**：在联邦学习编排层加入治理控制，而不只依赖数据本地化或加密技术。
- 用 **XACML 兼容的属性基访问控制（ABAC）** 做运行时策略判定，强制执行 5 类治理要求：机构身份认证、研究范围授权、基于角色的最小权限、时间有效期、审计追踪。
- 采用 **fail-closed** 机制：若策略评估失败、上下文属性缺失或审批过期，则默认拒绝参与或执行，防止“默认放行”。
- 引入 **study-scoped federation**：每个研究是独立联邦，拥有自己的参与方集合、授权策略和有效期，可在同一平台并发运行多个研究。
- 结合 **加密签名审计日志** 与 Flower 扩展实现；并展示其可与个性化联邦学习方法 **FedMAP** 配合，在非 IID 医疗数据下维持效能。

## Results
- **真实部署可行性**：平台已部署到 **5 个 BloodCounts! 联盟机构**，覆盖 **4 个国家**（英国、荷兰、印度、冈比亚）；作者称在真实网络与监管约束下，治理策略能正确执行。
- **临床数据规模**：在 INTERVAL 研究中进行了模拟联邦实验，使用 **54,446 个样本、35,315 名受试者、25 个中心** 的全血细胞计数数据。
- **性能主张**：作者称在严格治理约束下，FLA^3 的预测性能与**集中式训练相当（comparable to centralised training）**，并且**显著优于单中心/单独训练（significantly improves compared with individual training）**。
- **治理兼容性主张**：作者明确声称，加入策略驱动治理后，**不会降低与 FedMAP 集成时的个性化联邦学习性能**。
- **文中未给出具体精度数值**：摘录没有提供 AUROC、AUPRC、accuracy 等明确指标，也没有给出与具体基线的百分点差异，因此无法进一步量化比较。
- **额外证据**：作者还引用其系统性综述指出，医疗 FL 中只有约 **5%** 涉及真实部署，且其先前回顾中 **87/89（98%）** 的方法缺少节点认证、**0 篇**提供可同行评审的开放治理实现，以此强调该工作的现实突破点在“可执行治理基础设施”。

## Link
- [http://arxiv.org/abs/2603.10063v1](http://arxiv.org/abs/2603.10063v1)
