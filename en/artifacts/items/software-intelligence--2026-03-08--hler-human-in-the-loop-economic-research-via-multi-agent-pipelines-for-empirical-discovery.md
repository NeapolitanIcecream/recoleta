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
- dataset-aware-generation
- automated-scientific-workflows
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# HLER: Human-in-the-Loop Economic Research via Multi-Agent Pipelines for Empirical Discovery

## Summary
HLER is a human-in-the-loop multi-agent pipeline for empirical economic research, designed to automate data auditing, topic selection, econometric analysis, writing, and review while preserving critical human oversight. Its core contributions are dataset-aware question generation and a dual feedback loop, which reduce speculative topic selection and improve the stability of end-to-end research output.

## Problem
- Existing “AI scientist” systems tend toward full automation, but empirical research in economics/social science depends heavily on **data feasibility, identification strategy design, and human judgment**, and pure text generation can easily propose questions that are unverifiable or unreliable.
- Unconstrained LLM topic generation often produces **hallucinated hypotheses**: required variables do not exist, the research design does not match the data structure, or the implied econometric method is unsupported.
- This matters because the credibility of empirical research depends on **data validation, transparent analysis, reproducibility, and judgments of economic significance**, not merely generating a seemingly plausible paper.

## Approach
- Proposes a **multi-agent pipeline** in which an orchestrator connects 7 specialized agents: data-audit, data-profiling, question, data-collection, econometrics, paper, review.
- The core mechanism is **dataset-aware hypothesis generation**: first conduct data auditing and statistical profiling, then have the LLM generate research questions under constraints from variable availability, missingness patterns, distributional characteristics, and data structure, avoiding data-detached speculation.
- Two loops are designed: the **question quality loop** (generation → feasibility screening → human topic selection) and the **research revision loop** (automated review → additional analysis → manuscript revision), allowing the system to iterate like real research.
- **Human decision gates** are inserted at key nodes: human researchers are responsible for research question selection and final publication approval, while other highly repetitive work is automated as much as possible.
- Econometric execution is handled by programmatic statistical libraries, supporting **OLS, fixed-effects, difference-in-differences, event-study**; the LLM is mainly responsible for planning, interpretation, and writing.

## Results
- Across **3 datasets and 14 full pipeline runs**, dataset-aware topic generation produced **79** candidate questions, of which **69 were feasible, for a success rate of 87%**; unconstrained generation yielded **34 feasible out of 82, or 41%**. Equivalently, the infeasible share fell from **59% to 13%**.
- Among the main failure reasons for unconstrained generation, **42%** came from missing variables and **35%** from incompatibility between research design and data structure; this directly supports the authors’ claim that “data constraints can suppress hallucinated topic selection.”
- The end-to-end completion rate was **12/14 = 86%**; the **2** failures both occurred because fixed-effects estimation failed to converge on sparse subsamples, and the system could log the errors and stop safely.
- In the revision loop, for the **12 completed runs**, the average total review score improved from **4.8** for the first draft to **5.9** after the first revision and **6.3** for the final draft (on a 1–10 scale); **clarity +2.1** and **identification credibility +1.4**, while **novelty only +0.3**, indicating that the loop mainly improves presentation and robustness rather than the underlying novelty of the research.
- In terms of runtime efficiency, a single full pipeline run takes about **20–25 minutes**, with an average API cost of **$0.8–$1.5 per run**; the paper says this is lower than the **$6–$15 per paper** reported by AI Scientist.
- In the CHNS case: the data contain **285 variables and 57,203 observations**; in the topic-selection stage, **7 of 8 candidates were feasible**; the analysis sample had **19,466 observations**; the manuscript grew from **5,563 words** to **7,282 words** over **3 rounds** of revision, and the total review score rose from **4.6** to **6.5**, with identification **3.2→5.8** and clarity **4.1→6.9**.

## Link
- [http://arxiv.org/abs/2603.07444v1](http://arxiv.org/abs/2603.07444v1)
