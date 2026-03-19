---
source: arxiv
url: http://arxiv.org/abs/2603.11110v1
published_at: '2026-03-11T11:27:08'
authors:
- Jseen Zhang
- Gabriel Adineera
- Jinzhou Tan
- Jinoh Kim
topics:
- world-model
- visual-rl
- model-based-rl
- continuous-control
- residual-action
- dmcontrol
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# ResWM: Residual-Action World Model for Visual RL

## Summary
ResWM proposes a modification to world models for visual reinforcement learning: instead of directly predicting absolute actions, it predicts "residual actions" relative to the previous action. This turns control into smooth small-step adjustments and, combined with adjacent observation difference encoding, improves sample efficiency, long-horizon planning stability, and action smoothness.

## Problem
- Existing visual world models usually condition directly on **absolute actions**, which forces policy optimization to deal with task-dependent, non-stationary, and high-variance action distributions, often causing unstable training.
- In continuous control and robotics settings, this setup often leads to **action jitter/oscillation**, accumulated long-horizon planning errors, and inefficient control, affecting safety and energy consumption.
- This problem matters because data for visual RL and robotics is expensive; if the world model is unstable, it undermines the core value of model-based RL in sample efficiency and real-world deployment.

## Approach
- Reparameterize actions as **residual actions**: the policy first predicts an increment \(\delta a_t\), which is then combined with the previous action to obtain the current action \(a_t=\tanh(a_{t-1}+\delta a_t)\). Intuitively, the model only makes a "small correction" at each step instead of re-guessing the full action every time.
- In the latent dynamics of the world model, use **residual actions rather than absolute actions** to drive state transitions and imagination rollouts, so that both planning and policy learning operate in the same smoother action space.
- Propose an **Observation Difference Encoder (ODL)** that directly encodes the difference between adjacent frames \(o_t-o_{t-1}\), extracting "environmental changes" rather than static content, yielding a more compact dynamic representation better matched to residual control.
- Keep the Dreamer-style RSSM framework largely unchanged, and claim **no additional hyperparameters** are needed; together with KL regularization on residual actions and an optional energy penalty, this suppresses overly large and jittery control updates.

## Results
- On **6 common DMControl tasks at 100K steps**, ResWM achieves an average score of **828.7**, higher than **DeepRAD 695.1**, **RAD 663.6**, **DeepMDP 460.5**, and **pixel SAC 167.3**.
- On **6 common DMControl tasks at 500K steps**, ResWM achieves an average score of **925.0**, higher than **DeepRAD 890.8**, **RAD 872.5**, **DeepMDP 764.6**, and **pixel SAC 216.8**.
- Single-task examples: **Reacher Easy @100K**, ResWM **942 ± 43**, outperforming **DeepRAD 792 ± 77** and **RAD 894 ± 32**; **Finger Spin @100K**, ResWM **986 ± 86**, outperforming **DeepRAD 832 ± 101**.
- The relevant passage also claims that, in a broader comparison, ResWM reaches a DMControl average score of **925.0**, surpassing **TACO 887.1** and **MaDi 885.1**; on difficult tasks, it achieves an average of **644.8 vs. ResAct 630.2** at **1M steps**.
- The paper also claims that action trajectories are more stable, smoother, and more energy-efficient, and that long-horizon prediction error is smaller; however, in the provided excerpt, there is **no more detailed explicit quantitative table** for **action smoothness/energy consumption**.

## Link
- [http://arxiv.org/abs/2603.11110v1](http://arxiv.org/abs/2603.11110v1)
