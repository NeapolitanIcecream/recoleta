---
source: arxiv
url: https://arxiv.org/abs/2606.09630v1
published_at: '2026-06-08T15:29:09'
authors:
- Haodi Hu
- Chung-Ta Huang
- Jing Liu
- Ye Wang
- Kei Suzuki
- Matthew Brand
- Toshiaki Koike-Akino
topics:
- vision-language-action
- robot-failure-recovery
- residual-rl
- vlm-reward-compilation
- sim2real
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies

## Summary
ReCoVLA trains recovery policies for failed robot manipulation states while keeping the base vision-language-action policy frozen. A VLM identifies the failure type and recovery stage, then a reward compiler builds the residual-RL reward used in simulation before zero-shot physical deployment.

## Problem
- VLA manipulation policies can fail after off-distribution states such as dropped objects, wrong receptacle placement, lost grasps, or unfinished contact-rich steps.
- Fine-tuning the full VLA needs recovery demonstrations and can damage existing skills; generic RL rewards are often sparse or activate reward terms in the wrong order.
- The problem matters because a robot that completes nominal tasks still needs targeted correction when execution goes wrong.

## Approach
- The base VLA stays frozen. During recovery, a residual policy adds a corrective action to the VLA action.
- Qwen3-VL-8B-Instruct analyzes rollout images and the instruction, then outputs a structured descriptor: failure category, recovery stage, active entities, confidence, and reward mask.
- A deterministic compiler maps the descriptor to simulator reward terms for distance progress, grasp state, placement progress, and articulation closing progress.
- Stage gates activate reward terms only after required preconditions hold, such as enabling placement reward after the object is grasped.
- Residual policies are trained with PPO in simulation over VLA latent features, then selected on the real robot when the VLM detects a known failure category.

## Results
- In simulation across three Fetch tasks, ReCoVLA raises average success from 36.7% for the no-recovery π0.5 baseline to 66.7%; average Q-score rises from 0.56 to 0.83.
- In physical zero-shot sim-to-real tests, ReCoVLA reaches 61.7% average success and 0.75 average Q-score, with a reported 18.3-point success gain and 0.21 Q-score gain over baselines.
- The stage-gated method beats the VLM-selected, ungated reward ablation: M3 gets 48.3% simulation success, 18.4 points below ReCoVLA.
- Task-level simulation gains include toolbox organization from 25% to 60% success and vegetable sorting from 30% to 65% success.
- On OpenVLA, the same recovery design improves average simulation success from 23.3% for the base policy to 45.0%.
- In OOD object substitutions, the no-recovery baseline gets 10.0% success and 0.22 Q-score; ReCoVLA gets 53.3% success and 0.65 Q-score.

## Link
- [https://arxiv.org/abs/2606.09630v1](https://arxiv.org/abs/2606.09630v1)
