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
- robot-learning
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse

## Summary
SkillVLA studies the problem of “combinatorial diversity” in dual-arm robots: existing VLAs often learn dual-arm actions in a tied-together manner, making it impossible to freely recombine previously learned left- and right-arm skills for new tasks. The paper proposes a hierarchical, skill-adaptive dual-arm VLA framework that significantly improves success rates on unseen skill combinations while preserving collaboration ability.

## Problem
- Existing dual-arm VLAs typically predict concatenated joint actions for both arms directly, which easily leads to **skill entanglement**: left- and right-arm skills become bound together and are hard to recombine.
- Dual-arm tasks exhibit **combinatorial diversity**: if each arm has multiple skills, the number of possible combinations can grow rapidly, and learning every combination one by one is both inefficient and unscalable.
- This matters because real-world bimanual manipulation includes both independently parallel combinations of single-arm skills and tightly coordinated dual-arm skills; without skill reuse, generalization and continual learning are both limited.

## Approach
- Proposes **SkillVLA**: a two-level reasoning design that separates “what skill to choose” from “how to generate actions.” At the high level, it first generates natural-language subtask descriptions for the left and right arms separately, serving as recomposable skill representations.
- At the low level, it uses separate VLM streams and action experts for the two arms to generate actions; when a task requires collaboration, it then passes information between arms through **adaptive cross-attention**.
- Introduces a **collaboration estimator** that outputs collaboration strength \(\alpha\in[0,1]\), deciding when to decouple the two arms and when to enable coupled communication, thereby switching between single-arm skill reuse and dual-arm collaboration.
- Trains the collaboration estimator using the difference in behavior cloning errors between “communication enabled” and “communication disabled”: if communication reduces BC loss, \(\alpha\) is increased; otherwise it is decreased.
- Combined with VLM priors, temporal smoothing, conservative communication regularization, and optional discrete gating to improve the stability of collaboration-level decisions.

## Results
- On **9 unseen skill recombination tasks**, SkillVLA achieves an average success rate of **0.51**, while **\(\pi_{0.5}\)=0.0**, **\(\pi_{0}\)-FAST=0.0**, and **TwinVLA=0.04**; the paper describes this as a breakthrough in combinatorial generalization from nearly **0%** to **51%**.
- On specific recombination tasks, SkillVLA achieves **Cup×Cake 0.7, Cup×Stir 0.4, Cup×Smash 0.5, Box×Cake 0.6, Box×Stir 0.4, Box×Smash 0.5, Mug×Cake 0.6, Mug×Stir 0.3, Mug×Smash 0.6**, substantially outperforming baselines that are almost entirely near zero overall.
- On **previously learned skills**, SkillVLA achieves an average success rate of **0.78**, comparable to **0.77 for \(\pi_{0.5}\)**, and higher than **0.70 for \(\pi_{0}\)-FAST** and **0.67 for TwinVLA**, showing that it does not gain recomposition ability by sacrificing execution of base skills.
- The paper also claims competitive performance with baselines on **3 highly collaborative tasks**, indicating that adaptive communication can still express tight dual-arm coordination; however, no specific numeric table is provided in the excerpt.
- In **2 long-horizon multi-stage tasks**, SkillVLA accelerates execution by recombining skills in stages that can be parallelized, with **execution time reduced by 21%**; the excerpt does not provide finer-grained task-level numbers.
- The paper also claims substantially better performance in **continual learning / few-shot new skill acquisition** settings, but the excerpt does not provide quantitative results.

## Link
- [http://arxiv.org/abs/2603.03836v1](http://arxiv.org/abs/2603.03836v1)
