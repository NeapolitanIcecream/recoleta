---
kind: ideas
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
run_id: 0377f109-03bb-4fb5-8661-06b69442d995
status: succeeded
topics:
- coding agents
- repository repair
- tool calling
- program generation
- software quality
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repository-repair
- topic/tool-calling
- topic/program-generation
- topic/software-quality
language_code: en
pass_output_id: 129
pass_kind: trend_ideas
upstream_pass_output_id: 128
upstream_pass_kind: trend_synthesis
---

# Constrained coding agent interfaces

## Summary
Coding-agent teams can get concrete gains by moving terminal output, tool schemas, and repository evidence behind smaller, testable interfaces. The clearest adoption points are bounded command execution, compiled tool descriptions for long catalogs, and repository context tools that expose definition-use evidence before an agent edits code. Static API and type checks also deserve a place in generated-repository workflows because many failures are detectable before runtime tests.

## Bounded terminal-execution subagent for build and test runs
Coding-agent teams should route build, test, install, and diagnostic commands through a bounded terminal-execution subagent when raw logs are consuming the main agent’s context. The concrete build is small: the main agent sends a natural-language request, the subagent runs one synchronous terminal command per turn with timeouts, and it returns a structured summary containing command status, warnings, failing tests, and likely next actions.

Terminus-4B gives a practical template for this interface. In the reported Serilog example, the main-agent run fell from 2.46M tokens and 40 turns to 740k tokens and 32 turns while the subagent ran 9 commands internally. The summary sent back to the main agent was about 200 tokens and still included the `dotnet build` result, 769 passing unit tests, and one failing approval test with a likely fix. A team can test this on its own issue queue by replaying recent agent runs and comparing main-agent tokens, number of direct terminal calls, and patch success with and without the subagent.

### Sources
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): Summarizes Terminus-4B’s execution-subagent design, token reduction claims, and the Serilog example with command and test details.
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): Describes the context-window problem caused by terminal output and the need for concise summaries rather than raw shell logs.

## Tool-schema compilation for agents with long tool catalogs
Teams exposing 20 or more tools to a coding agent should test a tool-schema compiler at the API boundary. The build is a deterministic conversion step that turns existing JSON tool schemas into compact structured text before the model sees them, then keeps the downstream tool executor unchanged. The first evaluation should use the team’s current tool-call regression set and report tool selection accuracy, parameter accuracy, input tokens, and failures by model size.

TSCG is the concrete reference case. The paper reports about 19,000 calls across 12 models and claims large gains when catalogs grow. In the summary, conservative TSCG raises Mistral 7B from 35.0% to 80.0% accuracy at 20 tools and from 30.0% to 75.3% at 50 tools; Gemma 3 4B rises from 24.3% to 87.5% at 50 tools. The same work reports 52–57% token savings on heavy MCP schemas. This is most relevant for teams trying to run smaller local models or reduce repeated schema tokens in production agent calls.

### Sources
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): Reports TSCG’s problem statement, deterministic schema-compilation approach, benchmark size, model results, and token savings.
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): States that TSCG ships as a zero-dependency TypeScript package and reports production-style MCP schema savings.
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): Explains the API-boundary problem: JSON schemas consume thousands of repeated tokens and hurt small-model tool use.

## Definition-use slicing in repository repair agents
Repository repair agents need a context tool that can answer where a value is defined, used, and changed before the agent writes a patch. The concrete workflow is to index Python repositories into a graph with statement nodes and intra-procedural definition-use edges, then expose backward, forward, and bidirectional slices as a tool call. The agent can request a slice for a variable and statement, inspect the returned code context, and patch with less guessing around the relevant function or line.

ARISE shows why this is worth testing. On SWE-bench Lite with SWE-agent and Qwen2.5-Coder-32B-Instruct, it improved Function Recall@1 by 17.0 points and Line Recall@1 by 15.0 points over the unmodified baseline. It reached 22.0% Pass@1, fixing 66 of 300 issues, a 4.7 percentage-point gain. The ablation result matters for implementation: the data-flow graph drove the improvement, and the model could consume structured slice output directly without a natural-language summary layer.

### Sources
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): Summarizes ARISE’s graph design, slicing API, SWE-bench Lite setup, localization gains, and Pass@1 result.
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): Gives the reported Function Recall@1, Line Recall@1, Pass@1, ablation, and structured-output findings from the paper text.
