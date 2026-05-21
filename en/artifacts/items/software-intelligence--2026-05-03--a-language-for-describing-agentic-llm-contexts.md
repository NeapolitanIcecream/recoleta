---
source: arxiv
url: https://arxiv.org/abs/2605.01920v1
published_at: '2026-05-03T15:02:44'
authors:
- Noga Peleg Pelc
- Gal A. Kaminka
- Yoav Goldberg
topics:
- llm-agents
- context-engineering
- prompt-architecture
- multi-agent-systems
- agent-documentation
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# A Language for Describing Agentic LLM Contexts

## Summary
ACDL is a descriptive language for specifying how LLM agent contexts are assembled and how they change over time. It targets clearer comparison, reproduction, and team communication for agent systems.

## Problem
- Agent papers and code often describe context construction with prose, ad hoc diagrams, or implementation details, which leaves key prompt-history behavior ambiguous.
- This matters because context layout affects agent behavior, including which messages, tool outputs, reasoning traces, and prior turns the LLM sees at each step.
- Reproducing or comparing agent systems is hard when papers do not state how state and history are mapped into LLM inputs.

## Approach
- ACDL describes the context window as a sequence of role messages and information pieces, using symbolic labels instead of exact prompt wording.
- It tracks time-indexed state such as `env.user_input[@T]`, system state such as `sys.conf.role`, and prior model responses through `resp` references.
- It supports conditions, loops, named expressions, fragments, nested time steps, and multi-agent contexts.
- The language stays descriptive: it specifies what the LLM receives, not how tools, retrieval, memory, or agent control logic work.
- The paper also provides visual diagrams, a parser, an interactive renderer, a VS Code plugin, examples, and an agentic skill.

## Results
- The excerpt provides no quantitative benchmark table, dataset score, or measured baseline comparison.
- The paper shows 3 ReAct loop variants where ACDL makes differences visible: base ReAct, no reasoning traces in action history, and query-based tool selection with tools placed later in the context.
- ACDL models 4 common LLM API message roles: system, user, assistant, and tool.
- The language supports nested time steps such as `@T.I`, which lets one specification describe outer chat turns and inner ReAct tool-use steps.
- The claimed concrete output is a usable specification language plus 4 pieces of tooling: parser, renderer, VS Code plugin, and agentic skill.

## Link
- [https://arxiv.org/abs/2605.01920v1](https://arxiv.org/abs/2605.01920v1)
