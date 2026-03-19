---
source: hn
url: https://divanv.com/post/server-side-tool-gating/
published_at: '2026-03-15T22:36:22'
authors:
- divanvisagie
topics:
- mcp
- tool-selection
- tool-gating
- agent-infrastructure
- context-optimization
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Giving MCP servers a voice in tool selection

## Summary
This article proposes a lightweight improvement for MCP (Model Context Protocol) tool selection: allowing the server to participate in per-turn tool filtering through a conventionally named `_tool_gating` tool. Its goal is to reduce irrelevant tools entering the prompt, lower the probability of incorrect selection, and directly skip model invocation in deterministic command scenarios.

## Problem
- MCP servers can currently only register tools and provide schemas, but **cannot influence how the model selects tools**; as a result, irrelevant tools are also loaded into the context, wasting tokens and increasing the risk of incorrect selection.
- As the number of tools grows, LLM tool selection accuracy drops significantly; the article cites research saying that **performance degrades notably beyond about 20 tools**, and that the naive baseline where **all tools are loaded can have accuracy as low as about 14%**.
- This matters because in a multi-server MCP ecosystem, the number of tools can grow rapidly; the author gives the example of a weather MCP adding **20,000 tokens** of extra context, which is both expensive and slows responses.

## Approach
- The core mechanism is very simple: the server exposes a conventionally named tool **`_tool_gating`**; if the client discovers it in `tools/list`, it calls it **on every request, before constructing the tool list sent to the model**.
- `_tool_gating` returns two kinds of decisions: **`exclude`** (remove certain tools from the model context for this turn) and **`claim`** (the server declares that the request should be handled directly by a certain tool, allowing the client to **skip the model** and call that tool directly). Tools not mentioned are treated as `include` by default.
- This approach **does not require changes to the MCP spec** and **does not require a capability flag**; it relies only on the existing tool mechanism and a small amount of client-side logic changes.
- In the author's prototype implementation, the server side uses **simple keyword/pattern-based rules** rather than ML: for example, exact matches for `/projects` and `/list` are claimed directly; when read-only intent is detected, it excludes `notes_write`, `notes_edit`, and `project_new`; when there is no archive intent, it excludes `project_archive`.
- The client flow is: detect `_tool_gating` at connection time; on each turn, first request decisions from all servers that support gating; if there is a `claim`, call the tool directly and return; otherwise, apply `exclude` filtering to the tool list before sending it to the model. If a claim fails, it can still fall back to the normal LLM path.

## Results
- The author prototyped and validated this on their Python MCP server **pman-mcp** and Rust client **chell**; in **read-only request** scenarios, it can **remove 4 tools** from the candidate set on each turn.
- This filtering yields savings of about **318 tokens/turn**, which is the direct measured number given in the article.
- For slash commands (such as `/projects` and `/new ...`), the system can use the **claim** mechanism to **avoid calling the model entirely**, completing the command in a more deterministic, lower-latency way; the article does not provide specific latency numbers.
- The author considers this a “small but steady” optimization, but argues that if adopted by more tools and clients, the potential benefit could scale to **thousands or even millions of tokens saved**; this is a forward-looking claim, and **no systematic large-scale experimental data is provided**.
- Compared with approaches such as OpenAI Agents SDK `tool_filter`, Google ADK, Portkey embedding-based filter, and STRAP megatools, the strongest concrete claim of this article is that **filtering decisions should be made as much as possible on the server side, which best understands tool capabilities, rather than being placed entirely in the client or external frameworks**.

## Link
- [https://divanv.com/post/server-side-tool-gating/](https://divanv.com/post/server-side-tool-gating/)
