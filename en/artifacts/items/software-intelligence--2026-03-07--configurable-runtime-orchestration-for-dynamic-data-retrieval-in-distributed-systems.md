---
source: arxiv
url: http://arxiv.org/abs/2603.06980v1
published_at: '2026-03-07T01:45:18'
authors:
- Abhiram Kandiraju
topics:
- runtime-orchestration
- distributed-systems
- microservices
- dynamic-workflows
- configuration-driven
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Configurable Runtime Orchestration for Dynamic Data Retrieval in Distributed Systems

## Summary
This paper proposes a **configuration-driven framework that dynamically generates execution graphs at request time** for orchestrating distributed data retrieval, targeting enterprise scenarios where aggregation across frequently changing microservices/APIs/analytics platforms is common. Its core value is enabling low-latency, parallelized data aggregation through configuration updates **without redeploying orchestration code**.

## Problem
- Existing orchestration systems such as Airflow, Step Functions, and Temporal typically require **predefined workflows** (DAGs, state machines, or code-defined workflows), making them ill-suited for request-level data aggregation where topology changes frequently.
- Enterprise scenarios such as Customer 360, risk control, and operations often need to access multiple heterogeneous systems within a single request; if orchestration logic is hardcoded in code/workflows, **adding a new data source, changing dependencies, or adjusting optional rules** all become deployment events.
- This matters because enterprises need both **flexibility** (rapidly integrating changing services) and **performance** (low-latency responses), while serial calls waste latency budget.

## Approach
- The core idea is: **treat configuration, rather than predefined workflows, as the source of truth**. After receiving a request, the system reads the configuration, computes a dependency graph on the fly, and then executes it.
- The architecture has five layers: Request Adapter, Configuration Resolver, Execution Planner, Execution Engine, Aggregation/Response; among them, the Planner is responsible for parsing declarative configuration into a runtime dependency graph.
- The execution mechanism is straightforward: each call/transformation is treated as a node in the graph, and prerequisites are treated as edges; **nodes with no unsatisfied dependencies are executed in parallel immediately**, while nodes with dependencies wait for their predecessors to complete.
- Failure semantics are explicitly modeled as required / optional / fallback nodes, supporting **partial but still valid** results in latency-constrained scenarios rather than blindly pursuing long-running durable completion.
- In the Customer 360 example, account, transactions, fraud, and risk can run in parallel as four initial independent nodes; later, if recent-case context is added, only the configuration needs to be changed and the planner will automatically incorporate it into the graph.

## Results
- The paper **does not provide formal experiments, benchmarks, or quantitative metrics**; it reports no concrete numbers for latency, throughput, or success rate, and does not provide datasets or statistically significant results.
- The strongest concrete claim is: when a Customer 360 request includes **4 immediately executable nodes** (account, transactions, fraud, risk), the system can identify their independence at runtime and **execute 4 calls in parallel**.
- The paper claims that compared with Airflow / Step Functions / Temporal, its advantage is that **request-level topology changes do not require redeploy**, whereas those comparison systems typically require updating DAGs, state machines, or workflow code and then redeploying.
- The performance claim is qualitative: runtime graph generation introduces some planning overhead, but that overhead is usually **smaller than the cost of network-bound data retrieval**; the actual gains mainly come from dependency-aware parallelism and decoupling from deployment.
- The applicability boundary is also clearly stated: for workflows that are **long-running, strongly durable, involve cross-day retries, or require human participation**, the author does not claim superiority over durable workflow engines such as Temporal.

## Link
- [http://arxiv.org/abs/2603.06980v1](http://arxiv.org/abs/2603.06980v1)
