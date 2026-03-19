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
- visual-rl
- model-based-rl
- world-models
- continuous-control
- residual-actions
- robotics
relevance_score: 0.35
run_id: materialize-outputs
language_code: en
---

# ResWM: Residual-Action World Model for Visual RL

## Summary
ResWM addresses the instability of world model learning in visual continuous control by rewriting actions from “absolute actions” to “residual actions relative to the previous step,” in order to achieve smoother and more stable control. It also models dynamic changes using differences between adjacent observations, and reports better sample efficiency and final returns than Dreamer, TD-MPC, and several pixel-based RL baselines on DMControl.

## Problem
- Existing visual model-based RL typically conditions future predictions directly on absolute actions, but the optimal absolute action distribution is task-dependent and unknown a priori, leading to high-variance optimization and unstable long-horizon planning.
- This modeling approach can easily produce oscillatory or jittery control, which in robotics and continuous control settings can cause inefficiency, high energy consumption, and even safety risks.
- Purely static frame encoding retains a large amount of redundant background information, making it harder to capture the temporal dynamics that truly drive control changes.

## Approach
- Replace the control variable in both the policy and the world model from absolute actions to residual actions: the policy predicts an increment \(\delta a_t\), and the final action is \(a_t=\tanh(a_{t-1}+\delta a_t)\).
- In the Dreamer-style RSSM, both latent dynamics and reward prediction are conditioned directly on residual actions rather than absolute actions, so that imagination rollout and policy optimization use the same action representation.
- Propose an Observation Difference Encoder, which extracts dynamic changes through adjacent-observation feature differences \(f(o_t)-f'(o_{t-1})\), forming a more compact latent representation naturally matched to residual control.
- Add a KL prior constraint on residual actions during actor optimization, and optionally include an energy penalty \(\|\delta a_t\|_2^2\) to suppress excessively large or jittery control updates.
- The method claims to require only minimal modifications to a Dreamer-style framework and introduces no additional hyperparameters.

## Results
- On 6 common DMControl tasks, ResWM achieves an average score of **828.7** at **100K steps**, higher than **DeepRAD 695.1**, **RAD 663.6**, **DeepMDP 460.5**, and **pixel SAC 167.3**.
- On the same 6 tasks, ResWM achieves an average score of **925.0** at **500K steps**, higher than **DeepRAD 890.8**, **RAD 872.5**, **DeepMDP 764.6**, and **pixel SAC 216.8**.
- On individual tasks at 100K, ResWM reaches **Cartpole 845** (vs DeepRAD **703**), **Reacher 942** (vs **792**), **Cheetah 542** (vs **453**), **Walker 694** (vs **582**), **Finger 986** (vs **832**), and **Ball-in-cup 963** (vs **809**).
- At 500K, ResWM reaches **Cartpole 882** (vs DeepRAD **870**), **Reacher 986** (vs **942**), **Cheetah 783** (vs **721**), **Walker 957** (vs **925**), **Finger 964** (vs **932**), and **Ball-in-cup 978** (vs **954**).
- The paper also claims to outperform **ResAct** in comparisons against stronger baselines (for example, a hard-task 1M steps average of **644.8 vs 630.2**), and to exceed **TACO 887.1** and **MaDi 885.1**; however, these results are not fully presented in the provided excerpt.
- Beyond returns, the paper claims that ResWM can also produce smoother, more stable, and more energy-efficient action trajectories, and reduce long-horizon prediction error; however, the excerpt does not provide explicit quantitative metrics for action smoothness or energy consumption.

## Link
- [http://arxiv.org/abs/2603.11110v1](http://arxiv.org/abs/2603.11110v1)
