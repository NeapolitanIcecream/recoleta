---
source: hn
url: https://github.com/lifez/docsearch
published_at: '2026-03-04T23:25:28'
authors:
- lifez
topics:
- developer-tools
- local-search
- documentation-retrieval
- claude-code
- bm25
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Show HN: I built CLI for developer docs locally working with any Coding Agent

## Summary
This is a local retrieval CLI for developer documentation. It can scrape official docs, convert them to Markdown, build a local index, and integrate with Claude Code through `/docs`. Its goal is to let coding agents search and cite real, up-to-date, version-specific documentation, reducing the cost of developers frequently switching to a browser to look things up.

## Problem
- Developer documentation is scattered across many websites with inconsistent structures, requiring frequent switching between the editor and browser when searching for information.
- Coding assistants often cannot access the latest, version-specific official documentation, making them prone to giving outdated or inaccurate answers.
- There is a lack of a simple local solution that connects document scraping, cleaning, indexing, and agent-oriented retrieval into one workflow.

## Approach
- First, perform **BFS crawling** on documentation sites, keeping only relevant pages and filtering out navigation bars, page chrome, and other irrelevant content.
- Convert the cleaned HTML into **Markdown**, and attach YAML frontmatter such as title, source URL, document name, and version number.
- Use **qmd** to build a local **BM25 retrieval index** over the Markdown documents, supporting CLI queries, filtering by collection, and fetching full text by docid.
- Connect local retrieval to the coding agent through Claude Code's `/docs` skill, enabling it to search, read full documents, and generate synthesized answers with source citations.

## Results
- The text **does not provide standard benchmark tests or quantitative experimental results**; it gives no recall, accuracy, latency, or numerical comparisons with other tools.
- The most concrete capability claims given are: it supports the full `scrape / index / search / get / list / read` workflow from the command line, and can scrape versioned documentation collections such as `node/22`, `nextjs/14`, and `bun/1`.
- The system claims that Claude Code can use queries such as `/docs "how does fs.readFile work?"` to directly search local documentation and generate answers **with citations**.
- Its core value proposition is to connect “scrape HTML → convert to Markdown → local BM25 indexing → agent retrieval” into a single local workflow, thereby enabling access to “the latest, version-specific” real developer documentation.

## Link
- [https://github.com/lifez/docsearch](https://github.com/lifez/docsearch)
