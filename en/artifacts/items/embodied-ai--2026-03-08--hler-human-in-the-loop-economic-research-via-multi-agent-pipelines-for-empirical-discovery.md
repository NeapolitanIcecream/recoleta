---
source: arxiv
url: http://arxiv.org/abs/2603.07444v1
published_at: '2026-03-08T03:40:34'
authors:
- Chen Zhu
- Xiaolu Wang
topics:
- multi-agent-systems
- human-in-the-loop
- economic-research
- llm-agents
- research-automation
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# HLER: Human-in-the-Loop Economic Research via Multi-Agent Pipelines for Empirical Discovery

## Summary
HLER is a **human-in-the-loop** multi-agent pipeline for empirical economics research that uses data-constrained topic selection and iterative review to reduce the speculation and distortion that LLMs can introduce into research automation. It emphasizes not full autonomy, but preserving human oversight at key scientific decision points.

## Problem
- Existing “AI scientist”-style systems tend toward **full automation**, but empirical economics research requires that questions match real data, identification strategies be sound, and conclusions be judged by humans for their economic significance.
- Standard LLMs can easily propose **infeasible or hallucinated hypotheses**, for example when the data simply do not contain the relevant variables, or when the data structure does not support the required design.
- This matters because the credibility of empirical social science depends on data auditing, reproducible analysis, and repeated revision, rather than merely generating text that looks like a paper.

## Approach
- HLER divides the workflow into multiple specialized agents: **data auditing, data profiling, question generation, data collection, econometric analysis, manuscript drafting, and automated review**, connected by an orchestrator.
- The core mechanism is **dataset-aware hypothesis generation**: it first reads table structure, variable availability, missingness patterns, distributions, and correlations, and only then has the LLM generate research questions, constraining unrealistic topics at the source.
- The system includes two closed loops: a **question quality loop** (generation → feasibility screening → human selection) and a **research revision loop** (review → additional analysis/robustness checks → revision).
- Human decision gates are retained at key stages: the human researcher is responsible for **topic selection** and **whether to publish the final output**, while the other tedious steps are automated as much as possible.
- The econometric component is mainly executed by programmatic statistical libraries, such as OLS, fixed effects, DID, and event-study; the LLM is mainly responsible for reasoning, planning, and writing.

## Results
- Across **3 datasets and 14 complete pipeline runs**, dataset-aware topic generation produced **79** candidate questions, of which **69 were feasible (87%)**; unconstrained generation produced **34 feasible out of 82 (41%)**, meaning the infeasible rate fell from **59% to 13%**.
- The main failure reasons for unconstrained generation included **nonexistent variables**, accounting for **42%** of failures, and **designs incompatible with the data structure**, accounting for **35%**.
- The end-to-end completion rate was **12/14 = 86%**; the **2 failures** both stalled on sparse-subsample convergence issues in fixed-effects estimation, but the system could log the errors and stop gracefully.
- In the revision loop, across the 12 completed runs, the reviewer’s average overall score improved from **4.8 ± 0.9** for the first draft to **5.9 ± 0.7** after one revision, and reached **6.3 ± 0.6** for the final draft; the largest gains came from **clarity (+2.1 points)** and **identification credibility (+1.4 points)**, while **novelty increased by only +0.3 points**.
- Typical reviewer requests included **additional robustness checks (10/12)**, **clearer discussion of the identification strategy (8/12)**, and **better variable descriptions (7/12)**; most runs converged within **2–3 rounds**, though the paper also states typically **2–4 rounds**.
- A single run took about **20–25 minutes**, with an average API cost of **$0.8–$1.5 per run**; the authors compare this with the **$6–$15 per paper** reported by AI Scientist and claim that HLER is cheaper. In the case study, the CHNS task was revised from a **5,563-word** first draft to a **7,282-word** final draft, the review score rose from **4.6** to **6.5**, and identification credibility increased from **3.2** to **5.8**.

## Link
- [http://arxiv.org/abs/2603.07444v1](http://arxiv.org/abs/2603.07444v1)
