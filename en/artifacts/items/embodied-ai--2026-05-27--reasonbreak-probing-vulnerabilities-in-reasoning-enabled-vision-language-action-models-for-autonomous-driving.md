---
source: arxiv
url: https://arxiv.org/abs/2605.29114v1
published_at: '2026-05-27T21:21:37'
authors:
- Mohammadreza Teymoorianfard
- Jean-Philippe Monteuuis
- Jonathan Petit
- Amir Houmansadr
topics:
- vision-language-action
- autonomous-driving
- vla-safety
- adversarial-robustness
- closed-loop-simulation
- reasoning-models
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# ReasonBreak: Probing Vulnerabilities in Reasoning-Enabled Vision-Language-Action Models for Autonomous Driving

## Summary
ReasonBreak shows that small, meaning-preserving text corruptions can change reasoning and driving trajectories in NVIDIA Alpamayo VLA driving models. The paper tests this in black-box open-loop and closed-loop settings and links failures to collisions, off-road driving, and wrong-lane events.

## Problem
- Reasoning-enabled VLA driving systems use text instructions together with sensor input, so speech-to-text and preprocessing noise can change the text surface form.
- Changes in intermediate reasoning can affect generated trajectories, which matters because driving errors can cause collisions or traffic-rule violations.
- Prior VLA vulnerability work mainly studied manipulation tasks or models without explicit reasoning outputs, leaving reasoning-enabled autonomous driving less tested.

## Approach
- The attack changes only the textual input while keeping the visual input fixed. Allowed corruptions include capitalization changes, word scrambling, and character-level noise that preserve the intended command.
- The threat model is query-based black-box: the attacker sees model outputs but has no access to parameters, logits, architecture, or internal states.
- Open-loop tests use Best-of-N perturbed queries to estimate how much the model can be manipulated under search.
- Closed-loop tests use one random corrupted text input per simulator step in AlpaSim, then measure how errors accumulate during driving.
- The evaluation checks semantic reasoning fields, reasoning length inflation, missing reasoning outputs, trajectory deviation, collision rate, near-encounter rate, time-to-collision, off-road rate, and wrong-lane rate.

## Results
- On 195 open-loop samples, Alpamayo1 semantic reasoning ASR reaches 0.889 for relation, 0.850 for implication, 0.832 for planning, 0.765 for object, and 0.836 overall.
- Alpamayo1.5 is harder to attack in open-loop tests, with semantic reasoning ASR of 0.626 for relation, 0.520 for implication, 0.436 for object, 0.429 for planning, and 0.422 overall.
- Open-loop structural attacks also work: Alpamayo1 has 0.248 slowdown ASR and 0.047 DoS ASR; Alpamayo1.5 has 0.102 slowdown ASR and 0.088 DoS ASR.
- Open-loop trajectory deviation ASR is 0.336 for Alpamayo1 and 0.115 for Alpamayo1.5, using ADE degradation against ground truth.
- In closed-loop simulation on 50 clips, the paper reports up to 72% ASR for trajectory manipulation and up to 62% ASR for semantic reasoning manipulation.
- The paper reports weak correlation between reasoning shifts and trajectory deviations, plus higher collision, off-road, and wrong-lane failures under successful attacks.

## Link
- [https://arxiv.org/abs/2605.29114v1](https://arxiv.org/abs/2605.29114v1)
