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
- ai-agents
- microservice-generation
- code-generation
- software-engineering
- empirical-study
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Can AI Agents Generate Microservices? How Far are We?

## Summary
This paper systematically evaluates the real capabilities of AI coding agents in microservice generation: they can already generate many runnable and relatively maintainable microservices, but there is still a clear gap before achieving "fully automated development without human supervision."

## Problem
- The paper addresses the question: can AI agents generate microservices that are **functionally correct and integrable**, rather than just individual functions or scattered code snippets.
- This matters because microservice development requires not only correct local business logic, but also compliance with cross-service API contracts, dependencies, and project structure; small errors can cause system integration to fail.
- Existing evaluations of agents mostly focus on bug fixing or repository-level tasks, while systematic empirical studies on "from requirements to microservice implementation" remain rare.

## Approach
- The authors designed an empirical study evaluating **144 generated microservices**, covering **3 agents, 4 projects, 2 prompting strategies, and 2 generation scenarios**.
- The two scenarios are: **incremental generation** (rebuilding the target service after deleting it from an existing system, while retaining context and tests) and **clean state generation** (starting only from requirements, removing the service implementation and traces of related calls).
- The two prompting strategies are: **P1 minimal prompt** (service name + requirements path) and **P2 detailed prompt** (additionally providing a summary of the target service implementation), used to measure how different forms of contextual information affect results.
- Functional correctness is measured with automated tests: the incremental scenario uses **unit test pass rate**, while the clean state scenario uses the **integration test pass rate** of tests depending on that service; code quality is compared against human baselines using **SLOC, cyclomatic complexity, and cognitive complexity**.
- Efficiency metrics are also compared, including **token usage, cost, and generation time**, and differences are tested using statistical methods such as Anderson-Darling and Wilcoxon/Dunn.

## Results
- In **incremental generation**, the **minimal prompt P1 actually outperformed the more detailed P2**, with unit test pass rates of about **50%–76%**; this suggests that providing more summarized context does not necessarily improve microservice reconstruction.
- In **clean state generation**, integration test pass rates were higher, reaching **81%–98%**; this indicates that when generating from requirements alone, agents can often comply well with the **API contract** and satisfy cross-service interaction requirements.
- In terms of code quality, the generated code had **lower complexity than the human baseline**; based on this, the paper argues that the generated results are overall easier to maintain, while also noting that lower complexity may partly result from missing defensive programming.
- In terms of efficiency, generation time varied greatly across agents, averaging about **6–16 minutes** per microservice; the paper also compares token usage and cost, but the excerpt does not provide more detailed figures.
- The paper’s core conclusion is that AI agents **can already generate working microservices**, but functional correctness remains unstable and still depends on human oversight, so **fully autonomous microservice generation is not yet achievable**.
- The excerpt does not provide finer-grained complete quantitative comparisons across agents, specific baseline values, or tables of significance test results, so the strongest quantitative conclusions mainly come from the pass-rate ranges and time range above.

## Link
- [http://arxiv.org/abs/2603.09004v1](http://arxiv.org/abs/2603.09004v1)
