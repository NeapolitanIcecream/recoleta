---
source: arxiv
url: https://arxiv.org/abs/2607.05659v1
published_at: '2026-07-06T22:00:27'
authors:
- Yunyan Ding
- Thomas Zimmermann
- Iftekhar Ahmed
topics:
- multi-agent-systems
- llm-agents
- software-engineering
- code-generation
- code-review
- persona-prompting
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Agents with Feelings? Personality and Emotion in Multi-Agent Software Teams

## Summary
This paper tests whether personality and emotion prompts change performance and behavior in LLM agent teams for software engineering.

## Problem
- Multi-agent software engineering systems usually vary agent roles and workflows, leaving behavior profiles under-tested.
- The problem matters because profile prompts can change pass rates, review outputs, revision loops, and token cost in agentic coding systems.

## Approach
- Builds agent personas from Big Five traits, six emotions, O*NET work styles, and task roles.
- Tests shared-profile teams, where all agents get the same profile, and mixed-profile teams, where roles get different profiles.
- Uses a Planner, Implementer, and Reviewer for code generation; uses two Writers and one Supervisor for code review.
- Evaluates 78 team-profile configurations: 54 shared-profile configurations and 24 mixed-profile configurations.
- Runs four instruction-tuned LLMs on 659 task instances: 282 LiveCodeBench v6 lite code-generation problems and 377 Hydra-Reviewer code-review instances.

## Results
- The study covers 4 LLMs, 2 tasks, 78 profile configurations per model-task pair, and 659 sampled task instances.
- For code generation, the best and worst shared-profile configurations differ by 7.1 to 11.3 percentage points in pass@1 across models.
- The best mixed-profile configuration beats the best shared-profile configuration in 6 of 8 model-task settings.
- Fear and high-conscientiousness profiles produce more revision activity, more over-revision, and higher token usage, with no consistent performance gain.
- The excerpt gives no detailed BLEU-4 values for code review; its strongest concrete claim is that profile choice changes reference alignment and collaboration behavior.

## Link
- [https://arxiv.org/abs/2607.05659v1](https://arxiv.org/abs/2607.05659v1)
