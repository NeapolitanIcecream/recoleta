---
source: arxiv
url: http://arxiv.org/abs/2603.05542v1
published_at: '2026-03-04T14:18:17'
authors:
- Jean-Daniel Fekete
- Yifan Hu
- Dominik Moritz
- Arnab Nandi
- Senjuti Basu Roy
- Eugene Wu
- Nikos Bikakis
- George Papastefanatos
- Panos K. Chrysanthis
- Guoliang Li
- Lingyun Yu
topics:
- human-ai-interaction
- visual-analytics
- multimodal-data
- foundation-models
- interactive-data-systems
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# Human-Data Interaction, Exploration, and Visualization in the AI Era: Challenges and Opportunities

## Summary
This is a position/review paper that discusses the new challenges facing human–data interaction, exploration, and visualization systems in the AI era, and proposes human-centered research directions for the future. The core argument is that traditional designs centered on throughput and average latency are no longer sufficient; systems, interfaces, AI models, and visualization need to be restructured as a coordinated whole.

## Problem
- The paper addresses why existing interactive data analysis systems struggle to continue supporting high-quality human analysis and decision-making after the widespread adoption of **large-scale, heterogeneous, multimodal, unstructured data** and **foundation models such as LLMs/VLMs**.
- This matters because the analytical process requires **responses close to the speed of human thought**; even delays of a few seconds can interrupt reasoning, reduce the number of observations, introduce exploration bias, and weaken human–machine collaboration.
- Another key issue is the **uncertainty, error propagation, bias, lack of interpretability, and verification cost** introduced by AI, which makes it harder for users to trust and calibrate AI-generated analytical results.

## Approach
- Rather than an experimental paper proposing a single algorithm, this paper presents an **end-to-end human-centered framework**: it treats data management, AI components, interactive interfaces, and visualization as a tightly coupled system to be designed jointly rather than optimized separately.
- The paper emphasizes upgrading from the traditional view of “treating interfaces as SQL workloads” to **interface/perception-constrained system design**: not only optimizing query speed, but also considering which views should update first, which results must stay synchronized, and whether the latency perceived by users feels smooth.
- For multimodal and AI-based analysis, the authors advocate mechanisms such as **progressive computation, approximate queries, prefetching, indexing, interface-aware optimization, and mixed-initiative interaction**, allowing systems to provide useful feedback quickly and then continuously refine results.
- At the interaction layer, the paper argues for developing new interfaces such as **natural language, gestures, AR/VR, narrative, and generative visualization**, and for turning visualization from a “passive output” into an active component that supports exploration, verification, attention guidance, and trust calibration.
- In terms of human–machine division of labor, the core mechanism can be understood simply as: **AI is responsible for generating candidate interpretations and action suggestions, humans are responsible for supervision, verification, error correction, and final judgment**, while the system is responsible for making this loop sufficiently fast, transparent, and trustworthy.

## Results
- Based on the provided excerpt, this is a **review/forward-looking paper** and **does not report new experimental data, benchmark datasets, or quantitative SOTA metrics**.
- One of the clearest quantitative signals given in the paper is that, in IEEE VIS conference papers, **only 2%** of articles use keywords related to “scalability,” illustrating that the visualization field still lacks systematic attention to scalability.
- The paper explicitly argues that interactive analysis requires **millisecond-level (order-of-millisecond)** responses, while many existing data systems are still designed for **second-level or even minute-level** response times; this mismatch in timescales reduces exploration efficiency and introduces bias.
- The paper also makes a strong claim that future systems should support interactive analysis under **large-scale, multimodal, unstructured data** and **foundation-model uncertainty**, but the excerpt does not provide corresponding quantitative validation results.
- Therefore, the paper’s main “breakthrough” is not numerical improvement, but the proposal of a **unified problem framework and research agenda** spanning databases, visualization, HCI, and AI.

## Link
- [http://arxiv.org/abs/2603.05542v1](http://arxiv.org/abs/2603.05542v1)
