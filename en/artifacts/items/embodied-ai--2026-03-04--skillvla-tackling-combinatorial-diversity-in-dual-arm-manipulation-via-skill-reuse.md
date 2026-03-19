---
source: arxiv
url: http://arxiv.org/abs/2603.03836v1
published_at: '2026-03-04T08:38:27'
authors:
- Xuanran Zhai
- Zekai Huang
- Longyan Wu
- Qianyou Zhao
- Qiaojun Yu
- Jieji Ren
- Ce Hao
- Harold Soh
topics:
- vision-language-action
- dual-arm-manipulation
- skill-reuse
- combinatorial-generalization
- robot-foundation-model
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse

## Summary
SkillVLA studies the problem of "combinatorial diversity" in bimanual robots: many dual-arm tasks are actually different combinations of left- and right-hand single-arm skills, but existing VLAs usually entangle the actions of both arms, making it difficult to recombine learned skills. The paper proposes a hierarchical, skill-adaptive bimanual VLA that enables the robot to reuse single-arm skills and activate bimanual collaboration only when needed.

## Problem
- Existing bimanual VLAs often directly predict concatenated joint actions, which causes left- and right-arm skills to become **entangled** and limits the model to reproducing action pairings seen during training.
- Bimanual tasks exhibit clear **combinatorial explosion**: if the left and right hands each learn multiple skills, the number of possible combinations can grow approximately quadratically, making it impossible to teach and learn them one by one.
- This matters because if a general-purpose bimanual robot cannot flexibly recombine existing single-arm skills, it will struggle to scale to new tasks, long-horizon tasks, and continual learning scenarios.

## Approach
- Proposes a **two-level reasoning** framework: a high-level VLM first uses visual/language input to generate subtask text prompts separately for the left and right arms, explicitly decomposing what each arm should do.
- At the low level, separate action-generation streams are built for the left and right arms, each producing actions based on its corresponding prompt and observations, thereby supporting direct recombination of learned single-arm skills under novel left-right pairings.
- For tasks that truly require tight coordination, it introduces **adaptive cross-arm communication**: the two action streams exchange information through cross-attention, but the communication strength is controlled by a cooperation estimator.
- The cooperation estimator outputs a scalar lpha∈[0,1] (denoted as alpha in the paper), and learns when bimanual coupling is needed and when decoupling should be maintained by comparing behavior cloning errors with communication turned "on" versus "off."
- It further incorporates VLM priors, temporal smoothing, and conservative communication regularization, and can discretize the cooperation gate to 0/1 to improve inference stability.

## Results
- On **9 unseen skill recombination tasks**, SkillVLA achieves an average success rate of **0.51**, while **π0.5 = 0.0**, **π0-FAST = 0.0**, and **TwinVLA = 0.04**, showing clear combinatorial generalization to unseen left-right skill pairings.
- On specific recombination tasks, SkillVLA scores **Cup×Cake 0.7, Cup×Stir 0.4, Cup×Smash 0.5, Box×Cake 0.6, Box×Stir 0.4, Box×Smash 0.5, Mug×Cake 0.6, Mug×Stir 0.3, Mug×Smash 0.6**; the main baselines are nearly all **0.0**.
- On **learned skills** evaluation, SkillVLA averages **0.78**, comparable to **π0.5 at 0.77**, and better than **π0-FAST at 0.70** and **TwinVLA at 0.67**, indicating that its improved recombination ability does not significantly harm performance on known skills.
- The paper also claims performance competitive with baselines on **three categories of highly cooperative tasks**, suggesting that adaptive communication can still represent tightly coordinated bimanual behavior, though the excerpt does not provide specific numbers.
- In **two multi-stage long-horizon tasks**, SkillVLA can automatically determine cooperation requirements by stage, and reduces execution time by **21%** through parallelizable recomposable skills; the excerpt does not provide the full baseline table values.
- The paper further claims that in **continual learning with limited demonstrations**, skill reuse can significantly help acquire new skills, but the excerpt does not provide quantitative results.

## Link
- [http://arxiv.org/abs/2603.03836v1](http://arxiv.org/abs/2603.03836v1)
