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
language_code: en
---

# Show HN: CRM-CLI – A local-first personal CRM for the terminal with MCP server

## Summary
This is a **local-first personal CRM tool for the terminal** that unifies contacts, organizations, interactions, deals, and tasks into a single CLI and SQLite database, with a built-in MCP server for AI agents to read and write directly. It reads more like an engineered product release description than an academic paper, emphasizing privacy, local deployment, scriptability, and AI integration.

## Problem
- Problem addressed: individuals or small teams lack a **lightweight, private, automatable** CRM; existing CRMs often depend on the cloud, account systems, and graphical interfaces, making them poorly suited to terminal workflows and integration with local AI agents.
- Why it matters: sales follow-up, relationship management, pre-meeting preparation, and task tracking require unified context; if data is scattered across notes, email, and spreadsheets, it becomes hard to search, update, and use safely with AI.
- The project also tries to reduce friction for AI agents accessing business data: enabling Claude and others to read and write CRM data through MCP in a structured way, without relying on third-party SaaS APIs.

## Approach
- The core mechanism is straightforward: use a **single static binary CLI** to manage CRM entities, stored underneath in **local SQLite**, with the default database located at `~/.crm/crm.db`.
- The data model covers people, organizations, interaction records, deals, tasks, tags, and relationships, and supports **full-text search** plus commands like `crm context` for pre-meeting briefings that aggregate relevant information at once.
- A unified command-line interface supports CRUD, filtering, soft deletion, pipeline views, overdue tasks, and more, while providing multiple output formats — **table/json/csv/tsv** — for scripting and Unix pipeline composition.
- Built-in **MCP server**: AI agents can access the CRM via `crm mcp serve` to perform actions such as logging interactions, updating deal stages, creating tasks, and updating contact summaries.
- The design emphasizes **local-first / no cloud / no accounts / zero dependencies**, and improves cross-platform deployment convenience through pure Go + no CGO.

## Results
- The text **does not provide standard academic benchmarks or quantitative experimental results**, so there are no comparable figures such as accuracy, success rate, latency, or ablation results.
- The most specific engineering claims provided include: **single static binary**, **SQLite local database**, **no cloud / no accounts**, **zero external dependencies**, **pure-Go SQLite**, **supports Go 1.23+**, **no CGO**, and the ability to build and run on platforms supported by Go.
- In terms of feature coverage, it claims support for **6+ core entity/capability types**: people, organizations, interaction log, deals, tasks, tags, relationships, along with full-text search, context briefing, pipeline view, and multi-format export.
- For AI integration, it claims MCP can enable Claude to perform at least **4 types of update operations**: logging interactions, updating deal stages, creating follow-up tasks, and updating contact summaries.
- For concurrency/deployment, the text claims **SQLite WAL mode** can support concurrent reads reasonably well, but warns against writing from two machines at the same time; it also supports switching the database path via environment variables or arguments, and placing the database in iCloud Drive for cross-device backup.

## Link
- [https://github.com/jdanielnd/crm-cli](https://github.com/jdanielnd/crm-cli)
