---
source: hn
url: https://github.com/mavaali/daftari
published_at: '2026-07-13T23:51:16'
authors:
- mavaali
topics:
- agent-memory
- llm-agents
- knowledge-provenance
- multi-agent-systems
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Long term memory cortex for agents that maintains tensions

## Summary
Daftari is a local, portable memory system for LLM agents that stores structured Markdown records with provenance, version history, supersession links, and unresolved contradictions. Its central rule is that the vault may resolve claims only through recorded evidence, while agents propose changes and humans retain final judgment.

## Problem
- LLM agents lose context between sessions, and provider-managed memory ties durable records to a model vendor.
- Retrieval can rebuild answers from stale or conflicting fragments without showing which sources are current, grounded, or contested.
- Agents need reliable memory because they may act on stored information without independently checking it.

## Approach
- Store documents as Markdown with YAML frontmatter in a local Git-backed vault that remains readable, searchable, and portable across models and tools.
- Expose the vault through 27 MCP tools for reading, searching, writing, provenance receipts, tension tracking, edge management, staged actions, and human ratification.
- Preserve contradictions as tensions and allow supersession only when a real evidence edge identifies a newer source; curation reports problems but does not auto-fix them.
- Generate deterministic receipts containing source status, confidence, provenance, freshness, content hashes, supersession resolution, open tensions, and the Git revision used as the answer's time anchor.
- Add domain-specific curation, audit, sleep, court, witness, and as-of commands for stale-document queues, contradiction review, contributor track records, cross-repository link failures, and historical belief-state inspection.

## Results
- The implementation provides 27 MCP tools and supports local use with Claude Desktop, Claude Code, and agent SDKs; the default configuration makes no network calls.
- The coherence audit example scans 2 repositories and 47 documents, finding 2 broken cross-repository references, 3 directly stale documents, and 5 transitively stale documents.
- The witness scoring schedule assigns 3 points to high-stakes writes, 1 to medium-stakes writes, and 0 to low-stakes writes; claims corrected by rulings lose their stake, while claims maintained through a full TTL cycle earn credit.
- The system can import existing Obsidian or Markdown vaults without copying content, export and round-trip through Google's OKF format, and preserve Git-based historical views and blast-radius reports.
- The provided text reports no formal benchmark results, accuracy scores, latency measurements, or comparison against another memory system; its strongest evidence is the implemented feature surface and deterministic audit example.

## Link
- [https://github.com/mavaali/daftari](https://github.com/mavaali/daftari)
