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
- agent-inference
- token-efficiency
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Giving MCP servers a voice in tool selection

## Summary
This article proposes a "server-side tool gating" mechanism for MCP, allowing the server to participate in filtering or directly claim tool calls before each request is processed, thereby reducing contextual noise, saving tokens, and lowering the probability that the model selects the wrong tool.

## Problem
- Although MCP servers understand their own tool capabilities best, in the traditional flow tool selection is done entirely by the model "guessing" from tool descriptions, and the server itself cannot participate in routing decisions.
- As the number of tools grows, loading all tools into the prompt significantly increases token overhead and reduces tool selection accuracy; the article cites research saying that beyond about 20 tools, the naive "load everything" baseline can fall to around **14%** accuracy.
- Some servers have very large toolsets; for example, one weather MCP adds about **20,000 tokens**, creating clear cost and misrouting problems.

## Approach
- The article proposes a solution that requires no changes to the MCP specification: the server exposes a conventional tool called **`_tool_gating`**, and if the client detects it, it calls it before each request and before constructing the tool list shown to the model.
- The server returns a small set of "exception rulings": **exclude** means removing certain tools from the model context for the current turn; **claim** means the server asserts that it should handle the request directly, allowing the client to skip the model and call the target tool directly.
- This mechanism puts filtering intelligence back in the hands of "the party that understands the tools best"—the server side—rather than relying only on client SDKs, external embedding filters, or megatool consolidation strategies.
- The author's implementation uses very simple rule-based logic rather than machine learning: keyword/prefix matching determines which commands can be directly claimed, and which write-related tools should be excluded under read-only intent; when uncertain, tools are kept by default.
- The client-side changes are minimal: detect `_tool_gating` on connection and hide it from the LLM; on each turn, first query all servers that support gating, then either execute direct calls or apply per-turn filtering to the tool list; if a claim fails, fall back to the normal LLM path.

## Results
- In the author's test environment, by adding one gating tool and modifying the client's pre-call logic, **4 tools** could be removed from the context for read-only-related requests.
- In testing, this change produced savings of about **318 tokens/turn**.
- For slash commands (such as deterministic imperative requests), the approach can **skip model invocation entirely**, replacing the LLM turn with a direct tool call.
- The article does not provide a standard dataset, systematic benchmarks, A/B experiments, or significance testing results, so there is **no rigorous general quantitative evaluation**.
- The strongest concrete claim is that this approach **requires no changes to the MCP specification** and only "one conventional tool + a small amount of client logic" to reduce prompt burden, lower misselection risk, and potentially save "**thousands to millions of tokens**" if adopted more broadly.

## Link
- [https://divanv.com/post/server-side-tool-gating/](https://divanv.com/post/server-side-tool-gating/)
