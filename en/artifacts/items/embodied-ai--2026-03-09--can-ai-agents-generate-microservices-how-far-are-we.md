---
source: arxiv
url: http://arxiv.org/abs/2603.09004v1
published_at: '2026-03-09T22:48:41'
authors:
- Bassam Adnan
- Matteo Esposito
- Davide Taibi
- Karthik Vaidhyanathan
topics:
- llm-code-generation
- ai-agents
- microservices
- software-engineering
- benchmarking
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Can AI Agents Generate Microservices? How Far are We?

## Summary
This paper evaluates whether AI coding agents can automatically generate runnable microservices, and systematically compares the effects of different contexts and prompting strategies. The conclusion is: agents can already generate relatively maintainable microservice code, but correctness remains unstable, and fully autonomous development is still some distance away.

## Problem
- The problem addressed by the paper is whether AI agents can generate microservices that satisfy dependency relationships, API contracts, and system integration requirements, rather than just individual functions or files.
- This matters because microservice development must ensure both **correct local business logic** and **cross-service interface compatibility**; even small errors can cause communication failures across the entire system.
- Existing research on LLM code generation has mostly focused on function-level tasks, bug fixing, or repository-level modifications, while the more realistic engineering problem of "end-to-end microservice generation" remains underexplored.

## Approach
- The authors designed an empirical evaluation: a total of **144** microservice implementations were generated, covering **3 agents**, **4 projects**, **2 prompting strategies**, and **2 generation scenarios**.
- The two scenarios are: **incremental generation** (removing the target service from an existing system and asking the agent to fill it back in, while preserving context and tests) and **clean state generation** (generating from an almost blank state based only on requirements).
- The two prompting strategies are: **P1 minimal prompt** (service name + requirements path) and **P2 detailed prompt** (plus an implementation summary), used to study whether “more context is really better.”
- Evaluation dimensions include: **functional correctness** (unit test pass rate for incremental, integration test pass rate of dependent services for clean state), **code quality** (SLOC, cyclomatic complexity, cognitive complexity), and **efficiency** (tokens, cost, generation time).
- In the simplest terms, the core mechanism is: let different AI coding agents “write a complete microservice” under different contextual conditions, then use automated tests and code quality metrics to judge whether what they wrote is correct, good, and worth it.

## Results
- In **incremental generation**, the **minimal prompt P1 actually outperformed the more detailed P2**, with unit test pass rates of about **50%–76%**, suggesting that existing codebase context is usually sufficient and extra summaries may not help.
- In **clean state generation**, integration test pass rates were higher, reaching **81%–98%**, indicating that when relying only on requirements, agents can often still follow the **API contract** well and complete cross-service integration.
- The complexity of the generated code was **lower than the human baseline**: the paper explicitly claims that AI-generated code scored lower on complexity metrics, suggesting it may be easier to maintain; however, the authors also caution that such “low complexity” does not necessarily mean greater robustness, and may instead reflect missing defensive handling.
- In terms of efficiency, there were clear differences across agents, with average generation time per microservice of about **6–16 minutes**; the paper also recorded tokens and cost, but the excerpt does not provide more detailed breakdown values.
- In terms of dataset and experimental scale, the study covered **4 formal projects** (plus **1 pilot project**), with **3 microservice tasks** per project and **144 total generation experiments**, making it, according to the authors, the first systematic evaluation of agents for microservice generation.
- The overall conclusion is: AI agents can already generate microservices that are “partially workable,” and they show good API contract compliance and maintainability, but because correctness is inconsistent and human supervision is still required, **fully autonomous microservice generation is not yet possible**.

## Link
- [http://arxiv.org/abs/2603.09004v1](http://arxiv.org/abs/2603.09004v1)
