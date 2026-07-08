---
source: arxiv
url: https://arxiv.org/abs/2607.06256v1
published_at: '2026-07-07T13:24:37'
authors:
- Ke Rui
- Yushen Zuo
- Jiawei Wang
- Haoran Jia
- Jinming Ma
- Weitao Zhou
- Minglei Li
topics:
- semantic-handoff
- vision-language-action
- skill-composition
- behavior-1k
- robot-diagnostics
- long-horizon-manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Diagnosing Semantic Handoff Failures in Agent-Orchestrated Vision-Language-Action Skill Composition

## Summary
The paper identifies semantic handoff failures in long-horizon VLA skill composition: a skill can pass its own check yet leave a state where the next skill cannot start. It introduces a BEHAVIOR-1K execution harness that runs π0.5-based skills with typed arguments, step budgets, multi-view VLM verification, retries, replanning, and trace logging.

## Problem
- Long-horizon household tasks require robots to chain navigation, grasping, placement, door, and appliance skills while preserving the state needed by the next skill.
- Standard skill evaluation starts each skill from clean demonstration snapshots, so it can miss failures caused by chained terminal states: shifted poses, displaced objects, poor camera views, or ambiguous object instances.
- This matters for robot foundation models because high isolated skill success can still produce near-zero full-task success when skill boundaries are weak.

## Approach
- The system wraps VLA skills in typed contracts: skill name, object arguments, language prompt, step budget, verifier interval, and expected postcondition.
- It trains a compact π0.5-based skill library on cleaned BEHAVIOR-1K demonstrations, using pooled all-skill mid-training followed by skill-group specialization.
- During execution, an agent runs a plan-act-verify-replan loop. Every 200 simulator steps, Gemini 2.5 Flash checks head and wrist camera views against the current postcondition.
- Navigation checks include an arm-reach readiness condition, so the agent advances only when the next skill has a plausible start state.
- The evaluation compares the same checkpoints from clean skill-boundary snapshots and from chained states produced by previous skills.

## Results
- Isolated snapshot skill success is high for several skills: move_to 27/35 (77.1%), pick_up_from 28/29 (96.5%), place_in 11/13 (84.6%), place_on 6/6 (100.0%), open_door 7/7 (100.0%), close_door 4/6 (66.7%), and turn_on_switch 7/8 (87.5%).
- End-to-end task predicate success is described as near zero, so the paper reports progress through reference skill sequences across 30 rollouts instead.
- Mean progress across 10 BEHAVIOR-1K tasks and 3 instances per task is 19.5%. The best tasks are Turn on radio at 50.0% ± 43.3 and Make microwave popcorn at 45.8% ± 7.2; Hide Easter eggs is 0.0% ± 0.0.
- In one representative 10-rollout round with 196 verifier calls, the harness records 130 failed skill attempts: 31 grasp control failures, 15 actuation failures, 12 placement failures, 37 target-grounding or scene-search failures, and 35 navigation-to-ready failures.
- Tightening the navigation verifier to require arm-reach readiness surfaces 12 additional readiness failures, triggers 25 more re-navigation attempts, and recovers the radio task in the reported ablation.
- A blinded human audit judged 20 of 21 adjudicable verifier-flagged failures as real, with an over-strict error rate of 0.05; category counts still come from the verifier and are preliminary.

## Link
- [https://arxiv.org/abs/2607.06256v1](https://arxiv.org/abs/2607.06256v1)
