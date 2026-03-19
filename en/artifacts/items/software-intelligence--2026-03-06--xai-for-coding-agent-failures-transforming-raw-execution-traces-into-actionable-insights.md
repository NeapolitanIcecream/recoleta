---
source: arxiv
url: http://arxiv.org/abs/2603.05941v1
published_at: '2026-03-06T06:18:20'
authors:
- Arun Joshi
topics:
- coding-agents
- explainable-ai
- failure-analysis
- execution-traces
- developer-tools
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# XAI for Coding Agent Failures: Transforming Raw Execution Traces into Actionable Insights

## Summary
This paper proposes an explainability system for coding agent failure analysis that converts hard-to-read raw execution traces into structured, actionable explanations. Its core value is enabling both technical and non-technical users to locate root causes faster and propose better fixes.

## Problem
- LLM coding agents fail frequently, but failure information is often buried in long, nested raw execution traces, making them hard for developers to understand quickly, let alone non-technical users.
- When general-purpose large models provide ad-hoc explanations of failures, they are often unstable, lack domain structure, provide no visual context, and often fail to offer actionable repair suggestions.
- This matters because without efficiently understanding why failures happen, it is difficult to debug, deploy, and improve agent reliability in software development.

## Approach
- Based on 32 real failure cases from 87 HumanEval coding agent runs, the authors build a failure taxonomy for coding agents.
- They use GPT-4/4.1 structured outputs for automatic annotation: extracting features from traces, then predicting failure category, subcategory, and confidence according to the taxonomy.
- The system generates three kinds of explanations: execution flow diagrams, natural-language root cause descriptions, and action recommendations plus counterfactual analysis mapped to failure categories.
- The outputs are suitable both for human consumption (HTML + visualization) and for system integration (JSON), supporting inclusion in CI/CD or monitoring workflows.

## Results
- Data and taxonomy: 87 runs were analyzed in total, including 32 failures and 55 successes; among failures, "iterative improvement failure" was the most common, accounting for **56%** (18/32).
- Automatic classification performance: on 32 failure samples, the system achieved **82.1%** accuracy (26/32); high-confidence predictions were **90.5%** (19/21) accurate; agreement with human annotation reached Cohen's **κ=0.76**.
- User study: among **20** participants (10 technical, 10 non-technical), the system enabled users to understand failures **2.8× faster** than with raw traces and **1.7× faster** than with general-purpose LLM explanations (**p<0.01**).
- Technical users: understanding time decreased from **8.4±2.1** minutes (raw) / **5.2±1.3** (general-purpose LLM) to **3.0±0.8**; root-cause identification accuracy increased from **42±15%** / **68±12%** to **89±8%**; fix quality improved from **2.6/5** / **3.4/5** to **4.3/5**.
- Non-technical users: understanding time decreased from **12.8±3.2** / **7.1±1.8** to **4.2±1.1**; root-cause identification accuracy increased from **18±12%** / **52±18%** to **76±11%**; fix quality improved from **1.4/5** / **2.8/5** to **3.8/5**.
- The claimed breakthrough is that, compared with raw traces and ad-hoc general-purpose LLM explanations, a domain-specific, structured XAI pipeline with visualizations and recommendations can significantly improve consistency, comprehension speed, root-cause judgment, and the quality of proposed fixes.

## Link
- [http://arxiv.org/abs/2603.05941v1](http://arxiv.org/abs/2603.05941v1)
