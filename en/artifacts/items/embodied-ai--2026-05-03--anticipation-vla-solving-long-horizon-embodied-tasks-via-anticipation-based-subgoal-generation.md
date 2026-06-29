---
source: arxiv
url: https://arxiv.org/abs/2605.01772v1
published_at: '2026-05-03T08:11:35'
authors:
- Zhilong Zhang
- Wenyu Luo
- Haonan Wang
- Yifei Sheng
- Yidi Wang
- Hanyuan Guo
- Haoxiang Ren
- Xinghao Du
- Yuhan Che
- Tongtong Cao
- Lei Yuan
- Yang Yu
topics:
- vision-language-action
- generalist-robot-policy
- long-horizon-planning
- subgoal-generation
- robot-manipulation
- world-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation

## Summary
Anticipation-VLA adds adaptive subgoal generation to a goal-conditioned VLA policy for long-horizon robot tasks. It improves simulated manipulation results and reports larger gains in real-world unseen settings.

## Problem
- Standard VLA policies often fail on long-horizon tasks because small action errors compound across many steps.
- Fixed subtask decompositions can be too coarse or too fine for the current state, so they may fail to guide execution when the robot stalls or the scene changes.
- This matters for household and mobile manipulation tasks where the robot must complete several dependent stages under language or image goals.

## Approach
- The system keeps a stack of active goals and subgoals. A high-level anticipation model proposes the next reachable subgoal, and a low-level VLA policy acts toward it.
- The anticipation model first generates a text subgoal, then predicts a matching subgoal image. An inverse dynamics check rejects image subgoals whose inferred instruction does not match the text subgoal.
- A value model classifies progress as goal achieved, progress improved, or progress stalled. This classification triggers goal popping, continued execution, or recursive subgoal refinement.
- The authors implement the high-level model with Bagel, a unified multimodal model, and implement the low-level policy by finetuning a goal-conditioned $\pi_{0.5}$-style flow-matching VLA.
- Training uses hierarchical datasets for anticipation, value classification, and goal-conditioned action prediction.

## Results
- On Libero one-trajectory SFT, Anticipation-VLA reaches 80.8 average success, compared with 76.8 for $\pi_{0.5}$, 76.0 for $\pi_{0.5}$+VLM, 64.6 for $\pi_0$, 27.3 for DreamVLA, and 21.5 for UniVLA.
- On Libero-Long, the main long-horizon suite, Anticipation-VLA scores 63.2, compared with 54.6 for $\pi_{0.5}$ and 53.2 for $\pi_{0.5}$+VLM.
- On VLABench Hammer Nail & Hang Picture, Anticipation-VLA reaches 56.3 process reward and 4.2 success rate, compared with 47.9 and 2.1 for $\pi_{0.5}$+VLM.
- In real-world tests on Arx-X5, the paper uses 100 demonstrations for Rearrange Objects and 200 for Spell Words, with 40 rollouts per task split into 20 seen and 20 unseen configurations.
- The excerpt gives no exact real-world success rates, but reports +60% gains in seen configurations and +107% in unseen configurations over the baselines. It also says Anticipation-VLA is the only tested model with non-zero success on unseen Spell Words.

## Link
- [https://arxiv.org/abs/2605.01772v1](https://arxiv.org/abs/2605.01772v1)
