---
source: arxiv
url: http://arxiv.org/abs/2604.11623v3
published_at: '2026-04-13T15:35:55'
authors:
- Charafeddine Mouzouni
topics:
- agentic-ai
- context-orchestration
- enterprise-governance
- access-control
- rag-systems
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# Context Kubernetes: Declarative Orchestration of Enterprise Knowledge for Agentic AI Systems

## Summary
## 摘要
这篇论文提出了 Context Kubernetes，一个面向 AI 代理所用企业知识的类 Kubernetes 编排层。它关注治理、权限、新鲜度和可审计性，而不是代理推理本身。

## 问题
- 企业可以让单个 AI 代理访问本地文件，但当规模扩大到组织内多个代理时，就会出现协调和治理问题：哪些知识会到达哪个代理、在什么权限下、具有怎样的新鲜度，以及留下什么样的审计记录。
- 现有代理平台的治理层较弱，或者依赖特定厂商；而面向人类用户的标准 RBAC 也无法完全处理代表用户自主行动的代理。
- 这很重要，因为过时、权限过宽或路由不当的上下文会导致数据泄露、错误操作和企业部署失败。

## 方法
- 论文把组织知识视为一种可调度资源，并借用了 Kubernetes 的两个思想：在 YAML 清单中声明期望状态，以及使用 reconciliation loop 对照声明状态检查实际状态并修复漂移。
- 它定义了六个主要抽象：上下文单元、域、存储、端点、用于连接器的 Context Runtime Interface，以及面向特定领域的上下文操作器。
- 代理按意图而不是按源位置请求知识。路由器将请求解析到允许的来源，按权限过滤，检查新鲜度，并将响应控制在 token 预算内。
- 核心治理机制是三层权限模型，其中代理权限必须严格小于人类用户的权限。高风险操作需要带有独立因子的带外批准。
- 原型包括 Context Router、Permission Engine、连接器、reconciliation loop、审计日志、FastAPI 服务，以及 92 个自动化测试。

## 结果
- 评估包括 8 个实验：5 个正确性实验和 3 个价值实验。
- 在基于合成种子数据的 200 个基准查询上，论文比较了四种治理设置：无治理 RAG、ACL 过滤检索、RBAC 感知路由，以及完整架构。论文称每一层新增能力都不同。
- 在 5 个攻击场景中，扁平权限阻止了 0/5 次攻击，基础 RBAC 阻止了 4/5 次，三层模型阻止了 5/5 次。
- 没有新鲜度监控时，过时和已删除内容会被静默返回。使用 reconciliation 后，系统可在 1 ms 以内检测到过时内容。
- 正确性测试报告显示，未发生未授权上下文交付，也未出现权限不变量违反。
- TLA+ 模型检查探索了 460 万个可达状态，发现 0 个安全性违反。论文还称，在其调研的企业平台中，没有平台实现其带外批准隔离设计。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11623v3](http://arxiv.org/abs/2604.11623v3)
