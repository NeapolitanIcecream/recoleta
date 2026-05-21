---
source: arxiv
url: https://arxiv.org/abs/2605.05241v1
published_at: '2026-05-03T17:29:29'
authors:
- Zijian Zeng
- Fei Ding
- Huiming Yang
- Xianwei Li
- Yuhao Liao
topics:
- sim2real
- dexterous-manipulation
- vision-language-models
- domain-randomization
- visuo-tactile-policy
- robot-foundation-models
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation

## Summary
DexSim2Real trains dexterous robot policies in simulation and transfers them to a real Franka Panda with an Allegro Hand by using a vision-language model to tune simulation randomization.

## Problem
- Sim-trained dexterous manipulation policies often fail on real robots because visual appearance, physics, camera pose, friction, mass, and sensor signals differ between simulation and hardware.
- Standard domain randomization needs hand-tuned ranges and can train on unrealistic simulated worlds, which hurts contact-rich tasks such as insertion, in-hand rotation, tool use, and pouring.
- The problem matters because dexterous hands need reliable zero-shot transfer to reduce real-world data collection, manual tuning, and unsafe trial-and-error on hardware.

## Approach
- FM-DR uses GPT-4V as a visual realism critic: it scores rendered simulation images against real reference images on a 1–10 scale for lighting, texture, geometry, and physical plausibility.
- CMA-ES optimizes a Gaussian-mixture distribution over simulation parameters, including friction, mass scaling, lighting, texture noise, and camera pose noise; an entropy term keeps variation in the training distribution.
- TVCAP encodes RGB, tactile readings, and proprioception with separate encoders, then uses bidirectional cross-attention so vision can attend to touch and touch can attend to vision during contact.
- PSC uses an LLM to split a natural-language task into sub-skills, raises task difficulty when sub-skill success exceeds 0.8, and chains skills once success exceeds 0.9.
- The final policy is trained with PPO in Isaac Sim and deployed directly on the real robot without real demonstrations for the sim-to-real methods.

## Results
- On six real-world tasks with 50 trials per task and 3 seeds, DexSim2Real reports 78.2% average success. The table reports 66.1% for Act3D with 100 real demonstrations, 65.1% for DrEureka, 59.2% for DeXtreme, 54.2% for ADR, and 45.2% for Vanilla DR.
- Task success rates for DexSim2Real are 92.3% Pick-Place, 85.7% Stacking, 78.4% Peg Insertion, 71.2% In-Hand Rotation, 67.8% Tool Use, and 73.5% Pouring.
- The average sim-to-real gap is 8.3% for DexSim2Real, compared with 28.5% for Vanilla DR and 19.2% for ADR.
- Ablations report 65.8% without FM-DR using Vanilla DR, 69.3% without FM-DR using ADR, 70.1% without tactile input, 72.4% with concatenation instead of cross-attention, and 68.9% without PSC.
- FM-DR raises average VLM realism score from 4.2/10 to 7.8/10, reduces friction mean error from 0.35 to 0.08, and cuts entropy by 18% relative to uniform randomization.
- The paper reports that FM-DR needs about 200–300 VLM queries per task, uses CMA-ES with population size 16 for 50 generations, and adds about 2 GPU-hours of overhead.

## Link
- [https://arxiv.org/abs/2605.05241v1](https://arxiv.org/abs/2605.05241v1)
