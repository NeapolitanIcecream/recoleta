---
source: hn
url: https://github.com/everyinc/proof-sdk
published_at: '2026-03-12T23:20:13'
authors:
- azhenley
topics:
- collaborative-editor
- provenance-tracking
- agent-http-bridge
- realtime-collaboration
- human-ai-collaboration
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Proof SDK: Editor, collab server, provenance model, and agent HTTP bridge

## Summary
Proof SDK is an open-source collaborative document infrastructure that provides an editor, a real-time collaboration server, a provenance model, and an agent-facing HTTP bridge interface. It targets developers who need to connect human collaborative editing and intelligent agent operations within the same document workflow.

## Problem
- The problem it solves is how to unify **multi-user real-time document collaboration**, **edit history/provenance tracking**, and **AI/agent-programmable operations** within a single document system.
- This matters because in human-AI collaborative writing, code/document co-creation, and multi-agent workflows, the system must support not only editing but also auditable changes, comments, suggestions, and state synchronization.
- Traditional editors or collaboration backends usually lack a unified agent interface and provenance model, making it difficult to safely connect automation capabilities to collaborative documents.

## Approach
- The core approach is straightforward: split the collaborative document system into four composable parts—**editor**, **real-time collaboration server**, **provenance model**, and **agent HTTP bridge**.
- The editing layer supports collaborative Markdown editing and includes higher-level operations such as **comments, suggestions, and rewrite**, not just low-level text editing.
- The server exposes document state, snapshots, edit operations, presence, and event streams through a set of public HTTP routes, such as `/state`, `/snapshot`, `/edit`, `/ops`, and `/events/pending`.
- The agent-facing bridge separately exposes interfaces for state, marks, comments, suggestions, rewrite, and presence, allowing external agents to read documents and submit structured modifications over standard HTTP.
- The project also provides an example app and modular packages (such as `doc-editor`, `doc-server`, `agent-bridge`, and `doc-store-sqlite`) to make further integration easier.

## Results
- The text **does not provide quantitative results such as benchmarks, accuracy, throughput, latency, or user studies**.
- The strongest concrete claim is that the SDK publicly exposes a complete interface surface: at least **13 canonical routes**, covering document creation, state retrieval, snapshots, editing, ops, presence, events, and agent bridge capabilities.
- Functionally, it claims support for **4 core capability categories**: collaborative Markdown editing, provenance tracking, a real-time collaboration server, and an agent HTTP bridge.
- The agent-side interface covers at least **6 interaction categories**: state, marks, comments, suggestions, rewrite, and presence, which can support external automation or agent participation in document collaboration.
- From an engineering delivery perspective, the repository includes an example app (`apps/proof-example`) and multiple foundational packages, requires **Node.js 18+**, and can launch the full system locally with the editor on `:3000` and the API/server on `:4000`.

## Link
- [https://github.com/everyinc/proof-sdk](https://github.com/everyinc/proof-sdk)
