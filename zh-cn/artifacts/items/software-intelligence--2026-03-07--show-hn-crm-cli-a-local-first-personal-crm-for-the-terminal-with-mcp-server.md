---
source: hn
url: https://github.com/jdanielnd/crm-cli
published_at: '2026-03-07T22:32:45'
authors:
- jdanielnd
topics:
- local-first
- terminal-crm
- mcp-server
- ai-agent-integration
- sqlite
- command-line-tools
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: CRM-CLI – A local-first personal CRM for the terminal with MCP server

## Summary
这是一个面向终端的本地优先个人 CRM 工具，使用单一二进制和 SQLite 管理联系人、组织、互动、商机与任务。其关键特色是内置 MCP 服务器，使 Claude 等 AI 代理可以直接读写 CRM，实现人与 AI 协同维护关系数据。

## Problem
- 个人 CRM 往往依赖云端账户和图形界面，不适合重视隐私、可脚本化和终端工作流的用户。
- AI 代理虽然能帮助记录会谈与跟进，但通常缺少一个可本地访问、结构化、可写入的联系人/销售上下文系统。
- 会前准备、互动记录、任务跟进和关系维护分散在多个工具中，导致信息碎片化、自动化困难。

## Approach
- 提供一个**local-first** 的 CLI CRM：单个静态二进制 + SQLite 数据库 + 无云端账号，数据默认保留在本机。
- 用统一命令管理核心实体：person、org、interaction、deal、task、tag、relationship，并支持软删除、筛选、状态面板和管道视图。
- 内置全文搜索与 `crm context` 上下文简报命令，把联系人资料、组织、近期互动、未完成商机、待办、关系和标签聚合成会前摘要。
- 通过多格式输出（table/JSON/CSV/TSV）、标准 stdout/stderr、结构化退出码，兼容 Unix 管道、jq、fzf 等自动化工具链。
- 内置 MCP server，允许 Claude 等 AI 代理通过结构化协议查询和更新 CRM；联系人 `summary` 字段被设计为由 AI 持续维护的动态档案。

## Results
- 文本**没有提供基准测试或正式量化实验结果**，因此没有准确的性能、准确率或用户研究数字可报告。
- 功能覆盖上，系统声称支持 **5+ 核心业务对象**（contacts/orgs/interactions/deals/tasks），并额外支持 tags、relationships、full-text search、context briefing、pipeline/status dashboard。
- 部署复杂度上，项目宣称为 **single static binary**、**zero dependencies**、**no cloud / no accounts**、**pure-Go SQLite**，可在 Go 运行的平台上工作，构建要求为 **Go 1.23+**。
- 互操作性上，提供 **4 种输出格式**（table、JSON、CSV、TSV）和 **6 个退出码语义**（0、1、2、3、4、10），强调脚本化与自动化集成能力。
- AI 集成上，作者给出了 Claude 通过 MCP 自动执行 **4 类操作** 的具体示例：记录互动、更新商机阶段、创建跟进任务、更新联系人摘要。强主张是 AI 可以在会后直接把自然语言转成 CRM 写操作。
- 存储与同步上，数据库默认位于 `~/.crm/crm.db`，并声称可通过将 SQLite 文件放入 iCloud Drive 实现跨设备备份；同时明确提示 SQLite WAL 适合并发读，但不建议双机同时写入。

## Link
- [https://github.com/jdanielnd/crm-cli](https://github.com/jdanielnd/crm-cli)
