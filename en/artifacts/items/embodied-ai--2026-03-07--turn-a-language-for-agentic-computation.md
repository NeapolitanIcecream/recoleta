---
source: arxiv
url: http://arxiv.org/abs/2603.08755v1
published_at: '2026-03-07T09:10:09'
authors:
- Muyukani Kizito
topics:
- agentic-programming-language
- llm-systems
- actor-model
- type-safety
- capability-security
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Turn: A Language for Agentic Computation

## Summary
Turn introduces a compiled language for “agentic computation,” turning LLM inference, context management, persistent state, and credential security into language primitives rather than relying on framework conventions. Its goal is to improve engineering control over the reliability, security, and recoverability of LLM-based autonomous software.

## Problem
- Existing Agent frameworks in Python/TypeScript and similar ecosystems typically treat **context boundaries, structured output, persistent execution, unified state representation, and credential isolation** as application-layer conventions, which are prone to failure.
- This leads to five common failure modes: unbounded context growth with silent truncation, no type guarantees for LLM output, fragmented state, inability to resume long-running tasks from checkpoints, and possible leakage of credentials such as API keys to the model.
- This matters because agentic programs delegate critical decisions to probabilistic LLMs; if these boundaries are not enforced at the language level, systems become unreliable and insecure at scale.

## Approach
- The core mechanism is to make **LLM inference a typed language primitive**: `infer T { prompt }`. The compiler automatically generates a JSON Schema from `struct T`, and the runtime VM validates the model output; only validated output is bound as type `T`.
- It introduces a **confidence operator**, extracting the model’s confidence as a `[0,1]` scalar for deterministic branching, such as falling back to local logic when confidence is below a threshold.
- It adopts an **actor-based process model**: each agent process has an isolated context window, persistent memory, and mailbox, and supports `suspend/resume`-style durable execution and checkpoint recovery.
- It designs a **three-layer structured context** (P0 system, P1 work, P2 episodic), explicitly placing system instructions at the high-recall beginning and recent content at the high-recall end, avoiding context pollution caused by shared message lists.
- It uses a **capability-based identity system** and **compile-time schema absorption**: `grant identity` returns an unforgeable, non-stringifiable credential handle, and `use schema::<protocol>` generates typed bindings from external API specifications at compile time.

## Results
- The paper provides a **formal correctness claim**: if `infer T { e }` completes successfully after at most `k=3` retries, then the bound value is structurally consistent with the declared `struct T`; this is the core guarantee of “typed LLM output,” though it is not a traditional task-accuracy metric.
- The context architecture specifies explicit capacity limits: the P1 workspace is capped at `W=100` items, the P2 episodic area at `2W=200` items, and rendering is fixed in `P0 -> P2 -> P1` order to exploit the attention-position differences cited in the paper (about `90%` recall at the beginning, `85%` at the end, and about `50%` in the middle).
- The example “investment committee” program in the paper is only **89 lines**, includes 3 concurrent committee-member actors, and has the analyst take a deterministic fallback branch when `confidence < 0.7`, demonstrating how the language primitives compose.
- The paper claims evaluation on “representative agentic workloads” and reports a Rust bytecode VM, an open-source repository, and an `openapi` adapter; however, the provided excerpt **does not include complete quantitative comparison results on standard benchmarks** (such as success rate, latency, cost, or numerical comparisons with baselines like LangChain).

## Link
- [http://arxiv.org/abs/2603.08755v1](http://arxiv.org/abs/2603.08755v1)
