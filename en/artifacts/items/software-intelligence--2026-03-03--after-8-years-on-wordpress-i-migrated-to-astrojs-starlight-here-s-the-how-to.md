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
language_code: en
---

# After 8 years on WordPress, I migrated to AstroJS Starlight. Here's the how-to

## Summary
This is a practical report on migrating a personal website from an 8-year-old WordPress setup relying on 25 plugins to AstroJS Starlight + Cloudflare Pages. The core value lies in freeing content from the database and plugin ecosystem, turning it into a Git-managed Markdown static site, and using AI to significantly reduce migration costs.

## Problem
- The problem being solved is how to migrate a long-running personal WordPress site with many plugins, slow performance, and hosting-environment constraints into a modern static site that is version-controlled, low-cost, high-performance, and centered around Markdown.
- This matters because the original system had long-term friction points such as the **maintenance burden of 25 plugins**, subscription costs, no version control, PHP performance overhead on shared hosting, content locked in a database, and runtime limitations imposed by the host.
- For a knowledge base / digital garden type of site, the author especially values content portability, Git history, open source, and a Markdown workflow closer to Obsidian.

## Approach
- First, a technical evaluation was done: Hugo, GatsbyJS, VitePress, and AstroJS Starlight were compared, and **Starlight** was ultimately chosen because it natively provides a sidebar, search, and Markdown/MDX support, making it suitable for a hybrid “blog + knowledge base” format.
- The built-in WordPress export tool was used to export XML, which was then converted into Markdown and local images via **wordpress-export-to-markdown** as the starting point for the migration.
- The exported content then underwent large-scale cleanup: fixing shortcodes, replacing remote `wp-content` images, localizing assets, standardizing filenames for about **284** image files, correcting quotes/highlighting/image captions, and removing outdated pages and frontmatter fields.
- **Claude Code / GitHub Copilot with Claude** was used as an AI pair programmer to batch-handle broken links, SEO metadata, JSON-LD, RSS, tag pages, old URL redirects, image optimization, and syntax checks, compressing repetitive work that might otherwise have taken weeks into a manageable process.
- Deployment was done on **Cloudflare Pages**, with `git fetch --unshallow && npm run build` configured to preserve real Git history so that Starlight’s “Last updated” is based on actual modification time rather than deployment time; the runtime was fixed at **Node 22**.

## Results
- The qualitative conclusion on performance is very strong: the author says that after migration the **Lighthouse score was nearly perfect**, whereas the original WordPress + shared hosting setup was “clearly struggling”; the article explicitly provides one specific number: **Accessibility = 98/100**.
- Costs dropped significantly: the current annual fixed cost is about **~60 PLN/year for the domain + ~50 PLN/year for email**, while all other hosting and deployment services are free; compared with the previous WordPress hosting and some plugin/theme subscriptions, it is cheaper overall.
- Content and maintenance complexity improved substantially: after migrating away from **25 WordPress plugins**, the author’s audit found that only **1 plugin (Redirection)** actually needed to be reimplemented, and even that was just a redirect mapping object in Astro configuration.
- Knowledge base capabilities were enhanced: the new site now includes a continuously expanding digital garden / knowledge base, described in the article as having **16+ pages**.
- The migration workload is specifically quantified: one large PR not only completed the site infrastructure migration, but also fixed **about 30 syntax issues across 11 files**.
- Strictly speaking, this is not an academic paper and does not include standardized benchmarks, controlled experiments, or a complete metrics table; aside from figures such as **98/100**, **25 plugins**, **284 images**, **16+ pages**, and **~60/50 PLN**, the remaining results are mainly strong claims grounded in engineering practice.

## Link
- [https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/](https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/)
