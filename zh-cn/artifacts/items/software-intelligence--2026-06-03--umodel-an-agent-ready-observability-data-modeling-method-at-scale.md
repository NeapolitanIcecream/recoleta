---
source: arxiv
url: https://arxiv.org/abs/2606.04799v1
published_at: '2026-06-03T12:25:50'
authors:
- Changhua Pei
- Zheyuan Li
- Zexin Wang
- Hang Cui
- Xiaohui Nie
- Qi Zhou
- Fang Situ
- Cheng Zhang
- Xin Zhang
- Xidao Wen
- Gaogang Xie
- Jingjing Li
- Dan Pei
topics:
- aiops
- observability
- root-cause-analysis
- llm-agents
- knowledge-graph
- query-language
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# UModel: An Agent-Ready Observability Data Modeling Method at Scale

## Summary
## 摘要
UModel 将可观测性数据组织成相互连接的对象，让 LLM 代理可以在根因分析中查询遥测、拓扑和运维知识。论文声称在 AIOps 2025 Challenge 数据集上，根因定位提升了 8%，并报告了在阿里云的大规模部署。

## 问题
- 网络系统的 RCA 需要把日志、指标、链路追踪、拓扑和专家知识放在同一视图里；现有可观测性栈把这些数据分散在 Prometheus、Elasticsearch 和追踪系统等不同工具中。
- LLM 代理常常缺少模式语义、单位、查询规则和实体关系，因此在诊断时会发出无效查询，或漏掉因果路径。
- 这个问题很重要，因为超过 40% 的真实工业故障被报告为 zero-shot 故障，依赖历史事件的监督式 RCA 模型在这类故障上可能失效。

## 方法
- UModel 把运维资源转换为对象：服务、Pod、主机、指标、日志、链路追踪、事件、运行手册和工具。
- 它用语义图连接这些对象，使用 EntitySet、DataSet、EntitySetLink 和 DataLink 连接拓扑、遥测和知识。
- U-SPL 为代理提供一种管道式查询语言，用于模式查找、实体搜索和图遍历，替代分开的 PromQL、SQL、日志和追踪查询。
- USearch 通过关键词搜索、过滤、模糊匹配、排序和 top-k 控制，处理实体和遥测检索。
- GSearch 让代理沿着依赖图行走，例如服务调用路径，用来检查可能的故障传播路径。

## 结果
- 在 AIOps 2025 Challenge 数据集上，用 UModel 重新建模后，根因定位精度比朴素的基于代理的方法提高了 8%；摘要没有给出绝对精度值。
- 引言还把这描述为 RCA 准确率提升 8%，但摘要没有说明这个 8% 是绝对百分点还是相对提升。
- 阿里云已经在生产环境中部署 UModel 超过 1 年。
- 这套部署已服务数万用户，并统一了数千个标准化模型，覆盖 Kubernetes、网络、容器服务、APM 和云基础设施监控等子系统。
- 据报告，该系统可以每秒处理数百万次操作，大规模数据检索的查询延迟为亚秒级或秒级。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04799v1](https://arxiv.org/abs/2606.04799v1)
