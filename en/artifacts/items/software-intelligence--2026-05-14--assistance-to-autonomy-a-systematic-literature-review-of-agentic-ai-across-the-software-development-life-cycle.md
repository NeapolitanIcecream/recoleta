---
source: arxiv
url: https://arxiv.org/abs/2605.15245v1
published_at: '2026-05-14T10:46:51'
authors:
- Spyridon Alvanakis Apostolou
- Jan Bosch
- "Helena Holmstr\xF6m Olsson"
topics:
- agentic-ai
- software-engineering
- systematic-review
- multi-agent-systems
- sdlc-automation
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle

## Summary
This paper reviews agentic AI across the software development life cycle and finds that adoption is strongest where outputs can be checked by tests, compilers, logs, or other executable signals.

## Problem
- Agentic AI research for software development is growing fast, but teams lack a consolidated view of where systems work in the SDLC, which designs recur, and which limits appear in industrial use.
- The problem matters because autonomous agents can affect code, tests, releases, and operations; weak evidence or unclear boundaries can create reliability and safety risks.
- Manual screening could not scale to the publication volume, with 1,609 initial candidate records across ACM, IEEE, Scopus, and Springer.

## Approach
- The authors ran a Kitchenham-style systematic literature review over peer-reviewed English publications from 2023 onward.
- They searched four sources, normalized records, removed duplicates, retrieved missing abstracts, and filtered records through quality control, screening, relevance selection, and manual review.
- They built a domain-agnostic multi-agent screening pipeline with Assistant and Evaluator agents, independent classifications, up to three rounds of disagreement dialogue, and inclusion as the default when conflicts remained.
- They manually checked the candidate set and extracted SDLC phase, evaluation context, architecture pattern, limitations, and mitigation strategies.

## Results
- The search started with 1,609 records, processed 1,331, kept 796 after quality control, screened 265, selected 127 as candidates, and ended with 92 manually verified primary studies.
- Of the 92 studies, 13 used industrial contexts and 79 were academic proof-of-concept studies, showing that most evidence still comes from controlled settings.
- The largest SDLC categories were Maintenance with 20 studies, Testing & QA with 18, Cross-cutting systems with 15, Deployment & Operations with 14, and Coding & Implementation with 12.
- Industrial studies clustered in verifiable later phases: Testing & QA had 5 industrial studies, Deployment & Operations had 2, while Coding & Implementation and Requirements Analysis had 0 industrial studies each.
- The dominant architecture was Planner-Executor-Reviewer role specialization, often with an Orchestrator; the Reviewer checks outputs through executable feedback such as tests, compiler output, logs, metrics, or CI/CD state.
- The screening pipeline produced 26 false positives after manual review; a 100-paper excluded sample found 1 false negative, with 0/50 in screening exclusions and 1/50 in relevance-selection exclusions, leading the authors to estimate about 7 missed relevant papers across 669 excluded records.

## Link
- [https://arxiv.org/abs/2605.15245v1](https://arxiv.org/abs/2605.15245v1)
