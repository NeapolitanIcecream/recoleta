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
language_code: zh-CN
---

# Show HN: I built CLI for developer docs locally working with any Coding Agent

## Summary
这是一个面向开发者文档的本地检索 CLI，可抓取官网文档、转为 Markdown、建立本地索引，并通过 `/docs` 集成到 Claude Code 中。它旨在让编码代理基于最新、特定版本的真实文档进行检索和引用，减少开发者频繁切换浏览器查资料的成本。

## Problem
- 开发者文档分散在大量网站上，结构不统一，查找信息时需要频繁在编辑器与浏览器之间切换。
- 代码助手通常无法访问最新、特定版本的官方文档，容易给出过时或不准确的答案。
- 缺少一种简单的本地化方案，把文档抓取、清洗、索引和面向代理的检索串起来。

## Approach
- 先对文档站点做 **BFS 抓取**，只保留相关页面，并过滤导航栏、页面 chrome 等无关内容。
- 将清洗后的 HTML 转成 **Markdown**，并附加 YAML frontmatter，如标题、来源 URL、文档名和版本号。
- 使用 **qmd** 对 Markdown 文档做本地 **BM25 检索索引**，支持 CLI 查询、按 collection 过滤、按 docid 取全文。
- 通过 Claude Code 的 `/docs` 技能把本地检索接入编码代理，使其可以搜索、读取全文并带来源引用地综合回答。

## Results
- 文中**没有提供标准基准测试或定量实验结果**，没有给出召回率、准确率、延迟或与其他工具的数值对比。
- 给出的最具体能力声明是：支持从命令行完成 `scrape / index / search / get / list / read` 全流程，并能抓取如 `node/22`、`nextjs/14`、`bun/1` 等版本化文档集合。
- 系统声称可让 Claude Code 通过 `/docs "how does fs.readFile work?"` 等查询，直接检索本地文档并生成**带引用**的回答。
- 核心价值主张是：把“抓取 HTML → 转 Markdown → 本地 BM25 索引 → 代理检索”串成一条本地工作流，从而访问“最新、特定版本”的真实开发文档。

## Link
- [https://github.com/lifez/docsearch](https://github.com/lifez/docsearch)
