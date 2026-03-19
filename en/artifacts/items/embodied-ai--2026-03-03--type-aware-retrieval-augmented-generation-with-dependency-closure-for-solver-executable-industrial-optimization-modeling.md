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
- knowledge-graph
- optimization-modeling
- type-aware-retrieval
- dependency-closure
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Type-Aware Retrieval-Augmented Generation with Dependency Closure for Solver-Executable Industrial Optimization Modeling

## Summary
This paper proposes a type-aware RAG method for industrial optimization modeling that uses a "dependency closure" to automatically complete the minimal context required by variables, parameters, index sets, and constraints, enabling stable generation of solver-executable code from natural language. Its core value is reducing structural hallucinations by LLMs in optimization modeling, turning outputs from "looking like code" into models that can actually compile and be solved.

## Problem
- The problem it addresses is how to automatically translate natural-language requirements in industrial settings into optimization model code that is **compilable and solvable**, rather than merely semantically plausible but practically non-executable.
- This matters because every constraint in an industrial optimization model must reference variables, parameters, and indices that have been declared and typed correctly; if declarations are missing, types are inconsistent, or dependencies are incomplete, the model cannot be executed by solvers such as LINGO/Gurobi/CPLEX.
- Existing RAG methods mostly retrieve unstructured text fragments and lack guarantees of "type consistency" and "dependency closure," causing LLMs to frequently produce structural hallucinations, especially in constraint-intensive industrial optimization tasks.

## Approach
- Build a **typed knowledge base/knowledge graph**: parse papers and solver code into typed knowledge units such as decision-variables, parameters, index-sets, constraints, objective-functions, and auxiliary-rules.
- Explicitly encode mathematical dependency relations in the graph, such as `used_in`, `depends_on`, and `aligns_to`, aligning concepts in papers with concrete symbols in code.
- Perform **hybrid retrieval** on the user's natural-language request: use vector retrieval to find semantically relevant background on one hand, and identify relevant seed nodes and structured definitions from the knowledge graph on the other.
- Compute the **minimal dependency closure** for the target entities: run BFS along executability-critical edges, retaining only the minimal set of symbols necessary to make the target constraint/objective function "fully defined and executable."
- Feed the type definitions, dependency subgraph descriptions, and semantic fragments together to the LLM (WizardCoder-33B in the paper's example), so the model mainly handles "translation into code" rather than guessing missing structure itself.

## Results
- In the battery production demand response case, the method successfully generated executable LINGO code containing both incentive revenue terms and peak-shaving constraints; the paper states that **conventional RAG baselines failed** and could not generate executable code.
- This demand response model **converged to the global optimum within 120 seconds**; the scenario was set as **24 hours / 144 ten-minute periods**, requiring at least **10 kW of reduction** during **hours 16–17 (periods 91–102)**, with an incentive price of **$0.54/kWh**.
- In this case, final output decreased from **828 to 786**, a reduction of **5.1%**; however, profit increased from **$2776.86** to **$2780.51**, an increase of **0.13%**, indicating that the model can balance production loss against demand response revenue.
- The paper also claims that in the flexible job shop scheduling (FJSP) case, the method **consistently generated compilable models and reached known optimal solutions**, demonstrating cross-domain generalization; it also states that **baseline methods failed completely on all test instances**.
- The core conclusion of the ablation study is that **heterogeneous knowledge source integration** and **type-aware dependency closure** are necessary to avoid structural hallucinations and ensure executability.
- However, in the provided excerpt, aside from the battery demand response case, **no more complete FJSP numerical tables or specific baseline metrics are provided**.

## Link
- [http://arxiv.org/abs/2603.03180v1](http://arxiv.org/abs/2603.03180v1)
