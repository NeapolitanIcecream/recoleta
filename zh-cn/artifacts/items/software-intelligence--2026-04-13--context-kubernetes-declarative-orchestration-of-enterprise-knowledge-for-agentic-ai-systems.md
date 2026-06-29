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
本文提出 Context Kubernetes，一种面向 AI 代理使用的企业知识编排层，风格类似 Kubernetes。它关注治理、权限、新鲜度和可审计性，而不是代理本身的推理。

## 问题
- 企业可以让单个 AI 代理访问本地文件，但当多个代理扩展到整个组织时，就会出现协调和治理问题：哪些知识能送到哪个代理，基于什么权限，保持多新鲜，以及留下什么审计记录。
- 现有代理平台的治理层要么很弱，要么依赖厂商；面向人的标准 RBAC 也不足以完全覆盖代表用户行动的自主代理。
- 这很重要，因为陈旧、权限过高或路由不当的上下文会导致数据泄露、错误操作和企业部署失败。

## 方法
- 论文把组织知识当作可调度资源，并借用了 Kubernetes 的两个思路：用 YAML 清单声明期望状态，以及用 reconciliation loop 将真实状态与声明状态比对并修正偏移。
- 它定义了六个主要抽象：context units、domains、stores、endpoints、用于连接器的 Context Runtime Interface，以及按域划分的 context operators。
- 代理按意图请求知识，而不是按来源位置请求。路由器把请求解析到允许的数据源，按权限过滤，检查新鲜度，并将响应控制在 token 预算内。
- 关键治理机制是三层权限模型，代理权限必须严格小于人类用户权限。高风险操作需要带有独立因素的带外批准。
- 原型包括 Context Router、Permission Engine、连接器、reconciliation loop、审计日志、FastAPI 服务和 92 个自动化测试。

## 结果
- 评估包含 8 个实验：5 个正确性实验和 3 个价值实验。
- 在基于合成种子数据的 200 个基准查询上，论文比较了四种治理配置：无治理 RAG、ACL 过滤检索、RBAC 感知路由，以及完整架构。论文称每一层新增的能力都不同。
- 在 5 种攻击场景中，平坦权限拦截 0/5 次攻击，基础 RBAC 拦截 4/5 次，三层模型拦截 5/5 次。
- 没有新鲜度监控时，过期和已删除内容会被静默返回。有 reconciliation 时，过期内容在 1 ms 内被检测出来。
- 正确性测试报告了 0 次未授权上下文交付和 0 次权限不变量违反。
- TLA+ 模型检查探索了 460 万个可达状态，没有发现安全违规。论文还称，所调查的企业平台中，没有一个实现了其带外批准隔离设计。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11623v3](http://arxiv.org/abs/2604.11623v3)
