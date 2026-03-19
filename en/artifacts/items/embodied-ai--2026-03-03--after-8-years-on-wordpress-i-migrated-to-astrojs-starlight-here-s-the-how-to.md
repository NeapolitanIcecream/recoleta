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
language_code: en
---

# After 8 years on WordPress, I migrated to AstroJS Starlight. Here's the how-to

## Summary
This is not a robotics or machine learning paper, but a practical write-up about migrating a personal website from WordPress to AstroJS Starlight + Cloudflare Pages. Its core value lies in replacing a traditional WordPress setup—burdened by many plugins, weaker performance, and hosting-environment constraints—with Markdown, Git, and static deployment.

## Problem
- The problem being solved is: how to migrate a long-running personal WordPress site to a lighter, version-controllable, higher-performance, lower-cost static site architecture.
- This matters because the original site had real pain points, including the **maintenance burden of 25 plugins**, subscription costs, poor shared-hosting performance, restricted PHP/hosting environments, content locked in a database, and a lack of Git version control.
- This is especially important for content creators: the author wanted to keep content as **plain Markdown files**, so it could evolve, interlink, and remain maintainable over the long term, like an Obsidian vault.

## Approach
- In terms of technology selection, the author compared **Hugo, GatsbyJS, VitePress, and AstroJS Starlight**, and ultimately chose Starlight because it natively provides a documentation-style sidebar, search, and Markdown/MDX support, making it suitable for a hybrid structure of “blog + knowledge base/digital garden.”
- The content migration process was straightforward: first use WordPress’s built-in export to generate XML, then convert it into Markdown and image assets with `wordpress-export-to-markdown`.
- The real core mechanism was **“post-export bulk cleanup + static site reconstruction”**: fixing shortcodes, replacing remote images, standardizing filenames for about **284** images, cleaning up frontmatter, and adding infrastructure such as RSS, LaTeX, SEO, and redirects.
- The author made extensive use of **Claude Code/Copilot with Claude** as AI pair-programming tools to help with broken-link fixes, SEO configuration, custom components, tabs, RSS, URL redirects, image optimization and deduplication, and syntax proofreading, significantly reducing the manual cost of the migration.
- Deployment uses an automated **Cloudflare Pages + GitHub** workflow, and fixes Starlight’s “Last updated” timestamps— which depend on full Git history—via `git fetch --unshallow`.

## Results
- The clearest quantitative results are the migration scale: the original WordPress site had been running for **8 years** and relied on **25 plugins**; during migration, about **284 image filenames** were standardized, and **around 30 syntax issues across 11 files** were fixed.
- Costs dropped significantly: the current annual fixed cost is about **~60 PLN/year for the domain + ~50 PLN/year for email**, while the rest of the hosting and deployment is basically free; compared with the previous ongoing costs for shared hosting and some plugin/theme subscriptions, this is lower.
- On performance, the author claims the Lighthouse comparison showed a “huge difference,” with the new site reaching **near-perfect scores** on Cloudflare’s edge network; the only explicit score given in the article is **accessibility 98/100**, with the explanation that it was not a perfect score because some pages intentionally used non-sequential heading levels.
- In terms of functionality, the new site supports a knowledge base/digital garden and currently has **16+ pages**; it also adds capabilities such as automatic preview deployments, rollbacks, broken-link checks, recommended-content sync, annual automatic rebuilds, and availability monitoring at 5-minute intervals.
- No strictly reproducible experimental baseline, dataset, or standard benchmark is provided, so this is better viewed as a high-quality engineering case study rather than an academic breakthrough; the strongest conclusion is that, for this author, the static-site approach is clearly superior to the original WordPress setup in maintainability, controllability, performance, and cost.

## Link
- [https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/](https://pawelcislo.com/posts/migrating-from-wordpress-to-astrojs-starlight/)
