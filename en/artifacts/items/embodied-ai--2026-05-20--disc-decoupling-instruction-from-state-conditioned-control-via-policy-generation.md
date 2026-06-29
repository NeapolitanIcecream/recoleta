---
source: arxiv
url: https://arxiv.org/abs/2605.20856v1
published_at: '2026-05-20T07:45:50'
authors:
- Hanxiang Ren
- Pei Zhou
- Xunzhe Zhou
- Yanchao Yang
topics:
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
- language-grounding
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# DISC: Decoupling Instruction from State-Conditioned Control via Policy Generation

## Summary
DISC makes the language instruction generate a task-specific visuomotor policy, so the control policy receives observations only. The paper claims this separation improves language grounding and task success in simulated and real robot manipulation.

## Problem
- Language-conditioned robot policies often mix instruction tokens and observations in shared parameters, which lets scene cues drive actions even when the instruction asks for something else.
- This matters because robot datasets often reuse scenes and objects, so a policy can learn scene-to-action shortcuts that fail when the same scene supports several tasks.
- Long-horizon tasks suffer more because one missed language-conditioned subgoal can break the full episode.

## Approach
- DISC encodes the instruction with a frozen language encoder, then a hypernetwork generates the full parameter set of a task-specific visuomotor policy.
- The generated policy receives RGB and proprioceptive observations, then predicts actions. It has no direct language input during control.
- The hypernetwork has two stages: a Weight Initialization Network maps the instruction embedding to initial policy weights, and an Iterative Refinement Module updates those weights over learned feed-forward steps.
- The refinement module copies the shape of optimization, with learned forward, pseudo-gradient, and update operations, without computing gradients at inference time.
- Training uses behavior cloning end to end: action error updates the hypernetwork through the generated policy.

## Results
- On LIBERO-90, DISC reports 94.3% success using 50 demonstrations per task, with a 7.7 percentage-point gain over the strongest trained-from-scratch entangled baseline.
- On Meta-World ML45, DISC reports 92.2% success using 100 expert demonstrations per task.
- DISC reports higher LIBERO-90 success than pretrained π₀ at 91.6%, while staying below π₀.₅ at 95.7%.
- On a real-world 3 object × 3 container benchmark with 9 language-conditioned tasks sharing the same visual context, DISC reports 86.4% success versus 78.5% for the best entangled baseline.
- The paper also claims better few-shot adaptation, paraphrase handling, and task clustering in generated parameter space, but the excerpt does not provide the exact numbers for those claims.

## Link
- [https://arxiv.org/abs/2605.20856v1](https://arxiv.org/abs/2605.20856v1)
