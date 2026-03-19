---
source: hn
url: https://github.com/jdanielnd/crm-cli
published_at: '2026-03-07T22:32:45'
authors:
- jdanielnd
topics:
- cli-tool
- personal-crm
- local-first
- sqlite
- mcp
- ai-agent-integration
relevance_score: 0.07
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: CRM-CLI – A local-first personal CRM for the terminal with MCP server

## Summary
这是一个**本地优先的终端个人 CRM 工具**，把联系人、组织、互动、商机和任务统一到单个 CLI 与 SQLite 数据库中，并内置 MCP 服务器供 AI 代理直接读写。它更像是工程化产品发布说明而非学术论文，重点在隐私、本地部署、可脚本化和 AI 集成。

## Problem
- 解决的问题：个人或小团队缺少**轻量、私有、可自动化**的 CRM；现有 CRM 往往依赖云端、账户体系和图形界面，不适合终端工作流与本地 AI 代理集成。
- 为什么重要：销售跟进、关系维护、会前准备和任务追踪需要统一上下文；如果数据分散在笔记、邮件和表格中，就难以搜索、更新和让 AI 安全使用。
- 该项目还试图解决 AI 代理接入业务数据的摩擦：让 Claude 等通过 MCP 以结构化方式读写 CRM，而不必依赖第三方 SaaS API。

## Approach
- 核心机制很简单：用一个**单静态二进制 CLI** 管理 CRM 实体，底层存到**本地 SQLite**，默认数据库位于 `~/.crm/crm.db`。
- 数据模型覆盖人、组织、互动记录、商机、任务、标签和人际关系，并支持**全文搜索**与 `crm context` 这种会前简报命令，把相关信息一次性聚合出来。
- 通过统一的命令行接口支持增删改查、筛选、软删除、流水线视图、逾期任务等，并提供 **table/json/csv/tsv** 多种输出，方便脚本和 Unix 管道组合。
- 内置 **MCP server**：AI 代理可通过 `crm mcp serve` 访问 CRM，执行如记录互动、更新 deal 阶段、创建任务、更新联系人摘要等操作。
- 设计上强调**local-first / no cloud / no accounts / zero dependencies**，并通过纯 Go + 无 CGO 的方式提升跨平台部署便利性。

## Results
- 文本**没有提供标准学术基准或定量实验结果**，因此没有 accuracy、success rate、latency、ablation 等可对比数字。
- 给出的最具体工程性声明包括：**单个静态二进制**、**SQLite 本地数据库**、**无云端/无账户**、**零外部依赖**、**纯 Go SQLite**、**支持 Go 1.23+**、**无 CGO**、可在 Go 支持的平台构建运行。
- 功能覆盖上，声明支持 **6+ 类核心实体/能力**：people、organizations、interaction log、deals、tasks、tags、relationships，并带全文搜索、上下文简报、pipeline 视图和多格式导出。
- AI 集成上，声明可通过 MCP 让 Claude 完成至少 **4 类更新操作**：记录互动、更新商机阶段、创建跟进任务、更新联系人摘要。
- 并发/部署方面，文本声称 **SQLite WAL mode** 能较好支持并发读取，但提醒不要从两台机器同时写入；还支持通过环境变量或参数切换数据库路径，以及将数据库放到 iCloud Drive 做跨设备备份。

## Link
- [https://github.com/jdanielnd/crm-cli](https://github.com/jdanielnd/crm-cli)
