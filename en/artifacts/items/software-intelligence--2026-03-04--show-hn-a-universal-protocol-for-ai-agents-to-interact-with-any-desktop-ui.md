---
source: hn
url: https://github.com/computeruseprotocol/computeruseprotocol
published_at: '2026-03-04T23:15:00'
authors:
- k4cper-g
topics:
- ui-automation
- ai-agents
- accessibility-tree
- cross-platform-protocol
- llm-optimization
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Show HN: A universal protocol for AI agents to interact with any desktop UI

## Summary
CUP proposes a unified protocol that lets AI agents perceive and operate any desktop and mobile/Web UI in the same way. Its core value is to unify fragmented cross-platform accessibility tree representations, action semantics, and agent integration methods, while applying aggressive compression for LLM context usage.

## Problem
- UI accessibility interfaces are fragmented across platforms: Windows UIA, macOS AXUIElement, Linux AT-SPI2, Web ARIA, Android, and iOS all use different role systems and property representations.
- As a result, every agent framework must repeatedly implement its own translation layer from “platform UI → agent-understandable representation,” making reuse difficult and preventing cross-platform agent logic from being written once and run everywhere.
- For LLMs, raw JSON/UI trees are too verbose, and complex interfaces can easily exceed context windows, limiting real desktop automation and intelligent interaction capabilities.

## Approach
- Define a general JSON envelope/schema that normalizes native accessibility trees captured from different platforms into the same structure, including fields such as app, screen, tree, role, state, action, and bounds.
- Use 59 ARIA-derived roles, 16 state markers, and 15 canonical action verbs as a unified cross-platform semantic layer; SDKs then map these standard semantics to each platform’s native APIs.
- Provide an LLM-oriented compact text encoding that compresses the same UI tree from JSON into short text-line representations, aiming to significantly reduce token usage while minimizing information loss.
- Preserve native properties under `node.platform.*` to avoid information loss caused by normalization; at the same time, provide SDKs and MCP server support so agents like Claude and Copilot can directly access perception and execution capabilities.

## Results
- The paper/project claims the compact format is about **97% smaller** than JSON, making it more suitable for LLM/CUA context windows.
- It claims about **15x fewer tokens** relative to “the next closest format,” but the excerpt does not provide the specific baseline name, experimental setup, or a complete evaluation table.
- It unifies mappings across **6 platform categories**: Windows, macOS, Linux, Web, Android, and iOS.
- The protocol’s semantic scope includes **59** roles, **16** states, and **15** canonical actions for cross-platform interaction abstraction.
- It provides SDK and MCP server integration capabilities, supporting agents in directly capturing native UI trees and executing actions; however, the excerpt provides **no** quantitative results on task success rate, latency, agent benchmarks, or real desktop benchmarks.

## Link
- [https://github.com/computeruseprotocol/computeruseprotocol](https://github.com/computeruseprotocol/computeruseprotocol)
