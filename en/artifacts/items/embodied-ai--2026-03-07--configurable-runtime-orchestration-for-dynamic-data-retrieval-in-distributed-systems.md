---
source: arxiv
url: http://arxiv.org/abs/2603.06980v1
published_at: '2026-03-07T01:45:18'
authors:
- Abhiram Kandiraju
topics:
- distributed-systems
- workflow-orchestration
- microservices
- runtime-configuration
- data-retrieval
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Configurable Runtime Orchestration for Dynamic Data Retrieval in Distributed Systems

## Summary
This paper proposes a **configuration-driven framework that dynamically generates execution graphs at request time** for orchestrating distributed data retrieval, targeting low-latency aggregation scenarios across enterprise microservices, APIs, and analytical platforms. Its core value is that when integrations change frequently, the orchestration topology can be adjusted without redeploying workflow code.

## Problem
- Existing orchestration systems (such as Airflow, Step Functions, and Temporal) typically require **predefined** DAGs, state machines, or code-based workflows, making them unsuitable for retrieval topologies that may **change on every request**.
- Enterprise scenarios such as “Customer 360” often need to access multiple microservices, external APIs, and analytical platforms at once; relying on serial calls or frequent code redeployments leads to **high latency and high operational friction**.
- This problem matters because responses in modern distributed systems often depend on **on-demand aggregation of multi-source data**; when upstream services, dependencies, and optional data sources continue to evolve, the orchestration layer must balance flexibility, correctness, performance, and maintainability.

## Approach
- The core idea is to treat **configuration**, rather than a predefined workflow, as the “source of truth.” When a **request arrives**, the system reads declarative configuration, dynamically constructs a dependency graph, and then executes it.
- The architecture has five layers: Request Adapter, Configuration Resolver, Execution Planner, Execution Engine, and Aggregation/Response. They are responsible for receiving requests, resolving configuration, generating the dependency graph, scheduling parallel execution, and aggregating the returned results.
- The execution model is straightforward: each node represents a call or transformation, and each edge represents a dependency; **nodes with no unsatisfied dependencies immediately enter the ready queue and execute concurrently**, automatically exposing and exploiting parallelism.
- Failure semantics are explicitly modeled as **required / optional / fallback** nodes, so under strict latency constraints, the system can return **partial but still valid** results rather than pursuing the kind of “guaranteed completion” expected from long-running durable workflows.
- When adding a new data source or modifying dependencies, only the configuration needs to change (for example, adding a “recent-case context” node and its dependency/aggregation rules), without republishing orchestration code.

## Results
- The paper’s main contribution is an **architectural and mechanistic statement**, rather than a rigorous experimental evaluation on public benchmarks; **the paper does not provide quantitative results, performance tables, or numerical metrics** (such as percentage latency reduction, throughput gains, or dataset scores).
- In the case study, a Customer 360 request can be planned into **4 immediately executable parallel nodes**: account, transactions, fraud, and risk; if a **5th optional data source** is later added, the system claims it can be incorporated into the runtime execution graph simply by updating configuration.
- In comparison with Airflow / Step Functions / Temporal, the paper claims its approach is stronger on the dimension of **request-level topology changes without redeployment**, whereas the traditional systems are more oriented toward predefined DAGs, state machines, or durable code-defined workflows.
- The strongest concrete performance claim is that the overhead of generating the graph at runtime is usually **smaller than the cost of network-bound retrieval**, and that the benefits mainly come from two sources: **dependency-aware parallel execution** and **decoupling orchestration from deployment**; however, the paper does not provide specific evidence in milliseconds or percentages.
- Therefore, this paper is better understood as a **systems design / architectural position paper**: its key contribution is shifting from “workflow definitions specified in advance” to “execution graphs derived from configuration per request,” rather than proposing a new algorithm with advantages validated through large-scale experiments.

## Link
- [http://arxiv.org/abs/2603.06980v1](http://arxiv.org/abs/2603.06980v1)
