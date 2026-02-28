# ADR 0013: Batch Content Writes and Multi-Type Reads in SQLite Repository

## Status
Accepted

## Context
`html_document` enrichment previously performed multiple per-item database reads and writes, each opening a new session and committing independently. Under higher item counts (and especially with parallelism), this increases overhead and raises the risk of SQLite write lock contention.

## Decision
Add repository primitives to (1) fetch the latest texts for multiple `content_type` values in one query and (2) upsert multiple text contents for an item with a single commit. The `html_document` enrichment path uses these primitives to reduce round trips and commits.

## Consequences
Enrichment becomes more efficient and more robust under bounded parallelism. The repository surface area grows slightly, but the new APIs remain coarse and content-hash based, preserving existing dedup semantics.

