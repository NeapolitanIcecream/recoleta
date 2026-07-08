---
source: arxiv
url: https://arxiv.org/abs/2607.06195v1
published_at: '2026-07-07T12:21:42'
authors:
- Minghui Long
- Yanjie Zhao
- Haoyu Wang
topics:
- llm-agent-frameworks
- software-testing
- code-intelligence
- agentic-oracles
- automated-software-production
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle

## Summary
LogicHunter tests LLM agent frameworks by generating valid edge-case tests and using an agent oracle to judge whether failures are real bugs. It matters because LangChain, LlamaIndex, and CrewAI can fail through ordinary Python exceptions or silent wrong behavior that simple crash checks miss.

## Problem
- LLM agent frameworks rely on Pydantic schemas, type hints, async paths, callbacks, tools, memory, and external-service adapters, so random fuzzing often stops at invalid inputs before it reaches useful logic.
- Many defects appear as ValueError, KeyError, or assertion-like mismatches, and the same exception can come from valid rejection, API misuse, or a library bug.
- Existing test generators tend to create passing regression tests or noisy failures, so they miss semantic failures in production-facing agent infrastructure.

## Approach
- LogicHunter mines source code, type hints, Pydantic schemas, docstrings, and real repository usage to build executable seed tests and API profiles.
- A fixer agent runs generated seeds and repairs setup errors until the seed is executable.
- A mutator agent changes valid seeds at the API-usage level, adding behavioral probes for properties such as field preservation, idempotency, boundary behavior, and return-type consistency.
- A deterministic verification step executes tests, hashes duplicate failures, and removes cases whose stack traces point only to the test code.
- The Agentic Oracle uses a ReAct-style loop to retrieve documentation, inspect source, run reproduction scripts, and inspect runtime state before labeling an anomaly as a bug.

## Results
- On LangChain, LlamaIndex, and CrewAI, LogicHunter found 40 previously unknown bugs.
- Developers confirmed 30 of the 40 reported bugs.
- Developers fixed 26 bugs after the reports.
- The Agentic Oracle reached 91.17% precision.
- The best passive oracle reached 29.27% precision, so LogicHunter reports a 61 percentage-point gain.
- The tested state-of-the-art baselines reported 0 bugs as final findings.

## Link
- [https://arxiv.org/abs/2607.06195v1](https://arxiv.org/abs/2607.06195v1)
