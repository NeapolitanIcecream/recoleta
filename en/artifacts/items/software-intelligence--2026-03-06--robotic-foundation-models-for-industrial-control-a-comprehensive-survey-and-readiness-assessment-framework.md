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
- survey
- safety-critical-systems
relevance_score: 0.36
run_id: materialize-outputs
language_code: en
---

# Robotic Foundation Models for Industrial Control: A Comprehensive Survey and Readiness Assessment Framework

## Summary
This survey focuses on the deployability of robotic foundation models (RFMs) in industrial control. Rather than proposing a new model, it systematically evaluates "how far current RFMs still are from industrial usability." The authors provide a maturity assessment framework oriented toward industrial deployment and use it to make a conservative, auditable comparison across large-scale RFM literature and models.

## Problem
- Existing RFM research often emphasizes benchmark success, but lacks systematic evaluation for **industrial settings**, making it difficult to judge whether models are truly suitable for safe, real-time, low-cost factory deployment.
- Industrial robots, especially collaborative robots, require models to simultaneously satisfy multiple requirements such as **safety, low latency, robust perception, cross-hardware adaptation, and edge-computing constraints**; strength in a single capability does not equal deployability.
- The number of RFM papers has grown rapidly in recent years. Without a unified framework, the field is prone to **fragmentation and exaggerated conclusions**, which is not conducive to alignment between research and industry.

## Approach
- From the perspective of industrial deployment, the authors first structure robot control methods hierarchically and define RFMs as having a "generalist core" that must support **multimodal input, flexible output, and cross-task/cross-embodiment adaptability**.
- They synthesize industrial requirements into **11 interdependent deployment implications**, then refine them into an assessment catalogue containing **149 specific criteria**, covering both model capabilities and ecosystem requirements.
- To build the survey corpus, the authors use an automated retrieval and LLM-assisted screening pipeline: two rounds of large-scale retrieval yielded **10,728** and **12,027** valid records, which were merged into **6,497** unique papers; after screening, **1,025** highly relevant publications remained.
- For model evaluation, the authors use a **conservative LLM-assisted review process**, validated with expert judgment, to score **324 manipulation-capable RFMs** criterion by criterion, producing a total of **48,276** criterion-level decisions.

## Results
- The paper's central conclusion is that the **industrial maturity of current RFMs is limited and unevenly distributed**; even the highest-scoring models satisfy only **a subset of the 149 criteria**, and no model demonstrates comprehensive coverage of industry-critical requirements.
- In terms of evaluation scale, the authors claim this is a relatively large-scale and traceable analysis of industrial maturity: **324** manipulation-capable RFMs, **149** criteria, and **48,276** criterion-level judgments in total.
- For the literature review scale, the final main corpus contains **1,025** highly relevant papers, including **341** control or integrated RFMs; among them, **324** focus on manipulation / mobile manipulation / general robotic tasks, while **17** target other embodiments or domains.
- The retrieval and filtering pipeline shows that the field is growing rapidly: the two searches produced **10,728/12,027** valid records respectively; after merging and deduplication there were **6,497** papers, then screening reduced this to **4,834** robot-related papers, then **1,408** RFM-related papers, and finally **1,025** manually curated papers.
- The paper **does not provide traditional experimental figures such as single-model SOTA accuracy/success-rate gains**; its strongest empirical claim is that existing models typically show only "local peaks" on a small number of industrial implication dimensions, and still fall clearly short of an industry-grade RFM that integrates **safety, real-time performance, robust perception, interaction, and cost efficiency**.

## Link
- [http://arxiv.org/abs/2603.06749v1](http://arxiv.org/abs/2603.06749v1)
