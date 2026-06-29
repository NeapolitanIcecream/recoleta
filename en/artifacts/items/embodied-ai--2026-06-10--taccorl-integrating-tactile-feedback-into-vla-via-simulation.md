---
source: arxiv
url: https://arxiv.org/abs/2606.11743v1
published_at: '2026-06-10T07:20:36'
authors:
- Siyu Ma
- Yuqi Liang
- Chang Yu
- Yunuo Chen
- Hao Su
- Yixin Zhu
- Yin Yang
- Chenfanfu Jiang
topics:
- vision-language-action
- tactile-feedback
- sim2real
- robot-rl
- contact-rich-manipulation
- bimanual-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# TacCoRL: Integrating Tactile Feedback into VLA via Simulation

## Summary
TacCoRL adds tactile sensing to pretrained VLA robot policies and trains contact correction in simulation before real deployment. It targets bimanual contact-rich tasks where cameras miss local alignment and pressure cues.

## Problem
- Contact-rich manipulation tasks such as insertion, assembly, and puzzle placement need local contact state, but vision often cannot see misalignment, blockage, pressure, or contact location.
- Real robot demonstrations are expensive and mostly show successful nominal behavior, so they give weak supervision for near-failure contact states.
- Collecting many off-nominal contact rollouts on hardware can damage sensors and slows training because resets are costly.

## Approach
- The policy starts from a pretrained VLA backbone and adds tactile tokens from a recent tactile history window.
- A binary contact gate removes tactile tokens when readings look like background noise, so touch affects the policy mainly during contact.
- Sim-real co-training mixes real demonstrations with simulated teleoperation and MimicGen trajectories to warm-start tactile-conditioned actions.
- PPO reinforcement learning runs in a real-aligned simulator with sparse task rewards, while a supervised loss on real trajectories keeps the policy close to real robot observations and actions.
- The final policy deploys directly on the real robot without privileged simulator state or online real-world RL.

## Results
- Across 4 real-world bimanual contact-rich tasks, the final visuo-tactile policy reaches 72.5% average success, compared with 50.0% for the RL post-trained vision-only policy.
- Real-world task success after RL post-training is 70% on Test Tube Insertion, 45% on Do Puzzle, 95% on Assembly #1, and 80% on Assembly #2 for the visuo-tactile policy.
- On the same real tasks, vision-only RL post-training reaches 35%, 25%, 80%, and 60%, respectively.
- In simulation, RL with co-training raises average success to 78.5% for visuo-tactile policies and 60.5% for vision-only policies.
- Direct sparse-reward RL from the base VLA gets 0.0 success across all 4 simulated tasks, showing that co-training is needed before RL refinement.
- The ablation on Assembly #2 reports that real-data anchor weights β=0.1 and β=1.0 raise real-world success to 80%, while no anchor gives 45% under the same α=0.5 co-training ratio.

## Link
- [https://arxiv.org/abs/2606.11743v1](https://arxiv.org/abs/2606.11743v1)
