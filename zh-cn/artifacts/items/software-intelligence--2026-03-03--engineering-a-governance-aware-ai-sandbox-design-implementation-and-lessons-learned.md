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
- ai-sandbox
- governance-aware-architecture
- multi-tenant-systems
- access-control
- auditability
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Engineering a Governance-Aware AI Sandbox: Design, Implementation, and Lessons Learned

## Summary
本文提出并实现了一个面向产学协作的治理感知型多租户 AI Sandbox，用于在受控条件下开展 AI 试验并沉淀可复用的评估证据。其核心价值在于把访问控制、审批流和审计日志直接做进实验平台架构，而不是事后补救。

## Problem
- AI 技术在真实组织中的早期评估常常是**非正式、分散且不可比**的，导致结果难复用、 adoption 决策证据不足。
- 产学协作场景需要同时满足**快速试验**与**治理约束**：组织隔离、权限控制、合规、数据管理、人类监督、可追踪性。
- 现有关于监管沙盒或 AI 治理的研究更多讨论制度目标，**缺少如何工程化构建一个多租户、治理感知实验平台的实践指南**。

## Approach
- 提出一个**分层参考架构**：多租户前端层 + 后端控制平面 + 独立 AI 执行层 + 数据存储层，并以网关连接控制面与执行面，实现治理逻辑与算力/模型执行隔离。
- 在后端控制平面中把治理做成“默认路径”：通过 **JWT + RBAC + ABAC**、组织/项目级作用域、审批流、审计日志，在请求进入业务逻辑前先做策略执行。
- 以**持久化治理工件**为中心设计系统：用户、角色、组织、项目、服务权限、硬件配额、审批记录、审计记录都被结构化存储，从而让实验上下文与治理决策可追踪、可比较、可复用。
- 通过**需求驱动、迭代验证**方法开发：对 3 家工业伙伴开展约 1 小时半结构化访谈，随后每两周进行一次原型评审，不断修正需求、架构和实现。
- 实现了一个可部署原型：前端基于 Next.js/React，后端基于 Express/Node.js，数据库使用 SQLite，AI 能力通过后端适配 Hugging Face/OpenAI，并包含一个独立的 Python 匿名化微服务。

## Results
- 论文的主要产出是**架构、原型和经验总结**，而不是性能或模型效果 SOTA；文中**没有提供基准数据集上的定量性能指标**，也没有吞吐、时延、准确率等系统性 benchmark 数字。
- 工业研究过程覆盖 **3 家产业伙伴**（Bittium、Q4US、Solita），访谈为**半结构化、每次约 1 小时**，并在开发期间进行**每两周一次**的结构化原型评审。
- 原型声称已验证若干关键治理流程：用户注册、审批处理、基于角色的仪表盘访问、项目创建、AI 服务调用、硬件申请提交流程，以及跨角色/跨组织的未授权访问拦截。
- 测试结果以**定性验证**为主：作者称 middleware 级 RBAC 与权限检查能够拒绝非法请求，审计日志能够记录安全相关事件；但同时明确说明**没有实现完整自动化测试套件**。
- 工程实现上，系统支持 **Kubernetes-compatible** 部署、Docker Compose 本地编排，以及对 Hugging Face/OpenAI 的后端托管接入；硬件资源治理目前是**逻辑模拟**而非真实集群编排。
- 论文最强的“突破性”主张不是数值提升，而是：给出了一个可开源、可运行的**治理感知 AI Sandbox 参考架构与原型**，并明确区分了“技术沙盒”和“EU AI Act 第53条意义上的监管沙盒”。

## Link
- [http://arxiv.org/abs/2603.03394v1](http://arxiv.org/abs/2603.03394v1)
