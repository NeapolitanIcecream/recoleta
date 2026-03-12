---
source: arxiv
url: http://arxiv.org/abs/2603.03394v1
published_at: '2026-03-03T11:01:56'
authors:
- Muhammad Waseem
- Md Aidul Islam
- Md Nasir Uddin Shuvo
- Md Mahade Hasan
- Kai-Kristian Kemell
- Jussi Rasku
- Mika Saari
- Vilma Saari
- Roope Pajasmaa
- Markku Oivo
- Pekka Abrahamsson
topics:
- ai-governance
- sandbox-platform
- multi-tenant-architecture
- audit-logging
- access-control
relevance_score: 0.06
run_id: materialize-outputs
---

# Engineering a Governance-Aware AI Sandbox: Design, Implementation, and Lessons Learned

## Summary
本文提出并实现了一个面向产学协作的“治理感知”多租户 AI Sandbox，用于在受控权限、组织隔离和可追踪流程下开展 AI 试验。其核心贡献是把审批、访问控制和审计日志直接嵌入实验平台架构中，以提升评估证据的可复用性与可比性。

## Problem
- AI 技术早期评估常常是**非正式且分散的**，不同团队、工具和用例之间结果难以比较，证据也难以复用。
- 在真实组织环境中，AI 试验还受到**治理、合规、数据管理、人类监督**等约束；如果这些约束没有被系统化纳入平台，组织很难基于可靠证据决定是否采用 AI。
- 现有关于 sandbox 的研究更多讨论**监管或制度层面**，但缺少如何真正构建一个**多租户、治理感知、可操作化**实验平台的工程指导。

## Approach
- 作者基于芬兰 SW4E 生态，与 3 家工业伙伴通过**半结构化访谈 + 双周迭代评审**收集并验证需求，再逐步形成参考架构与 MVP 原型。
- 核心机制是一个**分层架构**：前端多租户工作区 + 后端控制平面 + 独立 AI 执行层 + 数据存储层；其中控制平面统一负责身份、审批、协作、实验编排与策略执行。
- 平台把治理直接做成系统机制：使用 **JWT + RBAC + ABAC**、组织/项目级隔离、审批流、审计日志，把“谁能访问什么、谁批准了什么、做了哪些实验”都记录为持久化治理工件。
- AI 能力通过**后端托管适配器**接入外部服务（如 Hugging Face、OpenAI），避免前端直接接触密钥或外部接口；硬件资源则通过**配额与审批工作流**治理，而非直接裸连集群。
- 原型实现采用 Next.js + Express + SQLite，并支持容器化部署到 Kubernetes/OpenShift 类环境，重点验证**治理正确性与架构可行性**，而非大规模性能。

## Results
- 论文的主要产出是**参考架构 + 开源原型 + 部署经验总结**；文中给出了开源仓库与在线演示，但**没有报告标准基准数据集上的定量性能结果**。
- 实证过程包含 **3 个阶段**（需求收集、架构设计、原型开发与迭代验证），并与 **3 家工业伙伴**开展访谈；每次访谈约 **1 小时**，且以**每两周一次**的结构化评审推进迭代。
- 测试覆盖的核心工作流包括：用户注册、审批处理、基于角色的仪表板访问、项目创建、AI 服务调用、硬件申请提交；作者声称这些流程中**API 边界上的治理约束均被正确执行**。
- 访问控制测试通过尝试**越权管理操作、跨组织访问、无权限服务调用**来验证；论文声称中间件级 **RBAC/权限检查成功拒绝了无效请求**，且审计日志能记录安全相关事件，但未给出拒绝率、延迟或覆盖率数字。
- 自动化测试方面，作者明确说明**没有完整的主前后端自动化测试套件**；仅有轻量级 CI 用于构建一致性与容器完整性检查，这表明当前成果更偏向**工程原型验证**而非成熟产品评测。
- 最强的具体主张是：该平台能在多租户环境中实现**受治理的 onboarding、项目协作、受控 AI 服务访问、可追踪实验记录**，并将审批决策与审计日志沉淀为可跨项目、跨利益相关方复用的评估证据。

## Link
- [http://arxiv.org/abs/2603.03394v1](http://arxiv.org/abs/2603.03394v1)
