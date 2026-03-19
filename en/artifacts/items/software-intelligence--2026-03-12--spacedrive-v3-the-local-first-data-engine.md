---
source: hn
url: https://spacedrive.com/blog/spacedrive-v3-launch
published_at: '2026-03-12T22:57:04'
authors:
- raybb
topics:
- local-first
- data-engine
- agent-memory
- prompt-injection-defense
- vector-search
- rust
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Spacedrive v3: The local-first data engine

## Summary
Spacedrive v3 is a local-first data engine aimed at unifying indexing and search across multi-source personal/team data without moving the original data. Its core value proposition is not file management, but performing local security screening, quality classification, and trust tiering on data before AI uses it.

## Problem
- Traditional cross-platform file manager products have too broad a surface area, involving file semantics, permissions, thumbnails, drag-and-drop, and more across multiple operating systems, making stable delivery difficult.
- Existing local data tools often send raw content directly into LLM/Agent context, lacking preprocessing for prompt injection and low-quality noisy content.
- Users want unified search across email, notes, bookmarks, calendars, contacts, GitHub, Slack, coding sessions, and other data while maintaining local control and privacy boundaries, which is especially important for AI scenarios.

## Approach
- Model each data source as a repository: the raw data stays where it is, and Spacedrive only maintains the corresponding SQLite database and vector index for that source to enable unified retrieval.
- Before entering the search index, each record goes through a four-stage processing pipeline: security screening, content classification, adapter-specific processing, and search indexing.
- In the security screening stage, Meta's Prompt Guard 2 runs locally on CPU, isolating injected content and attaching security metadata to borderline samples; in the content classification stage, records receive quality scores, noise labels, and category labels, which affect search ranking and Agent visibility.
- Through repository trust tiers and visibility controls, data sources are divided into trust levels such as authored/collaborative/external, and support private/shared/agent-excluded to restrict Agent cross-source access.
- The system architecture is a pure Rust core library built on SQLite, LanceDB, FastEmbed, BLAKE3, and more, running locally as a single binary; it connects 11 types of data sources through script-like adapters and integrates directly with Spacebot as a crate.

## Results
- The article does not provide quantitative experimental results on standard academic benchmarks for retrieval, classification, or Agent security, nor does it offer a unified benchmark comparison with other systems.
- The explicitly stated performance figure is: Prompt Guard 2 local CPU inference takes **less than 50ms per chunk**, used for pre-indexing injection screening.
- At launch it supports **11 adapters**: Gmail, Apple Notes, Chrome Bookmarks, Chrome History, Safari History, Obsidian, OpenCode, Slack Export, macOS Contacts, macOS Calendar, and GitHub, and it supports UTC-normalized dates and incremental sync cursors.
- Signals of engineering scale and maturity: about **183k lines of Rust** in the core implementation (referring to the v2 architectural background), and the current architecture includes **68 tests**; historically the project has accumulated **37,000 GitHub stars**, **600,000 downloads**, and **$2M seed**, indicating strong demand validation but not technical-effect benchmark results.
- Compared with v1/v2, the author claims v3's breakthrough is focusing on the “searchable data indexing layer” rather than cross-platform file management/real-time sync, and making injection protection, content classification, and trust tiering first-class capabilities rather than optional add-ons.

## Link
- [https://spacedrive.com/blog/spacedrive-v3-launch](https://spacedrive.com/blog/spacedrive-v3-launch)
