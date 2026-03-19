---
source: hn
url: https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/
published_at: '2026-03-03T23:48:20'
authors:
- pyxelr
topics:
- astrojs
- wordpress-migration
- static-site-generation
- cloudflare-pages
- ai-assisted-development
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# After 8 years on WordPress, I migrated to AstroJS Starlight. Here's the how-to

## Summary
这是一篇关于将个人网站从运行 8 年、依赖 25 个插件的 WordPress 迁移到 AstroJS Starlight + Cloudflare Pages 的实践报告。核心价值在于把内容从数据库和插件生态中解放出来，转为 Git 管理的 Markdown 静态站点，并借助 AI 显著降低迁移成本。

## Problem
- 解决的问题是：如何把一个长期运行、插件繁多、性能较慢、受托管环境限制的 WordPress 个人站，迁移为可版本控制、低成本、高性能、以 Markdown 为中心的现代静态站。
- 这件事重要，因为原系统存在 **25 个插件维护负担**、订阅成本、无版本控制、共享主机上的 PHP 性能开销、数据库锁定内容、运行时受主机限制等长期摩擦。
- 对于知识库/数字花园类网站，作者尤其在意内容可移植性、Git 历史、开放源码和更接近 Obsidian 的 Markdown 工作流。

## Approach
- 先做技术选型：比较 Hugo、GatsbyJS、VitePress 和 AstroJS Starlight，最终选择 **Starlight**，因为它原生提供侧边栏、搜索、Markdown/MDX 支持，适合“博客 + 知识库”混合形态。
- 用 WordPress 自带导出工具导出 XML，再通过 **wordpress-export-to-markdown** 转成 Markdown 和本地图片，作为迁移起点。
- 对导出内容做大规模清洗：修复短代码、替换 `wp-content` 远程图片、本地化资源、统一约 **284** 张图片文件名、修正引用/高亮/图片标题、删除过时页面与前置字段。
- 使用 **Claude Code / GitHub Copilot with Claude** 作为 AI 结对程序员，批量处理坏链、SEO 元数据、JSON-LD、RSS、标签页、旧 URL 重定向、图片优化和语法检查，把原本可能持续数周的重复劳动压缩为可管理流程。
- 部署到 **Cloudflare Pages**，设置 `git fetch --unshallow && npm run build` 以保留真实 Git 历史，从而让 Starlight 的“Last updated”基于实际修改时间而非部署时间；运行时固定为 **Node 22**。

## Results
- 性能结果的定性结论非常强：作者称迁移后 **Lighthouse 分数接近全满分**，而原先 WordPress + 共享主机“明显吃力”；文中明确给出一个具体数字：**Accessibility = 98/100**。
- 成本显著下降：当前年度固定成本约为 **~60 PLN/年域名 + ~50 PLN/年邮箱**，其余托管与部署服务免费；相较之前的 WordPress 主机与部分插件/主题订阅，整体更便宜。
- 内容与维护复杂度显著改善：从 **25 个 WordPress 插件** 迁移后，作者审计发现只有 **1 个插件（Redirection）** 需要真正重实现，而且仅是 Astro 配置中的一个重定向映射对象。
- 知识库能力增强：新站已加入一个持续扩展的 digital garden / knowledge base，文中给出规模为 **16+ pages**。
- 迁移工作量有具体量化：一次大型 PR 不仅完成站点基础设施迁移，还修复了 **11 个文件中的约 30 处语法问题**。
- 严格说，这不是学术论文，也没有标准化基准、对照实验或完整指标表；除 **98/100**、**25 插件**、**284 图片**、**16+ 页面**、**~60/50 PLN** 等数字外，其余结果主要是强烈的工程实践性主张。

## Link
- [https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/](https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/)
