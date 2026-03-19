---
source: arxiv
url: http://arxiv.org/abs/2603.12226v1
published_at: '2026-03-12T17:48:34'
authors:
- Priyanka Kargupta
- Shuhaib Mehri
- Dilek Hakkani-Tur
- Jiawei Han
topics:
- llm-scientific-discovery
- interdisciplinary-ideation
- creativity-support
- retrieval-augmented-generation
- human-ai-collaboration
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Sparking Scientific Creativity via LLM-Driven Interdisciplinary Inspiration

## Summary
This paper presents **Idea-Catalyst**, a framework that uses large language models to support interdisciplinary research brainstorming, with the goal of systematically introducing transferable insights from external disciplines before converging too early on specific solutions. It emphasizes augmenting the creative reasoning processes of humans and LLMs, rather than directly automating the entire scientific discovery pipeline.

## Problem
- The paper aims to address the fact that scientific innovation is often trapped in single-discipline “information silos,” while truly high-impact breakthroughs often come from interdisciplinary synthesis.
- Most existing AI research systems focus on “rapidly proposing solutions + running experiments,” which can lead to premature anchoring, compress the exploration space, and weaken cross-domain divergent thinking during the idea formation stage.
- This matters because interdisciplinary research typically has higher long-term impact, yet deeply engaged, long-distance cross-disciplinary collaboration accounts for only about **5%**, indicating that researchers struggle to systematically identify “which ideas from which external fields” are worth borrowing.

## Approach
- **Core mechanism**: first decompose an abstract research goal into several core research questions, then analyze the target-domain literature to determine which questions are solved, partially solved, or still open.
- For unresolved challenges, the system rewrites them as **domain-agnostic conceptual problems**; for example, turning a specific AI problem into “when control should be exercised, and when control should be restrained.”
- It then searches more distant external disciplines for mechanisms, theories, or empirical regularities similar to these abstract problems, extracting concept-level insights supported by the literature.
- Finally, it translates these external insights back into the target-domain context, generates candidate “idea fragments,” and ranks them by interdisciplinary potential, relevance, and impact.
- In implementation, it uses Semantic Scholar Snippets for literature-snippet retrieval, and organizes the workflow around “metacognitive” principles: self-awareness, situational awareness, strategy selection, goal management, and evaluation.

## Results
- The paper claims that, in experiments, Idea-Catalyst improves the average **novelty** of generated ideas by **21%**.
- At the same time, average **insightfulness** increases by **16%**, while maintaining close alignment with the original research problem.
- In the list of contributions, the authors provide more precise figures: based on **LLM evaluation and human evaluation**, the system’s generated ideas show a **21.38%** increase in novelty and a **16.22%** increase in insightfulness.
- The paper also cites background statistics: each additional discipline increases citation impact by about **20%**; however, deep cross-domain collaboration accounts for only about **5%** of interdisciplinary research. These figures are used to illustrate the importance of the problem, not as performance metrics of the method itself.
- The abstract and excerpt do not provide more detailed evaluation settings, such as specific dataset size, comparison baseline names, variance, or statistical significance.

## Link
- [http://arxiv.org/abs/2603.12226v1](http://arxiv.org/abs/2603.12226v1)
