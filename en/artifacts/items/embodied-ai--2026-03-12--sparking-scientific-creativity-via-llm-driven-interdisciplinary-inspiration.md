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
- scientific-discovery
- llm-ideation
- interdisciplinary-research
- retrieval-augmented-generation
- human-ai-collaboration
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Sparking Scientific Creativity via LLM-Driven Interdisciplinary Inspiration

## Summary
Idea-Catalyst is an LLM-driven framework for the scientific brainstorming stage, designed to systematically uncover interdisciplinary inspiration rather than directly automating experiments or quickly converging on a single solution. By decomposing a target problem, identifying unresolved challenges in the target domain, and then retrieving analogous insights from external disciplines, it generates research ideas that are more novel while still remaining closely tied to the original problem.

## Problem
- The paper addresses: how to help researchers and LLMs generate **well-grounded interdisciplinary ideas** early in the research process, breaking out of single-discipline information silos.
- This matters because interdisciplinary research typically leads to greater long-term impact; the paper states that each additional discipline increases citation impact by about **20%**, yet truly high-investment long-distance interdisciplinary collaborations account for only about **5%**.
- Existing AI methods for scientific discovery often shift too early toward experiment execution and feasibility filtering, making ideas more incremental and single-domain, and weakening creative exploration.

## Approach
- The input only needs a short research goal; the system first breaks it down into several **core research questions**, and uses literature from the target domain to analyze how far each question has already been solved.
- For unresolved difficulties, the system rewrites them from “domain terminology” into **domain-agnostic conceptual problems**; for example, abstracting a specific AI collaboration issue into “when to control, and when to relinquish control.”
- It then searches more distant external disciplines for mechanisms, theories, or empirical regularities that address similar conceptual problems, and extracts key literature-supported insights.
- Finally, it **recontextualizes** these external insights back into the target domain, forming candidate idea fragments and ranking them by “interdisciplinary potential,” balancing novelty and relevance.
- The core mechanism can be summarized in the simplest terms as: **first identify exactly where the current field is stuck, then look to other disciplines for solutions to analogous problems, and finally translate them back into new ideas.**

## Results
- The paper claims that, in empirical evaluation, Idea-Catalyst improves average **novelty by 21%**.
- At the same time, it improves average **insightfulness by 16%**.
- In the contribution summary, it provides more precise figures: compared with baselines/controls, the generated ideas show an average **21.38% increase in novelty** and a **16.22% increase in insightfulness**.
- The paper also emphasizes that these gains are achieved while “**still grounded in the original research problem**,” meaning it does not drift away from the original task in pursuit of interdisciplinarity.
- The abstract and excerpt do not provide finer-grained quantitative details, such as the specific dataset scale, number of evaluation samples, names of the baselines used, or significance test results.

## Link
- [http://arxiv.org/abs/2603.12226v1](http://arxiv.org/abs/2603.12226v1)
