---
source: arxiv
url: https://arxiv.org/abs/2606.10825v1
published_at: '2026-06-09T13:09:21'
authors:
- Zakariae El Asri
- Philippe Gratias-Quiquandon
- Nicolas Thome
- Olivier Sigaud
topics:
- diffusion-policy
- model-based-rl
- world-model
- mpc
- robot-manipulation
- offline-to-online-rl
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# MODIP: Efficient Model-Based Optimization for Diffusion Policies

## Summary
MODIP is an offline-to-online method that improves robot diffusion policies with model-based planning, then trains the policy by supervised denoising on the planned trajectories. It targets the high cost and instability of direct RL fine-tuning for diffusion policies.

## Problem
- Diffusion policies can model multi-modal robot actions, but behavior cloning only copies the offline data and cannot improve beyond the demonstrations.
- Direct RL fine-tuning is costly because each action query requires a multi-step denoising chain.
- Hybrid MPC methods often score terminal states with Q(s, pi(s)); for a diffusion policy, that requires extra denoising at many terminal states during planning.

## Approach
- MODIP trains a latent world model with an encoder, latent dynamics model, reward model, terminal state-value function, and diffusion policy.
- During online control, MPPI samples action sequences from a hybrid proposal: diffusion-policy candidates plus Gaussian exploration candidates.
- The planner rolls candidates forward in latent space, scores them with predicted rewards plus a terminal state value V(z), and executes the best sequence in receding-horizon MPC.
- The planned trajectories are stored in replay and used as supervised targets for the diffusion policy with the same denoising behavior-cloning loss.
- Critic targets use next-state values instead of actions sampled from the current diffusion policy, which removes repeated denoising calls during critic updates.

## Results
- On D4RL/Kitchen Complete, MODIP reports 0.94 ± 0.14 success, above BC at 0.41 ± 0.20, DPPO at 0.88 ± 0.02, PA-RL at 0.85 ± 0.01, and TD-MPC2 at 0.65 ± 0.13.
- On D4RL/Kitchen Partial, MODIP reports 0.98 ± 0.01 success, above BC at 0.32 ± 0.06, DQL at 0.45 ± 0.03, DPPO at 0.67 ± 0.04, PA-RL at 0.93 ± 0.01, and TD-MPC2 at 0.55 ± 0.28.
- On D4RL/MuJoCo, MODIP reports 13775 ± 203 on halfcheetah, 6081 ± 66 on walker, and 3281 ± 370 on hopper; the corresponding BC scores are 5108 ± 730, 5721 ± 324, and 3050 ± 90.
- On RoboMimic, MODIP reports 0.98 ± 0.03 success on Lift and 0.92 ± 0.01 on Can; BC reports 0.95 ± 0.01 and 0.87 ± 0.04 on those tasks.
- PA-RL is higher than MODIP on halfcheetah in the shown table, 14254 ± 1564 versus 13775 ± 203, while DSRL is higher on RoboMimic Lift and Can, with 1.0 ± 0.0 and 0.94 ± 0.02 versus MODIP's 0.98 ± 0.03 and 0.92 ± 0.01.
- The excerpt states that terminal V(z) reduces planning cost and policy-independent critic targets reduce training cost, but it gives no wall-clock, inference-time, or denoising-call counts.

## Link
- [https://arxiv.org/abs/2606.10825v1](https://arxiv.org/abs/2606.10825v1)
