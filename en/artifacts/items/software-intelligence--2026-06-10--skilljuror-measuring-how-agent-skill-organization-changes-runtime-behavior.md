---
source: arxiv
url: https://arxiv.org/abs/2606.11543v1
published_at: '2026-06-10T01:11:50'
authors:
- Zhiyu Chen
- Zihan Guo
- Bo Huang
- Bingwei Lu
- Jianghao Lin
- Yuanjian Zhou
- Weinan Zhang
topics:
- agent-skills
- llm-agents
- skill-evaluation
- runtime-behavior
- procedural-knowledge
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior

## Summary
SkillJuror tests whether rearranging the same Agent Skill content changes how an LLM agent acts at runtime. On 82 SkillsBench tasks, Progressive Disclosure increased resource use inside trajectories and gave a small pass-rate gain over a flat Skill baseline.

## Problem
- Agent Skill benchmarks often compare different Skills, which mixes content coverage, author style, helper availability, and organization.
- This matters because teams need evidence for how to write Skills, not only whether adding Skills helps.
- The paper studies whether Skill organization alone can change agent search, resource access, implementation, checking, and repair behavior.

## Approach
- SkillJuror builds two matched versions of each Skill: a normalized flat baseline and a Progressive Disclosure version with a short `SKILL.md` that points to support files.
- Both versions keep the same task scope, commands, helper contracts, constraints, numeric thresholds, schemas, and output rules.
- The system checks variants with deterministic gates, rubric-based semantic audits, and human review for flagged cases.
- It runs matched trials in the same Harbor-backed sandbox, with the same model, task environment, verifier, timeout, and reasoning setting.
- It measures verifier pass rate, cost, time, token use, resources touched, and Effective Resource Uptake, where uptake means the agent used a resource in implementation, validation, correction, or blocker diagnosis.

## Results
- Main runtime study: 82 SkillsBench tasks × 3 conditions × 5 trials = 1,230 trials; each condition has 410 trials.
- Pass rate improved from 172/410 for the flat baseline, 42.0%, to 189/410 for Progressive Disclosure, 46.1%, a gain of 17 verifier-passing trials or +4.1 percentage points.
- No-Skill scored 119/410, 29.0%, so both Skill variants outperformed the no-Skill condition on aggregate pass rate.
- Distinct Skill resources touched per trajectory rose from 1.18 with the flat baseline to 3.85 with Progressive Disclosure.
- Effective Resource Uptake events rose from 1.33 to 3.92 per trajectory.
- Yield-normalized efficiency changed from 20.1 minutes/pass, 0.22M tokens/pass, and $1.28/pass for the baseline to 17.8 minutes/pass, 0.21M tokens/pass, and $1.31/pass for Progressive Disclosure; gains were task-dependent and weaker for exact output conventions, numeric thresholds, and long artifact-generation pipelines.

## Link
- [https://arxiv.org/abs/2606.11543v1](https://arxiv.org/abs/2606.11543v1)
