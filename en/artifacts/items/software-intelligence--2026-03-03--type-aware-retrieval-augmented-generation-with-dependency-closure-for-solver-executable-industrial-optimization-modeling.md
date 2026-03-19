---
source: arxiv
url: http://arxiv.org/abs/2603.03180v1
published_at: '2026-03-03T17:41:34'
authors:
- Y. Zhong
- R. Huang
- M. Wang
- Z. Guo
- YC. Li
- M. Yu
- Z. Jin
topics:
- retrieval-augmented-generation
- code-generation
- knowledge-graph
- optimization-modeling
- type-aware-retrieval
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Type-Aware Retrieval-Augmented Generation with Dependency Closure for Solver-Executable Industrial Optimization Modeling

## Summary
This paper proposes a type-aware RAG method for industrial optimization modeling that uses a "minimal dependency closure" to ensure that generation results from natural language to solver code are compilable and solvable. Its core value is reducing the structural hallucinations of LLMs in complex constraint settings, making generated models truly executable.

## Problem
- The goal is to automatically convert natural-language requirements into **solver-executable** optimization model code, but standard LLMs often produce missing declarations, type inconsistencies, and incomplete symbol dependencies.
- These errors are critical in industrial optimization because variables, parameters, index sets, constraints, and objective functions must match strictly; otherwise, the model cannot be compiled or solved.
- Existing RAG methods mostly retrieve untyped text fragments and do not guarantee closure over mathematical dependencies, making it difficult to support reliable automation of optimization modeling.

## Approach
- Build a domain-specific **typed knowledge base / knowledge graph**: parse variables, parameters, constraints, objectives, index sets, and other typed entities from academic papers and solver code, and record relations such as `used_in`, `depends_on`, and `aligns_to`.
- First perform intent recognition and entity extraction on the user's natural-language request, then conduct **hybrid retrieval**: on one hand, use vector semantic retrieval to obtain conceptual background; on the other hand, use structured retrieval in the knowledge graph to locate relevant symbols.
- Compute the **minimal dependency closure** for target entities: perform constrained traversal along `used_in` and `depends_on` edges to find the smallest set of symbols that makes the target "fully defined."
- Feed the typed definitions in the closure, dependency subgraph descriptions, and top-k semantic snippets into the LLM together; the LLM is mainly responsible for "translating into LINGO code," rather than guessing which symbols are needed.
- Lightweight validation and corrective retrieval are also added to further improve compilability and solvability.

## Results
- In the battery production demand response case, the system handles a scheduling problem with **24 hours and 144 10-minute periods**, and automatically adds demand response incentives and load-reduction constraints for **hours 16–17 (periods 91–102)**; the minimum required reduction is **10 kW**, and the incentive price is **0.54 $/kWh**.
- The generated modified model **converges to the global optimum within 120 seconds**, and successfully achieves peak shaving within the event window, showing that the generated code is compilable, solvable, and operationally effective.
- In this case, final output drops from **828** to **786**, a decrease of **5.1%**; however, profit rises from **$2776.86** to **$2780.51**, an increase of **0.13%**, indicating that the system can balance production loss with demand response revenue.
- The paper claims that conventional RAG baselines **cannot generate executable code** in this case, whereas the proposed method can generate an executable LINGO model containing both incentive terms and load constraints.
- In the second flexible job shop scheduling (FJSP) case, the authors claim the method **consistently generates compilable models and reaches known optimal solutions**, demonstrating cross-domain generalization; however, the provided excerpt does not include more specific numerical results or baseline comparison tables.
- The core conclusion of the ablation study is that **integration of heterogeneous knowledge sources** and **type-aware dependency closure** are necessary to avoid structural hallucinations and ensure executability; the excerpt does not provide specific ablation numbers.

## Link
- [http://arxiv.org/abs/2603.03180v1](http://arxiv.org/abs/2603.03180v1)
