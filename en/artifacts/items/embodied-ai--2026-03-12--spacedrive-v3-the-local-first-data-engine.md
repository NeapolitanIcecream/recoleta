---
source: hn
url: https://spacedrive.com/blog/spacedrive-v3-launch
published_at: '2026-03-12T22:57:04'
authors:
- raybb
topics:
- local-first
- search-index
- prompt-injection-defense
- data-integration
- agent-memory
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Spacedrive v3: The local-first data engine

## Summary
Spacedrive v3 is a local-first data engine that turns data scattered across email, notes, browsers, Slack, files, and more into a searchable knowledge layer through a unified index. Its core selling point is not file management, but performing secure screening, quality classification, and structured processing locally first, then exposing the data to search and AI agents.

## Problem
- Existing file managers/local data tools either have too broad a product surface and overly heavy cross-platform implementations, making stable delivery difficult; or they feed raw content directly into search and LLMs, lacking security boundaries.
- When external content such as email and Slack enters AI retrieval corpora, malicious text may manipulate agents through prompt injection; the article describes this as OWASP's #1 LLM vulnerability.
- Users need a way to retrieve all personal and work data from a single entry point without handing data to the cloud, while also distinguishing trust levels and privacy permissions across different sources.

## Approach
- Abstract each data source as a repository: the data remains where it is, while Spacedrive stores only a local SQLite database, vector index, metadata, hashes, and extracted text.
- Design a four-stage processing pipeline: 1) use Prompt Guard 2 for local injection screening; 2) perform content quality/noise/category classification; 3) perform adapter-specific processing; 4) write only records that pass the earlier stages into FTS5 and LanceDB indexes.
- Use trust tiers and repository-level visibility controls to isolate different data sources, such as authored, collaborative, external, with support for private/shared/agent-excluded.
- Use a scripted adapter system to connect heterogeneous data sources; at launch it provides 11 adapters and supports UTC-normalized time and cursor-based incremental sync.
- Architecturally, it uses a pure Rust core library, while the CLI, desktop app, and Spacebot are all thin clients; single binary, no server dependencies, fully local operation.

## Results
- This is a product launch post rather than an academic paper, and **does not provide quantitative benchmarks or comparative experimental results on standard datasets**.
- The clearest performance number given in the article is that Prompt Guard 2 screens each chunk in **under 50ms** on a local CPU.
- Historical project impact metrics: over the past four years it has achieved **37,000 GitHub stars** and **600,000 downloads**; the v1 alpha was downloaded about **500,000** times; it also raised a **$2M** seed round.
- Engineering scale claims: v2 previously contained **183k lines of Rust code**; the current v3 architecture has **68 tests** covering subsystems; at launch it supports **11 adapters**.
- The core product claim is differentiation relative to existing local data tools: before entering search/AI, all content first goes through injection protection, quality classification, and trust-tiering, rather than going into the LLM context “as is.”

## Link
- [https://spacedrive.com/blog/spacedrive-v3-launch](https://spacedrive.com/blog/spacedrive-v3-launch)
