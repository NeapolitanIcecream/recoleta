---
source: arxiv
url: https://arxiv.org/abs/2606.23127v1
published_at: '2026-06-22T10:14:11'
authors:
- Julia Belikova
- Rauf Parchiev
- Evgeny Egorov
- Grigorii Davydenko
- Gleb Gusev
- Andrey Savchenko
- Maksim Makarenko
topics:
- llm-agents
- procedural-memory
- agent-benchmarks
- skill-transfer
- software-engineering
- enterprise-workflows
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation

## Summary
AFTER is a 382-task benchmark for testing whether LLM-agent procedural memory becomes reusable skill knowledge across tasks, roles, and model backbones. The paper finds that skill updates can improve workplace-agent accuracy and token cost, but narrow updates can overfit to one role or model.

## Problem
- LLM agents often repeat workplace procedures such as editing spreadsheets, querying databases, processing PDFs, configuring infrastructure, and writing tests, so reusable procedural memory could reduce repeated trial-and-error.
- Existing agent benchmarks usually measure task completion in one setting and do not separate local improvement from transfer across tasks, roles, or model backbones.
- This matters for production agents because a skill that works only where it was learned can raise maintenance cost and fail when users, workflows, or models change.

## Approach
- The authors build AFTER with 382 realistic enterprise tasks, 6 professional roles, and 22 procedural skills across documents, data operations, ML/AI, infrastructure, and software engineering.
- Each task has fixed skill annotations, which lets the benchmark test skill quality without mixing in retrieval errors.
- They evaluate two properties: specificity, meaning improvement in the source context, and generality, meaning transfer to held-out tasks, other roles, or other models.
- Skills are stored as versioned `SKILL.md` artifacts. Evolution collects execution traces, diagnoses failures, revises the skill text, and promotes or rolls back versions.
- The experiments compare no-skill prompts, handcrafted skills, LLM-generated skills, one-round refinement, and several trace-based memory update systems.

## Results
- AFTER contains 382 tasks: 318 single-skill tasks and 64 multi-skill workflows, across 6 roles and 22 skills.
- Static procedural skills improve full-pass accuracy by +2.8 points on average over no-skill baselines; individual aggregate gains in Table 2 range from +0.4 to +5.3 points across listed models.
- One LLM-guided refinement round adds +3.7 to +6.7 aggregate M2 points across model scales, with the paper reporting a +5.2-point average gain.
- Cross-model transfer is strongest when skills are evolved from diverse multi-model traces: 73.1% test accuracy versus 36.0% to 59.4% for single-model trace sources, a gain of at least +13.7 points over the best single-model source.
- In framework-guided evolution on pdf, xlsx, and pptx tasks with Qwen3.5-35B-A3B, Hermes gains +18.0 test M1 under diverse traces, while some methods with large train gains lose test accuracy, such as EvoSkill at +14.9 train and -2.7 test under narrow traces.
- Cross-role transfer can hurt: for the pdf skill, in-role evolution gains +11.7 points for PM and +6.2 for DS, while transferring the evolved skill across those roles loses -4.8 to -7.5 points. On one Kafka Lag Anomaly Detection task, evolved skills reduce token use by 326k tokens for Claude and 48k for Hermes.

## Link
- [https://arxiv.org/abs/2606.23127v1](https://arxiv.org/abs/2606.23127v1)
