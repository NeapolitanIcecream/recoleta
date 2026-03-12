---
source: hn
url: https://github.com/azaddjan/aipatternmanager
published_at: '2026-03-02T23:21:13'
authors:
- azaddjan
topics:
- enterprise-architecture
- neo4j
- ai-governance
- pattern-management
- llm-tooling
relevance_score: 0.08
run_id: materialize-outputs
---

# AI Architecture Pattern Manager – Togaf ABB/SBB/PBC with Neo4J

## Summary
这是一个面向企业 AI 架构治理的模式管理平台，用 TOGAF 的 ABB/SBB 与 Gartner 的 PBC 分层组织架构知识，并用 Neo4j 图数据库、LLM 分析与多格式导出把它做成可操作系统。它更像工程平台/工具说明，而不是一篇提供实验验证的新算法论文。

## Problem
- 解决的问题是：企业在规划 AI/LLM 系统时，架构模式分散在不同文档、抽象层和供应商实现中，难以统一管理、追踪依赖、评估覆盖缺口与变更影响。
- 这很重要，因为企业 AI 架构通常横跨蓝图、能力块、解决方案块、业务能力和具体技术产品；如果这些层之间无法对齐，会导致重复建设、接口不一致、治理困难和供应商锁定风险。
- 现有做法往往停留在静态文档或幻灯片，缺少可查询图结构、团队协作权限、健康度评分和 AI 辅助发现/分析能力。

## Approach
- 核心机制是把架构知识建模成一个**多层图谱**：AB/ABB/SBB/PBC/Technology 都作为节点与关系存入 Neo4j，从而支持浏览、搜索、过滤、依赖追踪和影响分析。
- 平台提供结构化模式 CRUD，要求填写 intent、problem、solution、interfaces、invariants 等字段，把原本非结构化的架构经验变成统一模式目录。
- 在此基础上叠加 LLM 能力：用于模式生成与补全、发现缺失模式、对整个模式库做 9 个维度的语义深度分析，以及对单个模式给出上下文化建议。
- 系统还加入治理与运营能力：四维健康评分（Completeness、Relationships、Coverage、Problems）及加权总分、JWT + RBAC + 团队归属、自动备份导入恢复、技术注册表与 PBC 管理。
- 交付形式强调企业落地：前端 React/Vite、后端 FastAPI、Neo4j、Docker Compose 一键启动，并支持导出 HTML、PPT、Word、JSON 以服务不同利益相关者。

## Results
- 文本没有提供标准学术实验、基准数据集或与其他方法的定量对比，因此**没有可核验的量化结果**。
- 给出的最具体功能性结果包括：对整个模式库进行 **9 个分析维度** 的 AI Deep Analysis，覆盖架构一致性、ABB↔SBB 对齐、接口一致性、业务能力缺口、供应商风险、内容质量、模式重叠、PBC 组合和成熟度路线图。
- 健康仪表板提供 **4 个维度** 的模式健康评分，并输出加权总分、单模式下钻与趋势跟踪，但文中未报告任何真实项目上的分数提升幅度。
- 导出能力包括 **4 种格式**：离线单文件 HTML、**30 页** PowerPoint、Word 文档和 JSON 备份；这是清晰的产品规格，不是实验指标。
- 部署方面宣称可通过 Docker Compose 启动，并给出镜像版本 **backend 0.9.0 / frontend 0.9.0**；数据库首次启动会自动创建约束、索引和内置分类。
- 安全与协作上，系统支持基于角色与团队的访问控制、匿名只读开关，以及默认管理员自动初始化，但仍属于工程特性声明，不构成研究突破证据。

## Link
- [https://github.com/azaddjan/aipatternmanager](https://github.com/azaddjan/aipatternmanager)
