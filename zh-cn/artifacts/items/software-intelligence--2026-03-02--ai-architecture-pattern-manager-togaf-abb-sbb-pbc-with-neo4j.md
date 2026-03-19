---
source: hn
url: https://github.com/azaddjan/aipatternmanager
published_at: '2026-03-02T23:21:13'
authors:
- azaddjan
topics:
- enterprise-architecture
- neo4j
- architecture-patterns
- llm-tooling
- knowledge-graph
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# AI Architecture Pattern Manager – Togaf ABB/SBB/PBC with Neo4J

## Summary
这是一个面向企业AI架构治理的模式管理平台，把 TOGAF 的 ABB/SBB 与 Gartner 的 PBC 结合到一个基于 Neo4j 的可视化与可分析目录中。它重点解决跨抽象层的模式建模、关系追踪、AI辅助补全与导出治理工件的问题。

## Problem
- 企业AI架构模式通常分散在文档、白板和团队经验中，难以统一管理从企业蓝图到厂商实现的多层抽象。
- 缺少对 ABB、SBB、PBC、技术产品之间关系的可视化、可追踪和可变更影响分析，导致架构治理与复用效率低。
- 纯手工维护模式库成本高，也难以发现缺失模式、内容质量问题和能力覆盖空白，这会影响企业级AI系统设计的一致性与落地速度。

## Approach
- 用一个图数据库驱动的平台统一管理多层对象：Architecture Blueprints、ABB、SBB、PBC 和 Technologies，并显式建模它们之间的关系。
- 提供结构化 Pattern CRUD，为每个模式保存 intent、problem、solution、interfaces、invariants 等 typed fields，形成可治理的模式目录。
- 在前端用交互式图谱浏览、搜索、过滤和双击导航来查看跨层依赖；在后端结合 Neo4j 查询与健康评分来评估完整性、关系、覆盖率和问题。
- 接入多种 LLM 提供商（Anthropic、OpenAI、AWS Bedrock、Ollama）做 AI authoring、缺失模式发现、单模式顾问和覆盖 9 个维度的全库深度语义分析。
- 配套 RBAC/JWT、团队所有权、导入恢复、以及 HTML/PPTX/DOCX/JSON 多格式导出，使其既是知识库也是企业架构治理工作台。

## Results
- 文本没有提供基于公开数据集或标准基准的定量实验结果，因此**没有可核验的学术性能数字**。
- 明确声称支持 **5 类核心架构层/实体**：AB、ABB、SBB、PBC、Technologies，并覆盖 Core AI/LLM、Integration、Agents、Knowledge & Retrieval 等多个类别。
- 平台提供 **4 维健康评分**：Completeness、Relationships、Coverage、Problems，并生成 weighted overall score、drill-down 与 trend tracking，但未给出评分公式效果数字。
- AI deep analysis 覆盖 **9 个分析区域**，包括架构一致性、ABB↔SBB 对齐、接口一致性、业务能力缺口、供应商风险、内容质量、模式重叠、PBC 组合和成熟度路线图。
- 导出能力给出较具体的产物规格：**30-slide PowerPoint**、可离线查看的 self-contained HTML、结构化 Word 文档，以及完整 JSON 备份/恢复。
- 工程实现上提供可直接运行的 Docker 镜像版本 **backend:0.9.0** 与 **frontend:0.9.0**，并宣称首启自动创建约束、索引、内置分类及管理员账户。

## Link
- [https://github.com/azaddjan/aipatternmanager](https://github.com/azaddjan/aipatternmanager)
