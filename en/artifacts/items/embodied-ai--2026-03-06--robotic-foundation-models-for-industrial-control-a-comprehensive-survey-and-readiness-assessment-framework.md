---
source: arxiv
url: http://arxiv.org/abs/2603.06749v1
published_at: '2026-03-06T11:23:00'
authors:
- David Kube
- Simon Hadwiger
- Tobias Meisen
topics:
- robotic-foundation-models
- industrial-robotics
- readiness-assessment
- vision-language-action
- manipulation
- survey
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Robotic Foundation Models for Industrial Control: A Comprehensive Survey and Readiness Assessment Framework

## Summary
This is a survey of robotic foundation models (RFMs) for industrial control scenarios. It does not propose a new model; rather, it systematically evaluates how far existing RFMs still are from real industrial deployment. The paper’s core value lies in making “industrial deployability” concrete as an auditable evaluation framework and, on that basis, conducting a large-scale analysis of the current model ecosystem.

## Problem
- Existing RFM/VLA research often emphasizes benchmark performance, but lacks a systematic review from the perspective of **industrial deployment**, especially regarding requirements such as safety, real-time performance, heterogeneous hardware, edge computing, and system integration.
- Industrial robots, especially collaborative robots, require general control capabilities that are instruction-following, transferable, and low in engineering cost; however, academic progress does not mean systems can directly enter factories.
- The literature is growing extremely quickly, which can easily lead to fragmentation and overstated conclusions; therefore, a reusable and traceable maturity assessment framework is needed to judge whether RFMs truly have industrial readiness.

## Approach
- The paper first starts from industrial requirements and redefines RFMs: they are required to possess **general core capabilities**, adapt across tasks and embodiments, and support multimodal inputs and flexible outputs, rather than being only a single perception or single control module.
- The authors summarize industrial deployment requirements into **11 interdependent implication dimensions** and operationalize these dimensions into an evaluation catalog containing **149 specific criteria**, covering both model capabilities and ecosystem requirements.
- They establish a standardized literature acquisition and screening process: through automated database retrieval, LLM-assisted filtering, and manual review, they organize the literature and model genealogy related to RFMs.
- In the evaluation stage, the authors use a **conservative LLM-assisted judgment pipeline**, validated with expert judgments, to score **324 manipulation-capable RFMs** criterion by criterion.
- The final result is a large-scale, industry-maturity-oriented horizontal comparison, rather than a classification based only on model architecture or a single benchmark.

## Results
- The paper claims to have completed an industrial maturity assessment of **324 manipulation-capable RFMs**, producing a total of **48,276 criterion-level decisions**.
- The evaluation framework itself includes **11 industrial deployment implication dimensions** and **149 specific criteria**, covering not only model capabilities but also deployment ecosystem requirements.
- In terms of literature construction, the main corpus ultimately contains **1,025** highly relevant papers, including **341 control/integrated RFMs**; among them, **324** focus on manipulation, mobile manipulation, or general robotics scenarios.
- Two rounds of large-scale retrieval yielded **10,728** and **12,027** valid article records, respectively; after merging and deduplication, this resulted in **6,497** unique entries; after two-stage filtering, **1,408** were retained, and after further manual refinement, the final corpus was obtained.
- The core conclusion is that **industrial maturity is overall “limited and uneven”**; even the highest-scoring models satisfy only **a portion** of the criteria and typically stand out only on a few dimensions, rather than comprehensively covering the capabilities required by industry.
- The provided excerpt does not give specific average scores for each model, leaderboard values, or percentage improvements relative to a certain baseline; the strongest quantitative claims are the scale of the evaluation (324 models, 149 criteria, 48,276 decisions) and the overall conclusion that “there is currently no truly industry-grade RFM.”

## Link
- [http://arxiv.org/abs/2603.06749v1](http://arxiv.org/abs/2603.06749v1)
