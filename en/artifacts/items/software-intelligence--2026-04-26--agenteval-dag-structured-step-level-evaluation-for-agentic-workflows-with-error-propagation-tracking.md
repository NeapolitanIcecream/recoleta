---
source: arxiv
url: http://arxiv.org/abs/2604.23581v1
published_at: '2026-04-26T07:38:47'
authors:
- Dongxin Guo
- Jikun Wu
- Siu Ming Yiu
topics:
- agent-evaluation
- workflow-debugging
- root-cause-analysis
- llm-as-judge
- software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking

## Summary
AgentEval evaluates multi-step AI agent workflows by scoring each step in a DAG and tracing which earlier error caused later failures. It targets production debugging and regression testing, where end-to-end checks miss most actionable failures.

## Problem
- Multi-step agents fail in intermediate planning, tool choice, parameter generation, execution, and synthesis steps, but end-to-end evaluation only sees the final output.
- In real workflows, many failures are propagated from earlier steps, so teams need to know where an error started, not only that the final answer is bad.
- Production teams also need continuous regression detection in CI/CD, which ad-hoc trace inspection does not scale to provide.

## Approach
- The paper models each agent run as an evaluation DAG, where nodes are workflow steps and edges show dependencies between steps.
- Each step type gets its own quality metrics: plan, tool selection, parameter generation, execution, and synthesis. A calibrated GPT-4o judge scores each step on a 15 rubric using local context and optional references.
- If a step fails, AgentEval assigns a failure label from a 3-level taxonomy with 21 subcategories, built from 523 separate agent traces.
- Root cause attribution uses a simple rule: if a failed step depends on earlier failed parents, the lowest-scoring parent is treated as the source; otherwise the step is marked as a root cause.
- The system supports schema-defined and trace-inferred DAGs, handles most non-DAG traces by loop unrolling and timestamp-based branch resolution, and plugs into CI/CD for regression tests.

## Results
- On 150 human-annotated test cases, AgentEval reached failure detection recall 0.89, versus 0.41 for end-to-end evaluation and 0.67 for flat step evaluation. That is 2.17x higher recall than end-to-end and +22 percentage points over flat step evaluation.
- On the same setup, human agreement reached Cohens kappa = 0.84, versus 0.71 for flat step evaluation and 0.52 for end-to-end evaluation.
- Root cause accuracy was 0.72, compared with 0.38 for flat step evaluation and an 0.81 human ceiling. In the ablation, removing DAG structure cut root cause accuracy by 34 percentage points and failure detection recall by 22 points.
- Across all 450 test cases, 63% of step-level failures were propagated from upstream errors. Non-DAG traces were about 12% of cases; on those, AgentEval still reported failure detection recall 0.82 and root cause accuracy 0.58.
- In cross-system tests without changing the taxonomy or rubrics, failure detection recall stayed at 0.83 and 0.79 on -bench retail and airline, and 0.78 on SWE-bench code editing. Root cause accuracy dropped to 0.61, 0.55, and 0.52 on those settings.
- In a 4-month pilot with 18 engineers, the system detected 23 pre-release regressions, reduced median root-cause identification time from 4.2 hours to 22 minutes, and the regression detector reached 88% precision and 94% recall across 18 simulated scenario-workflow combinations.

## Link
- [http://arxiv.org/abs/2604.23581v1](http://arxiv.org/abs/2604.23581v1)
