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
- compliance-control
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Contact-Grounded Policy: Dexterous Visuotactile Policy with Generative Contact Grounding

## Summary
CGP targets contact-rich manipulation for multi-finger dexterous hands. Its core idea is to first represent the “desired contact” as a joint trajectory of future robot states and tactile signals, and then map that trajectory into target states executable by a low-level compliance controller. Rather than treating tactile sensing as merely an extra input, it explicitly binds tactile feedback to control execution, thereby improving stability and success rates in complex contact tasks.

## Problem
- Existing dexterous manipulation policies often predict only kinematic trajectories, making it difficult to explicitly represent and maintain continuously changing multi-point contacts; as a result, slip, overly hard contact, or unstable execution can easily occur.
- Although many tactile methods use tactile observations, they do not model how the “predicted contact” is actually realized through a low-level compliance/PD controller.
- This matters because contact outcomes in multi-finger hands depend strongly on object geometry, friction changes, and slip; if the policy output is inconsistent with controller dynamics, real-world manipulation success drops significantly.

## Approach
- Proposes **Contact-Grounded Policy (CGP)**: instead of directly regressing actions, it predicts joint trajectories of future **actual robot state** and **tactile feedback**.
- Uses a **conditional diffusion model** to generate future trajectories in a compressed tactile latent space; tactile signals are first compressed with a VAE with KL regularization to reduce the cost of high-dimensional tactile generation and stabilize training.
- Learns a **contact-consistency mapping** that maps the predicted “state + tactile” pair into **target robot states** executable by the low-level compliance controller, making it more likely for the controller to reproduce the intended contact.
- This mapping predicts target-state offsets in a **residual form**, which is more robust than direct regression; at test time, it uses receding-horizon replanning to execute predicted targets step by step.

## Results
- On **5 contact-rich tasks**, CGP outperforms baseline diffusion policies across the board (Table II).
- **Simulated In-Hand Box Flipping (60 demos)**: CGP **66.0%**, above Visuotactile DP **58.0%** and Visuomotor DP **53.2%**.
- **Simulated Fragile Egg Grasping (100 demos)**: CGP **74.8%**, above Visuotactile DP **70.0%** and Visuomotor DP **53.2%**.
- **Simulated Dish Wiping (100 demos)**: CGP **58.4%**, above Visuotactile DP **43.6%** and Visuomotor DP **42.4%**.
- **Real Jar Opening (45 demos)**: CGP **93.3%**, significantly above Visuotactile DP **66.7%** and Visuomotor DP **73.3%**.
- **Real In-Hand Box Flipping (90 demos)**: CGP **80.0%**, above both baselines at **60.0%**. Another ablation shows that for hand-configuration prediction, the residual mapping with `State+Tactile` achieves an MAE of **5.94±0.20 ×10^-3 rad**, outperforming state-only **10.64±0.38**, tactile-only **12.15±0.20**, and absolute regression **8.80±0.24**.

## Link
- [http://arxiv.org/abs/2603.05687v2](http://arxiv.org/abs/2603.05687v2)
