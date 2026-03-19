---
source: hn
url: https://github.com/alonronin/orbit
published_at: '2026-03-13T23:52:34'
authors:
- alonronin
topics:
- github-tools
- repo-search
- ai-categorization
- developer-productivity
- offline-first
relevance_score: 0.69
run_id: materialize-outputs
language_code: en
---

# I got tired of GitHub's starred repo search, so I built a better one

## Summary
This is an application for managing GitHub starred repositories. It improves the efficiency of finding target projects from a large collection of saved repos through AI-powered automatic categorization and summaries combined with local full-text search. It is closer to an engineering product description than an academic paper, with a focus on turning a “favorites list” into a searchable, filterable, offline-usable repository library.

## Problem
- GitHub’s native starred repo search and organization capabilities are insufficient. After users have starred hundreds or thousands of repositories, it becomes difficult to quickly find the projects they need.
- Starred repositories can easily turn into a “bookmark graveyard”: without unified categorization, concise descriptions, and efficient filtering, the value of those saved repos is hard to realize.
- This problem matters because developers’ efficiency in knowledge management, code discovery, and tool reuse directly affects software development and engineering productivity.

## Approach
- The core mechanism is straightforward: first sync all of a user’s GitHub stars, then use AI to generate **category labels** and **one-line summaries** for each repository, and finally provide interfaces for search, filtering, and sorting.
- On the search side, it uses **Fuse.js client-side full-text search**, enabling instant retrieval by name, description, language, or AI label without relying on server-side queries.
- At the data layer, it uses **IndexedDB offline-first storage**, persisting repository metadata locally to achieve fast loading across sessions.
- On the sync side, it supports **streaming fetch with real-time progress display**, and can resume after refresh, which is convenient for handling large numbers of stars.
- The engineering implementation is based on Next.js, React, TypeScript, Vercel AI SDK, and GitHub OAuth, with the default model set to `groq/gpt-oss-20b`.

## Results
- The text **does not provide standard academic evaluation**: it gives no accuracy, recall, latency, user study, or quantitative comparison data against GitHub’s native starred search.
- The strongest quantitative claim is its target scale: it can help users organize “**hundreds (or thousands)** of repos,” meaning hundreds to thousands of starred repositories.
- Functional outcomes include: each repository can automatically receive **1 AI category label** and **1 one-line summary**, and users can organize and retrieve repos by language, label, starred date, star count, last updated time, name, and other dimensions.
- System-level result claims include **instant search** (client-side full-text search), **offline-first** (IndexedDB persistence), and **streaming sync** (with real-time progress and refresh-resume support), but the text does not report specific speed metrics or resource costs.
- Therefore, its main “breakthrough” is in product-experience integration: combining AI categorization, summarization, local search, and offline caching into a tool better suited for managing GitHub stars, rather than proposing a new algorithm or providing verifiable SOTA performance.

## Link
- [https://github.com/alonronin/orbit](https://github.com/alonronin/orbit)
