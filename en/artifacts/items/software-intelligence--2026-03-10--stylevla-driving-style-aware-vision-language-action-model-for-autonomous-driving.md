---
source: arxiv
url: http://arxiv.org/abs/2603.09482v1
published_at: '2026-03-10T10:33:58'
authors:
- Yuan Gao
- Dengyuan Hua
- Mattia Piccinini
- "Finn Rasmus Sch\xE4fer"
- Korbinian Moller
- Lin Li
- Johannes Betz
topics:
- autonomous-driving
- vision-language-action
- driving-style-control
- physics-informed-learning
- trajectory-generation
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# StyleVLA: Driving Style-Aware Vision Language Action Model for Autonomous Driving

## Summary
StyleVLA proposes a "driving-style-controllable" vision-language-action model for autonomous driving, and simultaneously constructs a dataset supporting five driving styles. Its core conclusion is: a lightweight specialized model combined with physics-constrained supervision can significantly outperform general-purpose closed-source VLM/VLA baselines on style-aware trajectory generation.

## Problem
- Existing autonomous driving datasets usually lack **explicit driving style annotations**, making it difficult for models to learn differentiated behaviors such as Comfort, Sporty, and Safety.
- Most existing VLA models learn only a **single generic driving policy** and cannot generate controllable trajectories according to a user-specified style, which affects personalization, comfort, and user acceptance.
- Many methods treat trajectory generation as **pure token prediction**, lacking explicit modeling of vehicle kinematic constraints, and therefore tend to produce physically implausible outputs.

## Approach
- Construct the **StyleVLA dataset**: based on CommonRoad and the Frenetix planner, style trajectories are generated for five styles (Default, Balanced, Comfort, Sporty, Safety) across 1,484 scenarios, and after statistical filtering the final dataset contains **1,216 scenarios, 76,030 BEV samples, and 42,084 FPV samples**.
- Generate supervision signals through **style-specific cost functions**: put simply, different weights are assigned to terms such as "speed, acceleration jerk, distance to obstacles, risk/visibility," allowing the planner to automatically produce trajectories with different driving styles in the same scenario.
- For the model, **Qwen3-VL-4B** is used as the base model, fine-tuned cost-effectively with **QLoRA**, and trajectory outputs are organized as structured JSON to predict the full kinematic state over the next 3 or 5 seconds.
- For the training objective, a **hybrid loss** is used: standard cross-entropy is responsible for generating discrete trajectory tokens, an additional MLP regression head handles continuous state regression, and a **physics-informed kinematic consistency loss (PIKC)** is added to constrain adjacent timestamps so that position, velocity/acceleration, and heading satisfy basic vehicle motion laws.

## Results
- In terms of dataset scale, the paper claims that StyleVLA contains **1,216 scenarios**, **76,030 BEV samples**, and **42,084 FPV samples**; the five styles are statistically distinguishable, for example **Sporty has the highest average speed at 7.32 m/s**, **Safety has the lowest average speed at 6.39 m/s**, and **Comfort has the lowest RMS jerk at 0.727 m/s³**.
- In the BEV ablation experiments, increasing training data from **4.5k→50k** continuously improves performance: ADE drops from **2.08 m to 1.17 m**, FDE from **5.43 m to 3.06 m**, PSR rises from **20.60% to 33.19%**, and Heading MAE from **0.073 to 0.035 rad**.
- In the loss-function ablation, based on the 50k training set, moving from **CE** to **CE+REG** reduces FDE from **3.82 m to 3.17 m** and increases PSR from **29.00% to 32.08%**; after adding **PIKC**, ADE further decreases from **1.21 m to 1.17 m**, FDE from **3.17 m to 3.06 m**, PSR rises to **33.19%**, and Heading MAE improves from **0.036 to 0.035 rad**.
- In the BEV benchmark comparison, the authors state that the fine-tuned **Qwen3-VL-4B** achieves a **39.47% success rate** on 2,000 test samples, while the best closed-source baseline reaches only **16.38%**; at the same time, inference time is about **1.92 s**, whereas some proprietary models require **more than 70 s** for a single inference.
- The composite style-driving score reported in the paper abstract shows that **StyleVLA achieves 0.55 (BEV) and 0.51 (FPV)**, significantly higher than **Gemini-3-Pro's 0.32 (BEV) and 0.35 (FPV)**. This composite score jointly considers success rate, physical feasibility, and adherence to the user-specified style.
- Based on this, the authors claim that a **specialized, lightweight, physics-aware** model can outperform general-purpose closed-source models on domain-specific tasks; this is the paper's most central breakthrough conclusion.

## Link
- [http://arxiv.org/abs/2603.09482v1](http://arxiv.org/abs/2603.09482v1)
