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
language_code: en
---

# Show HN: CRM-CLI – A local-first personal CRM for the terminal with MCP server

## Summary
This is a local-first personal CRM tool for the terminal, using a single binary and SQLite to manage contacts, organizations, interactions, deals, and tasks. Its key feature is a built-in MCP server, allowing AI agents such as Claude to directly read from and write to the CRM, enabling humans and AI to collaboratively maintain relationship data.

## Problem
- Personal CRMs often depend on cloud accounts and graphical interfaces, making them unsuitable for users who prioritize privacy, scriptability, and terminal-based workflows.
- Although AI agents can help record meetings and follow-ups, they usually lack a locally accessible, structured, writable contact/sales context system.
- Pre-meeting preparation, interaction logging, task follow-up, and relationship management are scattered across multiple tools, leading to fragmented information and difficult automation.

## Approach
- Provide a **local-first** CLI CRM: a single static binary + SQLite database + no cloud account, with data kept on the local machine by default.
- Use unified commands to manage core entities: person, org, interaction, deal, task, tag, relationship, while supporting soft deletion, filtering, status dashboards, and pipeline views.
- Built-in full-text search and the `crm context` context briefing command aggregate contact profiles, organizations, recent interactions, open deals, to-dos, relationships, and tags into a pre-meeting summary.
- Through multiple output formats (table/JSON/CSV/TSV), standard stdout/stderr, and structured exit codes, it is compatible with Unix pipelines and automation toolchains such as jq and fzf.
- Built-in MCP server allows AI agents such as Claude to query and update the CRM through a structured protocol; the contact `summary` field is designed as a dynamic profile continuously maintained by AI.

## Results
- The text **does not provide benchmark tests or formal quantitative experimental results**, so there are no precise performance, accuracy, or user-study figures to report.
- In terms of feature coverage, the system claims support for **5+ core business objects** (contacts/orgs/interactions/deals/tasks), with additional support for tags, relationships, full-text search, context briefing, and pipeline/status dashboard.
- In terms of deployment complexity, the project claims to be a **single static binary**, have **zero dependencies**, **no cloud / no accounts**, and **pure-Go SQLite**, and to work on platforms supported by Go, with a build requirement of **Go 1.23+**.
- In terms of interoperability, it provides **4 output formats** (table, JSON, CSV, TSV) and **6 exit code semantics** (0, 1, 2, 3, 4, 10), emphasizing scriptability and automation integration.
- For AI integration, the author gives concrete examples of Claude automatically performing **4 types of operations** through MCP: logging interactions, updating deal stages, creating follow-up tasks, and updating contact summaries. The strong claim is that AI can directly turn natural language into CRM write operations after a meeting.
- For storage and sync, the database is located by default at `~/.crm/crm.db`, and it is claimed that cross-device backup can be achieved by placing the SQLite file in iCloud Drive; it also explicitly notes that SQLite WAL is suitable for concurrent reads, but dual-machine simultaneous writes are not recommended.

## Link
- [https://github.com/jdanielnd/crm-cli](https://github.com/jdanielnd/crm-cli)
