---
source: arxiv
url: http://arxiv.org/abs/2603.11721v1
published_at: '2026-03-12T09:28:25'
authors:
- Wenxian Yang
- Hanzheng Qiu
- Bangqun Zhang
- Chengquan Li
- Zhiyong Huang
- Xiaobin Feng
- Rongshan Yu
- Jiahong Dong
topics:
- llm-agents
- clinical-workflows
- agentic-operating-system
- multi-agent-systems
- long-term-memory
relevance_score: 0.88
run_id: materialize-outputs
---

# When OpenClaw Meets Hospital: Toward an Agentic Operating System for Dynamic Clinical Workflows

## Summary
本文提出一个面向医院动态临床工作流的“医院代理操作系统”架构，基于 OpenClaw 式技能库，但用操作系统级隔离、文档驱动多代理协作和分层长期记忆来适配医疗场景。核心目标是在保证安全、可审计和可扩展的前提下，让 LLM 代理能处理医院中大量非预编程、长尾化的临床任务。

## Problem
- 现有通用 LLM agent 框架通常默认**宽权限执行**（文件系统、网络、代码执行），这与医院的隐私、合规和审计要求根本冲突。
- 现有基于向量检索的记忆/RAG 会把病历切碎成无上下文片段，难以保留**纵向、时序化、文档结构化**的临床信息。
- 医院工作流天然是**多角色、以文档为中心**的协作系统，而非单一对话界面；传统 HIS/EHR/CDSS 又多为固定流程，难覆盖临床长尾需求。

## Approach
- 提出一个受 Linux 多用户系统启发的**受限执行环境**：每个角色代理（患者、医生、护士等）运行在独立隔离命名空间中，禁止直接文件访问、外网访问和动态代码加载，只能调用预审计技能。
- 采用**医疗技能库**作为唯一可执行动作单元：技能具备类型化接口，只能通过预定义、窄权限连接器访问医院内部资源，从而把安全约束下沉到运行时和系统层。
- 设计**文档中心的多代理协作机制**：代理之间不直接通信，而是通过共享临床文档的写入/变更事件进行协调；事件流记录版本号、写入者角色和页面引用，形成可追溯审计链。
- 提出**页索引记忆架构（page-indexed memory）**：把患者长期记录组织成树状文档层级，每个内部节点维护 manifest 文件；查询时代理逐层读取 manifest 并选择相关子树，替代向量相似度检索。
- 为动态更新提供**局部增量维护**：单次文档变更只需更新受影响节点及必要祖先节点的 manifest，论文给出维护复杂度为每次变更 `O(d)` 或最多 `O(L)` 次增量 LLM 调用。

## Results
- 这篇论文是**架构/系统设计提案**，在给定摘录中**没有报告实验指标、基准测试或临床部署结果**，因此没有可填写的准确性能数字（如准确率、AUROC、吞吐、延迟）。
- 论文最强的具体技术主张是：页索引记忆**完全不依赖向量嵌入**，因此**无需 embedding 计算、无需离线建索引、无需重建索引**即可适配实时变更的病历文档集合。
- 在复杂度方面，作者明确声称 manifest 维护成本为**每次变更 `O(d)`**（`d` 为节点深度），祖先传播下最坏为**`O(L)` 次增量 LLM 调用**，而不是对整个语料批量重处理。
- 在系统约束方面，作者声称代理动作被限制为**两类**：调用预审计医疗技能、读写共享临床文档；跨代理协调通过**单一追加式 mutation event 流**完成，从而提升安全性、透明性和审计性。
- 在能力层面，作者声称该架构可支持**按需组合技能**来处理固定工作流之外的临床长尾需求，例如跨多年实验室趋势、罕见药物相互作用、跨 care episode 的个体化分析等，但摘录中未提供量化对比。

## Link
- [http://arxiv.org/abs/2603.11721v1](http://arxiv.org/abs/2603.11721v1)
