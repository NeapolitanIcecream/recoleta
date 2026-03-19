---
source: arxiv
url: http://arxiv.org/abs/2603.08755v1
published_at: '2026-03-07T09:10:09'
authors:
- Muyukani Kizito
topics:
- agent-programming-language
- llm-type-safety
- actor-model
- capability-security
- schema-driven-apis
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Turn: A Language for Agentic Computation

## Summary
Turn is a compiled language for "agentic computation" that makes LLM inference, context management, persistent state, and credential security into language primitives directly, rather than relying on framework conventions. The paper’s core claim is that many reliability and security problems in agent systems require language-level guarantees.

## Problem
- Existing Python/TypeScript/Rust + agent framework approaches leave **context boundaries, structured output, durable execution, state consistency, and credential isolation** to be maintained manually at the application layer, which is prone to failure.
- This matters because agent programs delegate critical decisions to **stochastic LLMs**; if outputs are not type-constrained, context is unbounded, and credentials are visible, errors can accumulate, systems can crash, or secrets can leak.
- The paper explicitly lists 5 failure modes: unbounded context, untyped inference output, fragmented state, lack of durable execution, and credential leakage.

## Approach
- It proposes **Turn, a compiled actor language**: dynamically typed at the value level, but with "targeted strictness" at high-risk boundaries.
- Using `infer Struct { prompt }`, it turns LLM inference into a **typed language primitive**: the compiler automatically generates a JSON Schema from the struct, and the runtime VM validates the model output; if binding succeeds, it structurally conforms to the declared type. On failure, it can retry up to **k=3** by default.
- Using `confidence v`, it exposes model confidence so programs can make **deterministic branches** based on thresholds; if the provider does not supply such a signal, it returns a default of **0.5**.
- Using an Erlang-based **actor process model**, it isolates each agent’s context, persistent memory, and mailbox, and supports durable execution with suspend/resume; the context uses a three-layer structure: P0 system, P1 working, P2 episodic, where P1 has a limit of **100** entries and P2 has a limit of **200** entries.
- Using `grant identity`, it provides **unforgeable, non-stringifiable, non-serializable** capability handles to isolate credentials; it also uses `use schema::<protocol>(...)` to absorb external API schemas at compile time and generate typed bindings.

## Results
- The paper provides **very limited quantitative experimental results**; the abstract says it was "evaluated on representative agentic workloads," but the excerpt provided here **does not give specific benchmark metrics, accuracy, latency, or ablation numbers**.
- The clearest formal/mechanistic result is that the paper claims and proves a structural conformance property: if an `infer` expression **completes without error**, then every field of the bound value conforms to the declared struct type.
- The context design cites attention phenomena from external research to support its motivation: in long contexts, information recall is about **90%** at the beginning, about **85%** at the end, and about **50%** in the middle; Turn uses the P0→P2→P1 rendering order to place critical content in high-recall positions.
- As for execution examples, the paper claims that an "investment committee" multi-agent program uses only **89 lines** to cover its 5 core language mechanisms, and demonstrates 3 specialized actors performing concurrent analysis, fallback based on a **0.7** confidence threshold, and I/O with scoped credentials.
- The paper also cites existing empirical evidence showing that agent reliability decreases exponentially with the number of loop iterations: if the single-step success rate is **0.95**, then after **20** steps the overall success rate is about **0.36**; Turn uses this as motivation for type boundaries and deterministic repair routing, rather than as an experimental improvement result of its own.

## Link
- [http://arxiv.org/abs/2603.08755v1](http://arxiv.org/abs/2603.08755v1)
