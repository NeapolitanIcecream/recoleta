---
source: arxiv
url: https://arxiv.org/abs/2606.13494v1
published_at: '2026-06-11T15:44:36'
authors:
- Daichi Azuma
- Taiki Miyanishi
- Koya Sakamoto
- Shuhei Kurita
- Yaonan Zhu
- Petr Khrapchenkov
- Motoaki Kawanabe
- Yusuke Iwasawa
- Yutaka Matsuo
topics:
- visual-navigation
- world-model
- diffusion-policy
- goal-conditioned-control
- robot-learning
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# NavWAM: A Navigation World Action Model for Goal-Conditioned Visual Navigation

## Summary
NavWAM solves goal-conditioned visual navigation by turning future prediction into direct action, so the robot can use visual foresight without a separate planner. It matters because navigation under partial observability needs both next-view prediction and action selection, and prior world models split those jobs.

## Problem
- Goal-conditioned image navigation must work from partial egocentric views, so the robot needs to predict how motion changes what it sees and whether that motion moves it toward the goal.
- Prior navigation world models predict future views, but they still depend on CEM-style planning or another external selector to choose actions.
- Direct navigation policies output actions efficiently, but they do not explicitly learn future egocentric prediction and goal-progress estimation in one model.

## Approach
- NavWAM is a diffusion-transformer policy built on Cosmos Predict2 that treats navigation as denoising one latent canvas.
- The canvas contains observed frames plus prediction frames for an action chunk, a future state, future egocentric views, and a goal-progress value.
- The model learns future view prediction, action generation, and value estimation together, instead of using separate heads or an external planner.
- At test time, it runs in policy mode and outputs an action chunk directly in a receding-horizon loop.
- It also supports optional best-of-N sampling, but the main results use default policy mode without CEM-style search.

## Results
- On go stanford, NavWAM beats planning baselines in trajectory error: ATE 0.324 vs 0.453 for NWM and 0.455 for Cosmos Predict2; RPE 0.099 vs 0.107 and 0.109.
- With fine-tuning on go stanford, NavWAM reaches ATE 0.192 and RPE 0.070, which the paper reports as its best navigation result on that benchmark.
- Future prediction stays useful after turning the model into a policy: subject consistency rises from 0.524 for NWM to 0.668 for NavWAM before fine-tuning, and stays at 0.635 after fine-tuning.
- On sit, NavWAM is competitive with OmniVLA despite using a 2B video backbone rather than OmniVLA's 7B OpenVLA backbone; it gets ATE 0.077 vs 0.086 at h=4 and 0.144 vs 0.162 at h=8, with SR 46.3% vs 45.4% at h=4 and 15.9% vs 12.1% at h=8.
- In real-robot tests on 24 episodes, NavWAM reaches the goal in 19/24 episodes, or 79.2%, compared with 14/24 for OmniVLA and 4/24 for NWM.

## Link
- [https://arxiv.org/abs/2606.13494v1](https://arxiv.org/abs/2606.13494v1)
