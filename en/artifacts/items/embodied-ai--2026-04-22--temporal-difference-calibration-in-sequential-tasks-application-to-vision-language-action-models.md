---
source: arxiv
url: http://arxiv.org/abs/2604.20472v1
published_at: '2026-04-22T11:58:05'
authors:
- Shelly Francis-Meretzki
- Mirco Mutti
- Yaniv Romano
- Aviv Tamar
topics:
- vision-language-action
- uncertainty-calibration
- temporal-difference-learning
- robot-failure-detection
- sequential-decision-making
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models

## Summary
This paper defines calibration for sequential tasks where success is known only at the end of an episode, then shows that the best calibrated predictor is the policy’s value function. It uses temporal-difference learning to train that predictor for vision-language-action models and reports better calibration and failure detection than prior methods on simulation and real-robot data.

## Problem
- Standard calibration methods fit single-step prediction problems, but robot episodes have delayed labels: the task succeeds or fails only after a sequence of actions.
- For VLA policies, action-level confidence can be misleading for rollout success because some uncertain actions are irrelevant to the final outcome.
- Reliable success confidence matters for safety, early failure detection, and black-box use of foundation models where internal features may be hidden behind an API.

## Approach
- The paper defines a **sequential Brier score**: at time step \(t\), predict the probability that the full episode will succeed, then score that prediction against the final binary success label.
- It proves that, for binary episodic success, the risk minimizer of this sequential Brier objective matches the policy’s expected future return or value function.
- Based on that link, it trains a success predictor with **temporal-difference calibration (TDQC)**: each step’s prediction is pushed toward the next step’s prediction, and the final step is tied to the episode success label.
- The method can use either internal VLA features (white-box) or only the policy’s action probabilities over time (black-box), which matters when hidden states are unavailable.
- The paper compares TDQC against cross-entropy or Monte Carlo style training used by prior work such as SAFE.

## Results
- The paper claims TD-based methods **consistently outperform** conventional binary-cross-entropy predictors on unseen validation tasks across all shown benchmark/model settings in Figure 1, measured by **sequential Brier score** over **time quantiles** and averaged over **21 random seeds**.
- It claims TDQC using only **action probabilities** can **match or improve** SAFE-style predictors that use internal hidden features, which matters for black-box VLA APIs. The excerpt does not provide exact Brier values.
- It reports **state-of-the-art early detection** results on **LIBERO** for **OpenVLA, π0, π0-FAST, and UniVLA**, and on a **Franka real-robot dataset** collected with **π0-FAST**. The excerpt names Table 2 for these results but does not include the numerical values.
- As a policy improvement by-product, using the learned value predictor to rank sampled actions gives a **15% increase in success rate for OpenVLA on LIBERO**.
- The excerpt gives broader context that unseen-task VLA success rates are often **30% to 60%** in prior reports, which explains why better calibrated success prediction is useful, but those numbers are background rather than TDQC gains from this paper.

## Link
- [http://arxiv.org/abs/2604.20472v1](http://arxiv.org/abs/2604.20472v1)
