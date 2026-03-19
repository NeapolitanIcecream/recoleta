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
- human-data-interaction
- visual-analytics
- foundation-models
- multimodal-analytics
- trustworthy-ai
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Human-Data Interaction, Exploration, and Visualization in the AI Era: Challenges and Opportunities

## Summary
This is a survey/position paper on human–data interaction and visual analytics in the AI era, discussing how large models, multimodality, and unstructured data are reshaping interactive data analysis systems. The paper’s core contribution is not to propose a single new algorithm, but to systematically organize the challenges and argue for reconstructing systems around human cognition, latency perception, trustworthiness, and end-to-end collaborative design.

## Problem
- The paper addresses the following problem: in the AI era, when interactive data analysis faces **large-scale, heterogeneous, multimodal, unstructured data** and **the uncertainty introduced by LLMs/VLMs**, why are existing human–data interaction and visual analytics systems unable to remain efficient, reliable, and interpretable?
- This matters because analysts need to repeatedly explore, rewrite queries, and verify intermediate results under uncertainty; if system latency is too high, scalability is insufficient, or AI outputs are untrustworthy, the reasoning process is disrupted, cognitive burden increases, and the quality of human–machine collaboration is weakened.
- Traditional evaluation methods that focus only on throughput, P95 latency, or offline accuracy are insufficient to measure real interactive experience, especially when a single interaction may trigger multiple queries, progressive updates, and multimodal feedback.

## Approach
- The core method of this paper is **perspective survey + research agenda setting**: it synthesizes the key bottlenecks and open directions for human–data interaction systems in the AI era from the perspectives of databases, AI, information visualization, HCI, and computer graphics.
- It argues that data management, AI models, interfaces, and visualization should be treated as an **end-to-end co-designed** whole, rather than loosely coupled modules; system design should directly account for interface structure, user perception, and interaction context.
- The paper emphasizes that “**query speed should approach the speed of human thought**,” requiring underlying systems to be designed around perceptually aligned latency, approximate computation, prefetching, indexing, progressive analysis, and result refinement.
- It proposes that future interfaces should move toward **multimodal, action-oriented, mixed-initiative** interaction paradigms, combining natural language, gestures, AR/VR, narrative and generative visualization, while ensuring that humans always retain the ability to supervise, trace provenance, and calibrate trust.
- For the AI component, the paper’s basic mechanistic claim is: large models are powerful, but they cannot replace structured tools and human-in-the-loop validation; therefore, clearer system abstractions, trustworthy analysis mechanisms, and interaction design oriented toward uncertainty are needed.

## Results
- This is not an experimental paper reporting a new model or new benchmark SOTA; **the provided excerpt does not include new quantitative experimental results, dataset comparisons, or performance numbers**.
- A more specific quantitative observation given in the paper is that among papers published at IEEE VIS, only **2%** used keywords related to “scalability,” illustrating insufficient systematic attention to scalability in the visualization community.
- The paper explicitly argues that interactive analysis requires **millisecond-level (order-of-millisecond)** responses, whereas many existing data systems are optimized more for **second-level or minute-level** responses; this mismatch reduces the number of observations and introduces exploration bias.
- The paper also suggests that even a delay of just **a few seconds** may interrupt analytical reasoning, alter exploration paths, and reduce the effectiveness of human–machine collaboration.
- Rather than presenting numeric breakthroughs, the paper’s stronger concrete contribution is the systematic proposal of several research directions, including interface–system co-optimization, cold start and progressive visual analytics, new interaction paradigms for multimodal/unstructured data, and trustworthy analysis and interpretable feedback mechanisms when LLMs/VLMs are involved.

## Link
- [http://arxiv.org/abs/2603.05542v1](http://arxiv.org/abs/2603.05542v1)
