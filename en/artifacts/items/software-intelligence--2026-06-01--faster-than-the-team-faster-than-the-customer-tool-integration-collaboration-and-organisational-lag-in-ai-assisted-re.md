---
source: arxiv
url: https://arxiv.org/abs/2606.01772v1
published_at: '2026-06-01T06:53:56'
authors:
- "Jan-Philipp Stegh\xF6fer"
topics:
- requirements-engineering
- ai-assisted-development
- human-ai-interaction
- tool-integration
- software-teams
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Faster than the Team, Faster than the Customer: Tool Integration, Collaboration, and Organisational Lag in AI-assisted RE

## Summary
This qualitative industry study finds that AI-assisted requirements engineering already changes product-owner work at XITASO, mainly through backlog, tender, document, and domain-understanding tasks. Product owners gain speed when tools connect to Jira, Confluence, code, or tender sources, while teams and customers often adapt more slowly.

## Problem
- The paper studies how generative AI affects requirements engineering in daily industrial work, where product owners must turn incomplete customer input into usable backlog items, bids, prototypes, and shared product direction.
- This matters because requirements work depends on tool context, team discussion, customer rules, and traceability; isolated LLM task tests miss those conditions.
- The study also examines a collaboration risk: AI can help one product owner produce artifacts faster than developers, customers, and team processes can review or absorb them.

## Approach
- The author ran a 2024 company-wide survey at XITASO, collecting 20 AI use cases from 11 communities of practice.
- A committee selected requirements-related areas, then interviews refined them into 15 use cases across 4 categories: product backlog management, tender management, requirements and domain understanding, and document and artifact creation.
- The study used two rounds of semi-structured interviews with 8 product owners in late 2025 and spring 2026; all had at least 5 years of PO experience and active AI use.
- Tools covered include ChatXiPT, Product Copilot, MS Copilot, Claude Desktop, Claude Code, TenderZen, Curly, and Rovo.
- The core mechanism is simple: product owners feed project artifacts, tender documents, backlog items, code context, meeting data, or prompts into AI tools; the tools draft, restructure, search, extract, summarize, or prototype outputs that the PO reviews.

## Results
- The paper reports no controlled benchmark for accuracy, quality, or productivity. Its evidence is qualitative, with counts of participants, tools, and use cases.
- It identifies 15 AI-assisted RE use cases across 4 categories, based on 20 initial survey use cases and interviews with 8 product owners.
- Backlog refinement is the most common use case: 6 of 8 product owners use AI to split epics, find duplicates, add acceptance criteria, detect gaps, or improve backlog items.
- Backlog bootstrapping is used by 4 of 8 product owners to generate many product backlog items from Excel sheets, screenshots, or specification documents; participants report large time savings, but the excerpt gives no measured hours saved.
- Tender management is used mainly by 2 product owners through a 4-stage pipeline: tender discovery, tender analysis, reference matching, and bid authoring.
- The main empirical claim is that tool connection drives value: integrated setups such as Jira plus source-code access through MCP let a PO refine requirements with implementation context, while missing links between tools still force manual handoffs.

## Link
- [https://arxiv.org/abs/2606.01772v1](https://arxiv.org/abs/2606.01772v1)
