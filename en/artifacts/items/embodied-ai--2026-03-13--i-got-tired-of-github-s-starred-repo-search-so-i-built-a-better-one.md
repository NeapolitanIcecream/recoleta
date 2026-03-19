---
source: hn
url: https://github.com/alonronin/orbit
published_at: '2026-03-13T23:52:34'
authors:
- alonronin
topics:
- github-search
- repo-management
- ai-categorization
- developer-tools
- offline-first
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# I got tired of GitHub's starred repo search, so I built a better one

## Summary
This is a tool for managing GitHub starred repositories. Through AI-based automatic categorization and summarization combined with local full-text search, it turns a messy collection of bookmarks into a searchable knowledge base. It is more like a practical developer product than a research paper or robotics-related work.

## Problem
- GitHub’s native starred-repository search and organization capabilities are insufficient; once users accumulate hundreds or thousands of starred repos, it becomes difficult to quickly find the projects they need.
- Starred repositories usually lack consistent tags and concise descriptions, leading to a “star it and forget it” bookmark graveyard problem.
- This problem matters because of developer knowledge-management efficiency: if historical starred items cannot be searched efficiently, the long-term value of starring drops significantly.

## Approach
- Uses GitHub OAuth to sign in and sync all of a user’s starred repositories, supporting **streaming sync** with real-time progress display and continuation after refresh.
- Calls AI on each repository to generate **automatic category labels** and a **one-line summary**, such as Framework, Tool, AI/ML, DevOps, Database, UI, etc.
- Uses **Fuse.js** on the frontend for client-side full-text search, and provides smart filtering and multiple sorting options by language, AI label, and other dimensions.
- Uses **IndexedDB** for offline-first persistence, enabling fast cross-session loading of synced and processed data.
- The engineering implementation is based on Next.js 16, React 19, TypeScript, Vercel AI SDK, TanStack Query/Virtual, Tailwind CSS, and more.

## Results
- The text does not provide standard research experiments, benchmark datasets, or peer baselines, so there are **no quantitative academic results to report**.
- The strongest concrete capability claim provided is support for AI categorization, summarization, search, and filtering across **hundreds or thousands** of GitHub starred repositories.
- The search method is described as **instant client-side full-text search**, powered by Fuse.js; however, no latency, recall, or accuracy numbers are given.
- The sync capability is described as **streaming fetch with real-time progress** and support for resuming after refresh; however, no throughput, success-rate, or runtime metrics are given.
- The default AI model is stated as **groq/gpt-oss-20b** (via Vercel AI SDK / AI Gateway), but no evaluation results for categorization or summary quality are provided.

## Link
- [https://github.com/alonronin/orbit](https://github.com/alonronin/orbit)
