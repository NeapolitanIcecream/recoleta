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
language_code: zh-CN
---

# Show HN: I built CLI for developer docs locally working with any Coding Agent

## Summary
这是一个面向开发者文档的本地化抓取、索引与检索 CLI，可与 Claude Code 的 `/docs` 命令集成，让编码代理直接查询最新、特定版本的官方文档并给出引用。它主要减少开发时在浏览器与代码环境之间来回切换的问题，并为 coding agent 提供可控的本地文档上下文。

## Problem
- 开发者文档分散在大量网站上，结构不统一，查阅时需要频繁离开编码环境去浏览器搜索，打断工作流。
- 现有 AI 编码助手往往拿不到**最新**、**版本特定**的官方文档，容易产生过时或不准确的回答。
- 对于代码智能与自动化开发场景，缺少一个可本地部署、可搜索、可被 coding agent 直接调用的文档基础设施。

## Approach
- 先对目标文档站点做 **BFS 抓取**，并按规则过滤无关页面与 URL。
- 将页面 HTML 清洗，去掉导航栏等站点噪声，再转换成 Markdown，并附加 YAML frontmatter（如标题、来源 URL、文档名、版本）。
- 把 Markdown 文档交给 **qmd** 建立本地 **BM25** 索引，实现离线检索。
- 提供 CLI 命令用于 `scrape / index / search / get / list / read`，同时通过 Claude Code 的 `/docs` skill 暴露给编码代理调用。
- 检索后可返回原始文档并由代理综合生成答案，同时附带来源引用。

## Results
- 文中**没有提供正式基准测试或定量实验结果**，未报告检索准确率、延迟、召回率或与其他系统的数值对比。
- 给出的最具体能力声明是：支持将如 **Node.js v22**、**Next.js 14**、**Bun 1** 等版本化文档抓取并自动索引到本地。
- 系统流程明确为 **Scrape → Filter → Convert → Index → Search**，并支持通过 CLI 直接搜索，或在 Claude Code 中用 `/docs "how does fs.readFile work?"` 这类查询调用。
- 声称的关键效果是：让 AI 助手能搜索并引用**真实文档**，减少上下文切换，并改善版本敏感问题；但这些效果在文中未用数字验证。

## Link
- [https://github.com/lifez/docsearch](https://github.com/lifez/docsearch)
