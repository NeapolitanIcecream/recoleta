---
source: hn
url: https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/
published_at: '2026-03-03T23:48:20'
authors:
- pyxelr
topics:
- wordpress-migration
- astrojs-starlight
- static-site-generator
- cloudflare-pages
- markdown-workflow
relevance_score: 0.01
run_id: materialize-outputs
---

# After 8 years on WordPress, I migrated to AstroJS Starlight. Here's the how-to

## Summary
这不是一篇机器人或机器学习论文，而是一篇关于将个人网站从 WordPress 迁移到 AstroJS Starlight + Cloudflare Pages 的实践总结。核心价值在于用 Markdown、Git 和静态部署替代插件繁重、性能较差且受托管环境限制的传统 WordPress 方案。

## Problem
- 解决的问题是：如何把一个运行多年的 WordPress 个人站，迁移到更轻量、可版本控制、性能更高、成本更低的静态站架构。
- 之所以重要，是因为原站点存在 **25 个插件维护负担**、订阅费用、共享主机性能差、PHP/主机环境受限、内容被数据库锁定、缺乏 Git 版本控制等实际痛点。
- 对内容创作者尤其重要：作者希望内容以 **纯 Markdown 文件** 持有，像 Obsidian 笔记库一样可演化、可互链、可长期维护。

## Approach
- 选型上，作者比较了 **Hugo、GatsbyJS、VitePress、AstroJS Starlight**，最终选择 Starlight，因为其原生提供文档式侧边栏、搜索、Markdown/MDX 支持，适合“博客 + 知识库/digital garden”的混合结构。
- 内容迁移流程很直接：先用 WordPress 内置导出生成 XML，再用 `wordpress-export-to-markdown` 转成 Markdown 和图片资源。
- 真正的核心机制是 **“导出后批量清洗 + 静态站重构”**：修复短代码、替换远程图片、统一约 **284** 张图片文件名、清理 frontmatter、补上 RSS/LaTeX/SEO/重定向等基础设施。
- 作者大量使用 **Claude Code/Copilot with Claude** 作为 AI 结对编程工具，辅助完成坏链修复、SEO 配置、自定义组件、标签页、RSS、URL 重定向、图片优化去重和语法审校，从而显著降低迁移的人力成本。
- 部署采用 **Cloudflare Pages + GitHub** 自动化工作流，并通过 `git fetch --unshallow` 修复 Starlight “Last updated” 时间戳依赖完整 Git 历史的问题。

## Results
- 最明确的量化结果是迁移规模：原 WordPress 站点运行 **8 年**，依赖 **25 个插件**；迁移中标准化了约 **284 张图片文件名**，并修复了 **11 个文件中的约 30 处语法问题**。
- 成本显著下降：当前年度固定成本约为 **~60 PLN/年域名 + ~50 PLN/年邮箱**，其余托管与部署基本免费；相较原先持续支付共享主机和部分插件/主题订阅，成本更低。
- 性能方面，作者声称 Lighthouse 对比“差异巨大”，新站在 Cloudflare 边缘网络上达到 **接近满分**；文中唯一明确给出的分数是 **可访问性 98/100**，并解释未满分是因为部分页面故意使用了非连续标题级别。
- 功能结果上，新站支持知识库/数字花园，当前已有 **16+ 页面**；并新增自动预览部署、回滚、坏链检查、推荐内容同步、年度自动重建、5 分钟间隔可用性监控等能力。
- 没有提供严格可复现的实验基线、数据集或标准 benchmark，因此这更像是高质量工程案例而非学术突破；最强结论是：静态站方案在可维护性、可控性、性能与成本上明显优于作者原有的 WordPress 配置。

## Link
- [https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/](https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/)
