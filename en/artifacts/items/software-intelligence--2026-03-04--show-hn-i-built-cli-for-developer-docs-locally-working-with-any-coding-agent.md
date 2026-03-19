---
source: hn
url: https://github.com/lifez/docsearch
published_at: '2026-03-04T23:25:28'
authors:
- lifez
topics:
- developer-docs
- code-intelligence
- local-search
- coding-agent-tools
- documentation-retrieval
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Show HN: I built CLI for developer docs locally working with any Coding Agent

## Summary
This is a local CLI for scraping, indexing, and searching developer documentation. It integrates with Claude Code's `/docs` command, allowing coding agents to directly query the latest, version-specific official docs and provide citations. Its main goal is to reduce the need to switch back and forth between the browser and the coding environment, while providing coding agents with controllable local documentation context.

## Problem
- Developer documentation is scattered across many websites with inconsistent structures. Looking things up often requires leaving the coding environment and searching in a browser, disrupting workflow.
- Existing AI coding assistants often cannot access the **latest** and **version-specific** official documentation, making outdated or inaccurate answers more likely.
- For code intelligence and automated development scenarios, there is a lack of documentation infrastructure that can be deployed locally, searched, and called directly by a coding agent.

## Approach
- First, perform **BFS crawling** on the target documentation site and filter irrelevant pages and URLs according to rules.
- Clean the page HTML, remove site noise such as navigation bars, then convert it to Markdown and attach YAML frontmatter (such as title, source URL, document name, and version).
- Feed the Markdown documents into **qmd** to build a local **BM25** index for offline retrieval.
- Provide CLI commands for `scrape / index / search / get / list / read`, while also exposing them to coding agents through Claude Code's `/docs` skill.
- After retrieval, the original documents can be returned and the agent can synthesize an answer with source citations.

## Results
- The text **does not provide formal benchmarks or quantitative experimental results**; it does not report retrieval accuracy, latency, recall, or numerical comparisons with other systems.
- The most specific capability claim provided is support for scraping and automatically indexing versioned documentation such as **Node.js v22**, **Next.js 14**, and **Bun 1** locally.
- The system workflow is clearly defined as **Scrape → Filter → Convert → Index → Search**, and it supports direct CLI search or queries in Claude Code such as `/docs \"how does fs.readFile work?\"`.
- The claimed key benefits are enabling AI assistants to search and cite **real documentation**, reducing context switching, and improving version-sensitive lookups; however, these effects are not numerically validated in the text.

## Link
- [https://github.com/lifez/docsearch](https://github.com/lifez/docsearch)
