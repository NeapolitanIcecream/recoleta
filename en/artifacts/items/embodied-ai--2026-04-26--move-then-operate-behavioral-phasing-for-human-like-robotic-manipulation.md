---
source: arxiv
url: http://arxiv.org/abs/2604.23620v1
published_at: '2026-04-26T09:28:10'
authors:
- Haoming Xu
- Lei Lei
- Jie Gu
- Chu Tang
- Jingmin Chen
- Ruiqi Wang
topics:
- vision-language-action
- robot-manipulation
- mixture-of-experts
- data-efficiency
- contact-rich-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation

## Summary
Move-Then-Operate is a vision-language-action policy that splits robot manipulation into two phases: moving near the target and then doing the precise contact work. On RoboTwin2, this phased design beats a monolithic pi_0 policy by a large margin and reaches strong results with less data and fewer training steps.

## Problem
- Standard VLA manipulation policies learn coarse reaching and fine contact control with one policy, even though these behaviors have different action scales and dynamics.
- The paper argues that move segments dominate the data and gradients, which makes it harder to learn the smaller, contact-critical operate actions.
- This matters for high-precision manipulation because failures often happen in the final contact stage, where small action errors can break the task.

## Approach
- The method introduces a dual-expert policy: one expert for **move** and one for **operate**. A lightweight router picks one expert per action chunk.
- Both experts use Conditional Flow Matching to generate actions, but their parameters are separate, so coarse motion and precise manipulation do not share the same low-level action head.
- During training, the router is supervised with phase labels, and each example updates only the matching expert. That keeps gradient updates phase-specific.
- Phase labels are auto-generated with an MLLM-based segmentation pipeline that uses video, language instruction, subtask decomposition, and cues such as end-effector velocity.
- The model is built on a pre-trained pi_0-base backbone with separate LoRA adapters for the two experts and the shared vision-language backbone.

## Results
- On 8 RoboTwin2 tasks with **50 demonstrations per task** and identical training steps, the method reaches **68.88% average success**, versus **44.75%** for **pi_0**, **35.63%** for **RDT**, and **31.63%** for **ACT**. That is **+24.13 points** over pi_0.
- Per-task gains over **pi_0** include: **Click Alarmclock 88% vs 63% (+25)**, **Click Bell 99% vs 44% (+55)**, **Move Pillbottle pad 37% vs 21% (+16)**, **Place Bread Basket 34% vs 17% (+17)**, **Place Cans Plasticbox 79% vs 34% (+45)**, **Place Empty Cup 55% vs 37% (+18)**, **Place Burger Fries 89% vs 80% (+9)**, **Press Stapler 70% vs 62% (+8)**.
- Against data-rich baselines trained with **10x more data**, the method is competitive on several tasks: **Click Bell 99%** vs **75%** for **pi_0.5*** and **98%** for **GO-1***, and **Press Stapler 93%** vs **80%** and **66%**.
- The abstract claims the model reaches peak performance in **40% fewer training steps** than the standard full training budget.
- The excerpt gives concrete numbers for benchmark success rates and selected baseline comparisons, but it does not include full aggregate averages for the 10x-data comparison table or the detailed training-efficiency curve values.

## Link
- [http://arxiv.org/abs/2604.23620v1](http://arxiv.org/abs/2604.23620v1)
