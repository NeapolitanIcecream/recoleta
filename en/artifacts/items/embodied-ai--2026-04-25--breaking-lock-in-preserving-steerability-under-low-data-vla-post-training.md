---
source: arxiv
url: http://arxiv.org/abs/2604.23121v1
published_at: '2026-04-25T03:18:07'
authors:
- Suning Huang
- Jiaqi Shao
- Ke Wang
- Qianzhong Chen
- Jiankai Sun
- Yanjiang Guo
- Mac Schwager
- Jeannette Bohg
topics:
- vision-language-action
- robot-foundation-models
- low-data-post-training
- instruction-following
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training

## Summary
DeLock targets a common failure in low-data post-training of vision-language-action policies: after fine-tuning on a narrow demo set, the robot learns the task but stops following new instructions. It preserves the model's pre-trained visual grounding during fine-tuning and adds a test-time prompt-contrast rule that steers action generation toward a new instruction.

## Problem
- Low-data supervised fine-tuning can cause **lock-in**: the policy overfits to the post-training demos and ignores novel instructions even when it knows the underlying concepts from pretraining.
- The paper splits this into **concept lock-in** (fixation on trained objects or attributes) and **spatial lock-in** (fixation on trained locations or relations such as left/right or upper/lower).
- This matters because collecting broad robot demonstration coverage is expensive, so practical adaptation often happens with only 80-100 demos per task and narrow instruction coverage.

## Approach
- **Visual encoder drift regularization:** during post-training, DeLock adds an L2 penalty on the visual encoder weights relative to the pre-trained model, with objective `L_BC + λ||θ_v - θ_v^pre||^2`, to keep visual grounding from collapsing onto the narrow fine-tuning distribution.
- **Contrastive Prompt Guidance (CPG):** at test time, the same flow-based policy is run with a novel prompt `τ+` and a trained prompt `τ-`, then their denoising vector fields are combined as `v_CPG = v(τ-) + w(v(τ+) - v(τ-))` to push action generation toward the novel instruction.
- The trained prompt acts as a negative condition because it captures the post-training bias; the novel prompt is the positive condition.
- The method does not rely on extra supervision, external foundation-model labels, auxiliary losses, or augmented datasets.
- The evaluation suite includes 8 tasks: 4 LIBERO simulation tasks with 100 demos each and 4 DROID real-world tasks with 80 demos each, designed to test concept and spatial lock-in directly.

## Results
- On the 8-task evaluation with **20 trials per task**, DeLock reports strong performance across OOD-location and novel-instruction tests: **T1 16/20**, **T4 OOD 15/20**, **T2[C] 19/20**, **T3[C] 19/20**, **T4[C] 17/20**, **T5[S] 11/20**, **T6[S] 13/20**, **T7[S] 14/20**, **T8[C+S] 13/20**.
- Against the low-data baseline **RETAIN**, DeLock is better on every novel-prompt task shown in Table 2. Examples: **T2 19/20 vs 0/20**, **T5 11/20 vs 0/20**, **T7 14/20 vs 2/20**, **T8 13/20 vs 1/20**.
- Against the high-resource reference **π0.5-DROID**, DeLock matches or exceeds it on several reported real-world novel-instruction tasks: **T4[C] 17/20 vs 18/20**, **T7[S] 14/20 vs 11/20**, **T8[C+S] 13/20 vs 0/20**. The paper frames this as reaching or beating a state-of-the-art generalist policy that used much more curated post-training data.
- Ablations show both parts matter. Removing visual regularization drops performance sharply, for example **T2 19/20 → 9/20** and **T8 13/20 → 0/20**. Removing CPG keeps some concept performance but fails on spatial lock-in tasks: **T5/T6/T7/T8 = 0/20, 0/20, 0/20, 0/20** without CPG, versus **11/20, 13/20, 14/20, 13/20** with full DeLock.
- Freezing the visual encoder is weaker than regularized adaptation: **Frozen-Vis** gets **T5 2/20**, **T6 11/20**, **T7 8/20**, **T8 4/20**, below full DeLock on the same tasks.
- The paper also gives qualitative evidence that standard fine-tuning collapses vision-language attention onto trained targets, while DeLock shifts attention and denoising trajectories in line with the new prompt.

## Link
- [http://arxiv.org/abs/2604.23121v1](http://arxiv.org/abs/2604.23121v1)
