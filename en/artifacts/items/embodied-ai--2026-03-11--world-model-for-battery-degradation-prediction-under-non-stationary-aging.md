---
source: arxiv
url: http://arxiv.org/abs/2603.10527v1
published_at: '2026-03-11T08:30:15'
authors:
- Kai Chin Lim
- Khay Wai See
topics:
- battery-degradation
- world-model
- state-of-health
- time-series-forecasting
- physics-informed-learning
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# World Model for Battery Degradation Prediction Under Non-Stationary Aging

## Summary
This paper formulates long-horizon battery state-of-health (SOH) forecasting as a "world model" problem: first compressing the raw voltage/current/temperature sequence of each cycle into a latent state, then using learned dynamics to roll forward step by step and predict the next 80 cycles. The core conclusion is that this iterative rollout clearly outperforms direct regression, while physics constraints mainly help prediction near the degradation knee.

## Problem
- The goal is to predict the SOH trajectory of lithium-ion batteries over multiple future cycles, rather than just a single-point estimate at the current time.
- Although existing data-driven methods can directly regress an entire trajectory, they lack a mechanism for "pushing the degradation process forward step by step," making them prone to learning an average slope and struggling to capture non-stationary aging.
- This matters because battery lifetime management, maintenance decisions, and safety assessment all depend on reliable forecasts of the future degradation path rather than a single-point value.

## Approach
- The raw **V/I/T** time series of each cycle is fed into a shared 1D CNN to extract a per-cycle embedding; PatchTST is then used to encode a latent degradation state `z(k)` over a 30-cycle historical window.
- An MLP dynamics transition module with residual connections maps the current latent state together with the charging-current condition to the next-cycle latent state; after repeated iteration, it rolls out a future latent trajectory over 80 steps.
- The same decoder head maps both the current latent state and future rollout states to SOH, thereby outputting both the current SOH and the future SOH sequence.
- Physics-constrained losses are added as soft regularization, including a monotonic non-increasing SOH constraint, a consistency constraint between internal resistance and SOH, and a voltage consistency constraint, to test whether physics priors can improve the learned dynamics.
- Three configurations are evaluated in an ablation study: a physics-informed world model (PIWM), a world model without physics constraints (WM), and a CNN-PatchTST that removes rollout in favor of direct regression; additional control experiments are conducted with LSTM and EWC continual learning.

## Results
- On the Severson LFP dataset of **138 cells**, the world model achieves better overall accuracy than direct regression with the same encoder: **MAE drops from 0.0078 to 0.0063**, a relative improvement of about **24%** (CNN-PatchTST vs PIWM/WM).
- Key future-trajectory forecasting result: at **h=5**, PIWM has an MAE of **0.0067**, WM **0.0065**, while direct-regression CNN-PatchTST has **0.0136**; that is, rollout roughly **halves** the short-term prediction error.
- Error in the rollout models increases with prediction horizon, consistent with true iterative forecasting behavior: PIWM rises from **h5=0.0067** to **h50=0.0109**, and WM from **0.0065** to **0.0096**; by contrast, direct regression remains almost constant at **0.0133–0.0136**, suggesting it behaves more like outputting an average degradation slope.
- The physics constraint **does not improve overall MAE**: both PIWM and WM have an overall **MAE of 0.0063**; however, it helps during the degradation-knee stage (Stage 2, SOH 0.95–0.90), where **Stage 2 MAE decreases from 0.0098 to 0.0080**.
- The physics constraint is instead slightly worse in later-stage degradation: in Stage 3, WM has **MAE=0.0135**, outperforming PIWM's **0.0185**; overall, it looks more like a local regularizer than a means of improving global accuracy.
- In the continual-learning control experiment, the authors state that **EWC accuracy is 3.3 times worse than joint training**; the paper also notes that if the Fisher information is computed after convergence, EWC becomes almost ineffective, and the Fisher must be computed during mid-training to activate the mechanism. The excerpt does not provide a complete test table, but gives an example EWC result of **test MAE=0.021**.

## Link
- [http://arxiv.org/abs/2603.10527v1](http://arxiv.org/abs/2603.10527v1)
