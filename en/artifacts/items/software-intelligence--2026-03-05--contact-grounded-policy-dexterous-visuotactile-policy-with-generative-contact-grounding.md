---
source: arxiv
url: http://arxiv.org/abs/2603.05687v2
published_at: '2026-03-05T21:22:49'
authors:
- Zhengtong Xu
- Yeping Wang
- Ben Abbatematteo
- Jom Preechayasomboon
- Sonny Chan
- Nick Colonnese
- Amirhossein H. Memar
topics:
- dexterous-manipulation
- visuotactile-policy
- diffusion-policy
- contact-modeling
- robot-learning
relevance_score: 0.29
run_id: materialize-outputs
language_code: en
---

# Contact-Grounded Policy: Dexterous Visuotactile Policy with Generative Contact Grounding

## Summary
This paper proposes Contact-Grounded Policy (CGP) for joint visuotactile control in multi-finger dexterous manipulation. The key idea is to first predict future robot states and tactile feedback, then convert them into target states that a low-level compliance controller can execute, so that the “desired contacts” can actually be realized.

## Problem
- Multi-finger dexterous manipulation depends on continuously changing multi-point contacts and is heavily affected by object geometry, friction transitions, and slip, making it difficult to complete tasks robustly using vision alone or purely kinematic prediction.
- Prior tactile policies typically treat touch as an additional input only, lacking modeling of the “contact state itself” and of “how policy outputs are executed by low-level compliance/PD controllers.”
- As a result, the model may be able to predict actions or tactile signals, but those outputs may not reproduce the target contacts in real closed-loop control, leading to slip, overly rigid contact, and unreliable execution.

## Approach
- CGP formulates the problem as **contact grounding**: instead of directly outputting actions, it first predicts coupled trajectories of the **actual robot state** and **tactile feedback** over a future time horizon.
- It contains two core modules: (1) a conditional diffusion model that jointly generates future states and tactile signals in a compressed tactile latent space; and (2) a contact-consistency mapping that converts the predicted “state + tactile” pair into target robot states executable by a compliance controller.
- The contact-consistency mapping learns a data-driven mapping tied to a specific robot, sensor, and controller, avoiding the need to manually define contact points, contact modes, or explicit dynamics.
- To efficiently generate high-dimensional tactile signals, the authors first use a VAE with KL regularization to compress tactile data, and then perform diffusion prediction in the latent space; this design applies to both dense tactile arrays in simulation and vision-based tactile images in real systems.

## Results
- Across 5 contact-rich tasks, CGP outperforms two diffusion policy baselines (Visuotactile DP and Visuomotor DP).
- Simulation In-Hand Box Flipping (60 demos): CGP **66.0%**, higher than Visuotactile DP **58.0%** and Visuomotor DP **53.2%**.
- Simulation Fragile Egg Grasping (100 demos): CGP **74.8%**, higher than Visuotactile DP **70.0%** and Visuomotor DP **53.2%**.
- Simulation Dish Wiping (100 demos): CGP **58.4%**, higher than Visuotactile DP **43.6%** and Visuomotor DP **42.4%**.
- Real-world Jar Opening (45 demos): CGP **93.3%**, significantly higher than Visuotactile DP **66.7%** and Visuomotor DP **73.3%**; real-world In-Hand Box Flipping (90 demos): CGP **80.0%**, higher than both baselines at **60.0%**.
- In the ablation on hand configuration prediction for the contact-consistency mapping, the best “State+Tactile + ResNet1D + Residual” MAE is **5.94±0.20 ×10^-3 rad**, better than the absolute prediction under the same setting at **8.80±0.24**, and also better than state-only residual prediction at **10.64±0.38**, showing that both tactile input and residual modeling are effective.

## Link
- [http://arxiv.org/abs/2603.05687v2](http://arxiv.org/abs/2603.05687v2)
