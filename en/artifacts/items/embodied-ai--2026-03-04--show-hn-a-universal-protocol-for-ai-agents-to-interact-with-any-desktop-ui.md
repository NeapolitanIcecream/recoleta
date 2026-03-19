---
source: hn
url: https://github.com/computeruseprotocol/computeruseprotocol
published_at: '2026-03-04T23:15:00'
authors:
- k4cper-g
topics:
- desktop-ui-agents
- accessibility-tree
- cross-platform-protocol
- llm-optimization
- computer-use
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Show HN: A universal protocol for AI agents to interact with any desktop UI

## Summary
This work proposes the Computer Use Protocol (CUP), a cross-platform protocol that allows AI agents to perceive and operate any desktop/mobile/web UI in a unified way. Its core value is to unify fragmented accessibility tree representations, action semantics, and platform differences, while significantly reducing LLM context overhead with an extremely compact text format.

## Problem
- Existing UI accessibility interfaces across Windows, macOS, Linux, Web, Android, and iOS all differ, forcing each agent framework to repeatedly implement its own platform adaptation and translation layer.
- For AI agents, UI structures are typically provided in verbose formats such as JSON, which can easily fill the context window and limit perception and reasoning over complex interfaces.
- The lack of unified action semantics makes cross-platform execution fragile; without "write once, run anywhere," the desktop agent ecosystem is hard to scale.

## Approach
- Proposes a unified UI representation protocol: using an ARIA-based role system to normalize native accessibility trees from different platforms into the same JSON envelope.
- Designs an LLM-oriented compact text encoding that compresses the same UI tree into shorter readable text, making it easier for models to process complex interfaces within limited context.
- Defines a shared cross-platform semantic layer, including 59 standard roles, 16 state markers, and 15 canonical action verbs, which platform SDKs map to native API execution.
- To avoid information loss, preserves native platform attributes under `node.platform.*` alongside the unified representation, balancing standardization and traceability.
- Through SDKs and MCP server, directly exposes the capability to "capture UI trees + execute actions" for AI agents such as Claude and Copilot.

## Results
- Claims to achieve **one format covering 6 platform categories**: Windows, macOS, Linux, Web, Android, and iOS, enabling agent logic to be reused across platforms.
- Claims the compact format can achieve about **97% size/token reduction** relative to JSON, and after optimization for CUA/LLMs can use about **15x fewer tokens** than the "next-best approximate format."
- Provides clear protocol-level specifications: **59 roles**, **16 states**, and **15 canonical actions**, along with cross-platform role mapping and schema.
- The text does not provide standard academic benchmarks, datasets, or comparative experiments, so there are **no verifiable quantitative evaluation results** such as task success rate, latency, or accuracy.
- The strongest concrete claim is that it solves the cross-platform UI translation problem once through a unified representation layer, while significantly reducing the context cost of LLM UI processing without losing native attributes.

## Link
- [https://github.com/computeruseprotocol/computeruseprotocol](https://github.com/computeruseprotocol/computeruseprotocol)
