---
source: arxiv
url: http://arxiv.org/abs/2603.10980v1
published_at: '2026-03-11T17:10:16'
authors:
- Zixing Wang
- Devesh K. Jha
- Ahmed H. Qureshi
- Diego Romeres
topics:
- diffusion-policy
- robot-learning
- inference-time-guidance
- multiple-instance-learning
- imitation-learning
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# PPGuide: Steering Diffusion Policies with Performance Predictive Guidance

## Summary
PPGuide is a method for guiding robotic diffusion policies at inference time: it first automatically identifies which observation-action segments are most likely to lead to success or failure, then uses the gradient of a lightweight classifier to “push” the policy away from failure modes. Its significance is that it can improve the robustness of long-horizon manipulation tasks without requiring dense rewards, a world model, or additional expert demonstrations.

## Problem
- Although diffusion policies excel at learning multimodal robotic manipulation, small errors in generated actions can accumulate over time and cause long-horizon tasks to fail.
- Existing improvement methods usually rely on more expert data, dense rewards, or world models, which are costly, hard to obtain, or computationally expensive in real-world settings.
- The core difficulty is that only sparse trajectory-level final labels (success/failure) are available, yet actionable fine-grained guidance signals are needed for each time step.

## Approach
- Proposes **PPGuide**: **inference-time guidance** for a trained diffusion policy, without changing the policy architecture or retraining the main policy.
- First collects rollouts from the base policy at different training stages, treats each full trajectory as an MIL “bag,” where each observation-action chunk is an “instance,” and trains an attention-based MIL model using only binary final success/failure labels.
- The MIL model automatically locates the most critical segments through attention weights and self-labels instances into three classes: **success-relevant (SR)**, **failure-relevant (FR)**, and **irrelevant (IR)**; the paper notes that the number of IR instances is more than **10×** that of SR/FR.
- Then trains a lightweight three-class guidance classifier that takes observation-action pairs as input and outputs the probability of belonging to SR/FR/IR; at inference time, it takes gradients with respect to the action to increase SR probability and decrease FR probability, thereby modifying the diffusion denoising process.
- To reduce overhead, the authors use **alternating guidance**, applying guidance only at some denoising steps, and claim that its performance is close to constant guidance applied at every step while being more computationally efficient.

## Results
- Across multiple tasks in **Robomimic** and **MimicGen**, and using only **10%** of the original expert demonstrations to train the base policy, PPGuide overall “consistently outperforms or matches” the base diffusion policy (DP) and several variants.
- **Square** task: DP improves from **62%/58%** (epoch 500/550) to PPGuide **72%/66%**, gains of **+10 / +8** percentage points respectively; PPGuide-CG reaches **72%/68%**, showing that alternating guidance is close to constant guidance.
- **Transport** task: DP **60%/68%** improves to PPGuide **68%/76%**, gains of **+8 / +8** percentage points respectively; PPGuide-CG is **68%/74%**.
- **Mug Cleanup D1**: DP **26%/26%** improves to PPGuide **30%/36%**, gains of **+4 / +10** percentage points respectively.
- **Coffee D2**: DP **54%/46%** improves to PPGuide **58%/58%**, gains of **+4 / +12** percentage points respectively; **Kitchen D1** goes from **52%/40%** to **52%/44%** (**+0 / +4**).
- There are also inconsistent improvements: for example, on **Stack Three D1** at epoch 550, DP is **30%** while PPGuide is **28%** (**-2**); in heterogeneous base-policy evaluation, **Transport 1500** drops from **74%** to **70%** (**-4**). The strongest gains appear in heterogeneous evaluation: **Transport 1300** improves from **56%** to **74%** (**+18**), and **Square 1300** from **54%** to **70%** (**+16**).

## Link
- [http://arxiv.org/abs/2603.10980v1](http://arxiv.org/abs/2603.10980v1)
