---
source: arxiv
url: http://arxiv.org/abs/2604.04806v2
published_at: '2026-04-06T16:10:23'
authors:
- XinRan Zhang
topics:
- microservice-testing
- llm-based-simulation
- integration-testing
- code-intelligence
- stateful-mocking
relevance_score: 0.79
run_id: materialize-outputs
language_code: en
---

# MIRAGE: Online LLM Simulation for Microservice Dependency Testing

## Summary
Mirage tests microservices by having an LLM answer dependency requests at runtime instead of replaying fixed traces or using prebuilt mocks. The paper shows that this online simulation matches real dependency behavior much more closely than record-replay on three benchmark systems.

## Problem
- Microservice integration tests need downstream services with the right behavior, state, and error handling, but real dependencies are often unavailable or expensive to run.
- Existing substitutes are static: record-replay, mined patterns, and spec-based stubs must encode behavior before the test starts, so they miss unseen inputs, multi-step state changes, and code-level edge cases.
- In the paper’s held-out scenarios, record-replay reached only 62% status-code fidelity and 16% response-shape fidelity, which means many tests would exercise the caller against unrealistic dependency behavior.

## Approach
- Mirage keeps the LLM in the request path during testing. For each incoming HTTP request, the model reads the request, uses prior conversation history as cross-request state, and returns a JSON response with status, body, and optional headers.
- The prompt can include dependency source code, caller source code, and summarized production traces. In white-box mode it uses all three; in black-box mode it uses caller code and traces only.
- Before each scenario, Mirage receives the planned sequence of HTTP methods and paths so it can prepare for a multi-step flow without seeing the expected answers.
- The key mechanism is simple: instead of generating a mock server ahead of time, the LLM simulates the dependency on demand and remembers what happened earlier in the scenario.
- The system runs as a FastAPI mock server, keeps the last 20 exchanges of history, retries once on invalid JSON, and resets state between scenarios.

## Results
- Across 110 scenarios, 14 caller-dependency pairs, and 3 systems, Mirage in white-box mode achieved 99% status-code fidelity and 99% response-shape fidelity, equal to 109/110 scenarios for status and 99% for body shape.
- Record-replay reached 62% status fidelity and 16% response-shape fidelity on the same benchmarks. On Demo, pattern-mining reached 61% and Contract IR reached 55%.
- In black-box mode, Mirage still achieved 94% status fidelity (103/110) and 75% response-shape fidelity (82/110), showing that source code improves structural accuracy more than status prediction.
- End-to-end caller integration tests had the same pass/fail outcomes with Mirage and with real dependencies in 8/8 checked scenarios.
- Signal ablations found that dependency source code alone was often enough for full fidelity on their tests: 100% by itself. Without dependency source, Mirage still got 94% status fidelity but only 75% body-shape fidelity. Traces-only reached 92% status and 53% body-shape fidelity.
- Typed intermediate representations hurt on complex services: Contract IR got 55% on Demo, and only 29% on Demo stateful scenarios, while Mirage reached 100% there. On a simpler OB product-catalog subset, IR reached 86% versus Mirage’s 100%. The reported cost was $0.16-$0.82 per dependency, with results within 3% across three LLM families.

## Link
- [http://arxiv.org/abs/2604.04806v2](http://arxiv.org/abs/2604.04806v2)
