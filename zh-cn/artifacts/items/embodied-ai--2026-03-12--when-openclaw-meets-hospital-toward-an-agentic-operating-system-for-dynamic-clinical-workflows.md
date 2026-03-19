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
- clinical-ai
- agent-architecture
- long-term-memory
- retrieval-architecture
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# When OpenClaw Meets Hospital: Toward an Agentic Operating System for Dynamic Clinical Workflows

## Summary
本文提出一个面向医院环境的“医院代理式操作系统”架构，把通用LLM Agent改造成受约束、可审计、可长期记忆的临床工作流协调层。核心贡献是将执行隔离、文档驱动多代理协作、页索引记忆和预审计医疗技能库组合起来，以应对医院场景中的安全性与长时上下文问题。

## Problem
- 现有LLM agent框架通常假设开放计算环境，常需要广泛系统权限，这与医院的隐私、安全、审计和合规要求冲突。
- 常见RAG/向量检索会把患者纵向病历切碎成去上下文片段，难以保留时间顺序、因果关系和跨护理阶段的临床语境。
- 医院工作流天然是多角色、以文档为中心、且存在大量“长尾”临床需求；固定预编程的医院IT系统很难覆盖这些临时组合任务。

## Approach
- 提出一个受限执行环境：每个患者/医生/工作人员代理运行在各自隔离命名空间中，只能通过预定义技能接口访问资源，禁止任意文件系统、外网和动态代码执行；安全边界由OS机制而不是prompt约束保证。
- 采用文档中心的多代理协作：代理之间不直接通信，而是通过共享临床文档的写入与变更事件流协同；每次写入都带版本号并形成追加式、可审计的事件轨迹。
- 设计页索引记忆架构：把病历组织成树形文档层级，每个内部节点维护manifest摘要；检索时让LLM逐层阅读manifest并选择下钻分支，而不是做向量相似度检索。
- 引入医疗技能库：把生命体征聚合、用药依从性跟踪、报告生成等能力封装成静态、类型化、预审计模块，代理可按目标动态组合这些技能，处理未被预编程覆盖的临床任务。
- 对记忆维护采用局部更新：文档变更后仅增量更新相关manifest，作者声称维护成本为每次变更`O(d)`或至多`O(L)`级别，而无需全库重建索引或重算embedding。

## Results
- 这是一篇架构/系统设计论文节选，未给出实证实验、基准数据集或定量性能结果，因此**没有可报告的准确率、召回率、效率或临床效果数字**。
- 文中明确给出的复杂度主张包括：manifest维护对单次变更的局部成本为`O(d)`（`d`为树深），并称祖先级增量更新最多需要`O(L)`次LLM调用，无需embedding重计算。
- 作者声称该架构相较传统开放式agent更安全：通过Linux用户隔离、seccomp、AppArmor、auditd/inotify等内核级机制实现最小权限、审计与资源隔离，但未提供量化安全评测。
- 作者声称相较向量RAG更适合临床纵向记录：页索引记忆保留文档层次、时间范围和文档类型，并可在实时病历变更下工作而无需离线图构建或重建索引，但未提供检索效果对比数字。
- 文中通过连续监测、急诊分诊、紧急升级等案例说明系统可支持动态临床工作流与临时任务组合；这些是概念性场景展示，不是基于真实医院部署的量化验证。

## Link
- [http://arxiv.org/abs/2603.11721v1](http://arxiv.org/abs/2603.11721v1)
