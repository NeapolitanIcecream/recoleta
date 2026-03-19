---
source: arxiv
url: http://arxiv.org/abs/2603.11104v1
published_at: '2026-03-11T10:03:57'
authors:
- Jan Baumeister
- Bernd Finkbeiner
- Florian Kohn
topics:
- runtime-verification
- stream-monitoring
- refinement-types
- cyber-physical-systems
- parameterized-streams
relevance_score: 0.22
run_id: materialize-outputs
language_code: en
---

# Type-safe Monitoring of Parameterized Streams

## Summary
This paper safely integrates parameterized streams into the real-time stream monitoring language RTLola to handle an unbounded number of dynamic objects, while aiming to ensure that the monitor does not encounter runtime errors due to invalid memory accesses. The core contributions are a refinement type system for reasoning about time points and a clarification of the decidability boundary for “absence of runtime errors.”

## Problem
- Runtime monitoring must handle **unbounded data domains**, such as an unrestricted number of airspace participants around an unmanned aircraft, which requires dynamically creating, accessing, and reclaiming monitoring state.
- If dynamic data structures or asynchronous/real-time stream combinations are used directly, monitoring specifications may incur **runtime memory errors** when reading non-existent stream values, historical values, or already closed instances.
- For such specifications with parameterized streams and real-time clocks, it is not easy to fully guarantee at static analysis time that they will “never fail”; the paper explicitly states that this problem is **undecidable in general**, which affects the trustworthy deployment of safety-critical CPS monitoring.

## Approach
- Introduces **parameterized streams** into RTLola: a stream is no longer just a single sequence, but a set of stream instances distinguished by parameters and dynamically managed at runtime via `spawn / eval / close`, providing a systematic way to manage unbounded object collections.
- Provides the **formal semantics** of such parameterized streams in RTLola, precisely defining when an instance is alive, when it is accessible, and how prefixes, windows, and historical values are obtained.
- Designs a **refinement type system** whose key idea is not only to record what type a stream has, but also to track **at which time points it is guaranteed to have a value**; Boolean stream conditions are then used to refine these time points, enabling checks of whether synchronous access, hold, offset, aggregation, and similar operations are safe.
- The type system guarantees that every memory/stream-value access is either statically proven to succeed or has a **default value** as a fallback in the expression, so it will not fail at runtime due to missing values.
- The paper also extends the definition of **well-formedness** to avoid monitor nondeterminism and implements an **over-approximate** type analyzer for this method in the RTLola framework.

## Results
- Theoretical result: the paper proves that for parameterized-stream RTLola specifications, generally guaranteeing the **absence of runtime errors is undecidable**; it therefore adopts a conservative but practical refinement type check.
- Safety claim: the authors claim that **well-typed** specifications can be monitored without runtime errors, because all accesses are either proven valid or protected by default values.
- Capability result: the method covers **asynchronous and real-time properties** that were difficult to express in prior parameterized-stream approaches, and can detect illegal-access problems in examples caused by the mismatch between a 1Hz trigger and `avg_distance(id)`.
- Engineering result: the authors implement type analysis in the RTLola-framework and evaluate its runtime performance and scalability on **aerospace-domain specifications** and **synthetic specifications**.
- Quantitative result: the provided excerpt **does not supply specific numerical metrics** (such as type-checking time, benchmark scale, relative baseline speedup/overhead, error-detection rate, etc.), so exact metric/dataset/baseline comparisons cannot be reported.

## Link
- [http://arxiv.org/abs/2603.11104v1](http://arxiv.org/abs/2603.11104v1)
