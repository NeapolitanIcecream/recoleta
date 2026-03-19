---
source: arxiv
url: http://arxiv.org/abs/2603.05941v1
published_at: '2026-03-06T06:18:20'
authors:
- Arun Joshi
topics:
- xai
- coding-agents
- failure-analysis
- llm-debugging
- execution-traces
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# XAI for Coding Agent Failures: Transforming Raw Execution Traces into Actionable Insights

## Summary
This paper proposes an explainable AI framework for analyzing failures of LLM coding agents, transforming hard-to-read raw execution traces into structured, visualized, and actionable explanations. Its core value is helping both technical and non-technical users identify root causes faster and propose more accurate fixes in real debugging scenarios.

## Problem
- Problem addressed: LLM coding agents often fail, but what they leave behind are lengthy, nested, and hard-to-interpret execution logs, making it difficult for developers and stakeholders to understand where things went wrong, why they went wrong, and how to fix them.
- Why it matters: If failure causes are not interpretable, coding agents cannot be reliably deployed in software development workflows, debugging costs remain high, and user trust is hard to establish.
- Limitations of existing general-purpose LLM explanations: inconsistent explanations, lack of domain structure, no visualization of execution flow, and rarely any directly actionable repair suggestions.

## Approach
- First, the authors derive a taxonomy of coding agent failures from **32 real failure cases**, including categories such as misunderstanding failure and iterative refinement failure; the most common is “hitting the iteration limit without making progress.”
- Then they use **GPT-4/4.1 + structured outputs/function calling** for automatic annotation: extracting features such as error messages, iteration counts, and execution patterns from raw traces to automatically determine failure category, subcategory, and confidence.
- Next, they build a **hybrid explanation system**: one part generates execution flow diagrams (Graphviz), one part produces natural-language root cause analysis, and another provides counterfactual explanations and repair recommendations.
- The output serves multiple audiences at once: it can generate human-readable HTML reports and also produce JSON results that can be integrated into CI/CD or monitoring systems.
- Put simply, the method is: “**first classify the failure, then turn the log into a flow, then use templated + LLM-generated explanations and recommendations**,” thereby turning messy logs into actionable insights.

## Results
- Data and failure distribution: across **87** HumanEval coding agent runs, there were **32 failures and 55 successes**; among failures, **18/32 (56%)** were iterative refinement failure, the most common pattern.
- Automatic classification performance: on **32 failure samples**, automatic classification achieved **82.1% (26/32)** accuracy; for high-confidence predictions (**p>0.8**), accuracy was **90.5% (19/21)**; agreement with human annotation was **Cohen’s κ = 0.76**.
- User study scale: **20 participants** in total, including **10 technical users** and **10 non-technical users**, comparing three conditions: raw traces, general-purpose LLM explanations, and the authors’ method.
- Speed of understanding: the authors’ method enabled users to understand failures **2.8× faster** than raw traces; average time for technical users dropped from **8.4±2.1 min** to **3.0±0.8 min**, and for non-technical users from **12.8±3.2 min** to **4.2±1.1 min**, with **p<0.01**.
- Root cause identification and fix quality: for technical users, root cause identification improved from **42±15%** with raw traces and **68±12%** with general-purpose LLMs to **89±8%**; for non-technical users, it improved from **18±12%** and **52±18%** to **76±11%**. Fix quality (1–5 scale) for technical users improved from **2.6±0.8 / 3.4±0.6** to **4.3±0.5**, and for non-technical users from **1.4±0.6 / 2.8±0.7** to **3.8±0.6**.
- Confidence and qualitative feedback: technical users’ confidence in understanding increased from **3.2±1.1** to **6.1±0.7**, and non-technical users’ from **2.1±0.9** to **5.6±0.8**; **18/20** participants explicitly said the execution flow diagrams were “very helpful” or “essential.”

## Link
- [http://arxiv.org/abs/2603.05941v1](http://arxiv.org/abs/2603.05941v1)
