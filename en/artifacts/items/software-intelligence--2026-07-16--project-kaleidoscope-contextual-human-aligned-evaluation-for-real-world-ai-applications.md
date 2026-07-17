---
source: arxiv
url: https://arxiv.org/abs/2607.14673v1
published_at: '2026-07-16T07:38:39'
authors:
- Leanne Tan
- Rohan Jaggi
- Shaun Khoo
- Roy Ka-Wei Lee
topics:
- ai-evaluation
- llm-as-a-judge
- human-in-the-loop
- contextual-testing
- ai-governance
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# Project Kaleidoscope: Contextual, Human-Aligned Evaluation for Real-World AI Applications

## Summary
Kaleidoscope is an inspectable workflow for evaluating real-world AI applications against application-specific users, policies, and risk requirements. It combines persona-based test generation, configurable rubrics, human calibration, and reliability-gated LLM judging rather than treating general benchmarks or uncalibrated automated scores as sufficient.

## Problem
- Public benchmarks often fail to represent a deployed application’s users, workflows, policies, knowledge base, and risk tolerance, while manual evaluation is slow and difficult to scale.
- Teams need reliable functional evaluation to determine whether application responses satisfy local requirements, especially in organizational and public-sector settings.
- Uncalibrated LLM judges can produce biased or inconsistent scores, so automated results need reviewable human reference labels and local reliability checks.

## Approach
- Define a target application profile, then generate representative tests across personas, typical or edge cases, knowledge-base scope, input style, and language.
- Let users select preset rubrics or define custom criteria at the claim or response level; the system uses one metric per judge prompt and can augment loosely specified criteria into structured prompts.
- Collect human labels on a calibration subset through an assisted review interface, while requiring reviewers to select rubric labels rather than simply accept a model suggestion.
- Create three candidate LLM judges per rubric and measure each judge against human labels; aggregate only judges whose local Macro F1 exceeds 0.5, using majority voting and exposing disagreements for error analysis.

## Results
- A three-week pilot covered 4 organizational use cases, 8 testers, approximately 12 evaluation runs, 180 generated test cases, and 40 human-reviewed outputs across 3 application snapshots; 6 of 8 pilot users completed the questionnaire.
- 83% of questionnaire respondents, or 5 of 6 users, said Kaleidoscope helped them evaluate applications more efficiently, and all respondents said they considered judge reliability scores when interpreting automated results.
- Formative judge and rubric experiments used 108 annotated question-answer pairs spanning 4 domains and 14 evaluation dimensions; the paper reports that generic rubric insertion was unreliable across metrics and that combining multiple rubric dimensions in one judge prompt substantially degraded performance.
- Pilot feedback led to concrete workflow changes, including revised test allocation, added input-style variation, web-search grounding for sparse application context, multi-judge guidance, and flexible data import and export.
- The evidence is early and does not establish evaluation correctness or superiority over manual evaluation or existing tools: the pilot was uncontrolled, small, and limited to four use cases, while the scores remain local to the chosen rubric, test set, human labels, and reliability threshold.

## Link
- [https://arxiv.org/abs/2607.14673v1](https://arxiv.org/abs/2607.14673v1)
