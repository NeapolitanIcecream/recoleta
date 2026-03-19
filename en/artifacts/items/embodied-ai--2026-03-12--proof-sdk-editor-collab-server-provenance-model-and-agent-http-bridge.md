---
source: hn
url: https://github.com/everyinc/proof-sdk
published_at: '2026-03-12T23:20:13'
authors:
- azhenley
topics:
- collaborative-editing
- markdown-editor
- provenance-tracking
- agent-interface
- realtime-server
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Proof SDK: Editor, collab server, provenance model, and agent HTTP bridge

## Summary
Proof SDK is an open-source collaborative document infrastructure that provides an editor, real-time collaboration service, provenance tracking model, and an agent-facing HTTP bridge interface. Its goal is to support collaborative Markdown document editing and allow external agents to read state, submit edits, and interact through events.

## Problem
- There is a need for an embeddable collaborative document system that supports real-time multi-user editing as well as workflows such as comments, suggestions, and rewrites.
- Traditional editors or collaboration backends often lack **provenance tracking** (tracking edit sources and change history), which affects auditing, collaboration transparency, and agent participation.
- To let AI/agents participate directly in document collaboration, stable public interfaces are needed to access document state, marks, presence, and events.

## Approach
- Provide an open-source SDK containing four core parts: a collaborative Markdown editor, a real-time collaboration server, a provenance model, and an agent HTTP bridge.
- Expose document lifecycle and collaboration capabilities through public HTTP routes, such as creating documents, fetching state/snapshot, submitting edit/ops, syncing presence, and handling events.
- Provide dedicated bridge interfaces for agents so they can read document state and marks, and submit operations such as comments, suggestions, and rewrite.
- Implement the system through modular packages (such as `doc-core`, `doc-editor`, `doc-server`, `doc-store-sqlite`, and `agent-bridge`), along with an example app for local deployment and integration.

## Results
- The text **does not provide quantitative experimental results**, and includes no dataset, baseline methods, or performance metric comparisons.
- The strongest concrete outcome claim is the release of a runnable open-source system covering four core capabilities: editor, collab server, provenance model, and agent HTTP bridge.
- The public SDK surface lists multiple canonical routes supporting document state, snapshot, editing, ops, presence, pending events, ack, and under bridge: state/marks/comments/suggestions/rewrite/presence.
- In terms of practical deployability, it requires Node.js 18+ and can be started locally via `npm run dev` and `npm run serve`, with the editor defaulting to port `3000` and the API/server to port `4000`.

## Link
- [https://github.com/everyinc/proof-sdk](https://github.com/everyinc/proof-sdk)
