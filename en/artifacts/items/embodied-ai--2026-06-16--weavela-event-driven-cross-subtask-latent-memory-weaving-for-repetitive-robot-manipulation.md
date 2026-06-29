---
source: arxiv
url: https://arxiv.org/abs/2606.17463v1
published_at: '2026-06-16T03:25:34'
authors:
- Shoujing Zhu
- Zhenyang Liu
- Fungmiu Wang
- Jiafeng Wang
- Bo Yue
- Guiliang Liu
- Simo Wu
- Xiangyang Xue
- Taiping Zeng
topics:
- vision-language-action
- robot-memory
- repetitive-manipulation
- cross-subtask-conditioning
- robot-foundation-model
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# WeaveLA: Event Driven Cross-Subtask Latent Memory Weaving for Repetitive Robot Manipulation

## Summary
WeaveLA adds an event-driven latent memory channel to a frozen VLA policy so repetitive robot tasks can carry information from one completed sub-task into the next action segment. The strongest claim is on RoboMME SwingXtimes with N=3, where success rises from 0% to 47.8% with a pi_0.5 backbone.

## Problem
- Short-window VLA policies can execute single manipulation primitives, but they lose needed state across sub-task boundaries in repetitive tasks such as swing three times, place N objects, or press stop after a count.
- This matters because the current observation can be ambiguous: in SwingXtimes and StopCube, the correct next action depends on how many prior sub-goals were completed, not only on the visible scene.
- Prior memory methods often write every frame, retrieve demonstration stages, or trigger at events without passing a compact completed-subtask summary into the action expert.

## Approach
- WeaveLA writes memory only at sub-goal completion events during rollout. In the reported simulation experiments, the simulator supplies these boundaries, so the paper isolates the memory mechanism from boundary detection.
- A Query-driven Memory Weaver compresses the just-completed segment into 8 latent tokens with width 2048 using a single attention-pooling step over frozen VLA visual, text, and proprioceptive features.
- The latent tokens condition the next sub-task through the action-generation path, using memory cross-attention and AdaRMS modulation inside the Gemma action expert of pi_0.5.
- The base VLA stays mostly frozen; the trainable part is about 46M parameters on top of a roughly 3.4B-parameter base policy, or about 1.4% of the base size.
- Training uses staged action grounding, memory warmup, then semantic alignment and contrastive auxiliary losses with weights 0.05 and 0.02; sub-goal text is used only during training.

## Results
- On the six trained RoboMME tasks with pi_0.5 plus attention pooling, average success improves from 19.0% with Weaver off to 24.7% with Weaver on.
- At 16-task training scale, average success improves from 17.3% to 23.3%.
- On SwingXtimes at N=3, the hardest reported repetition slice, success improves from 0% to 47.8%; at 16-task scale the same slice improves from 4% to 30%.
- On pooled repetition tasks with N>=2 at 6-task scale, success improves from 7.2% to 24.6%, a 3.4x relative gain; at 16-task scale it improves from 5.8% to 17.4%, a 3.0x relative gain.
- Single-execution episodes with N=1 stay near 100% in both Weaver-on and Weaver-off settings, which supports the claim that gains come from cross-subtask memory rather than a general capacity increase.
- Additional reported localization results include StopCube improving from 8% to 22%, Hard episodes improving from 1.4% to 12.5%, and paired matched episodes where Weaver-on uniquely solves 13 vs. 1 SwingXtimes episodes and 8 vs. 1 StopCube episodes.

## Link
- [https://arxiv.org/abs/2606.17463v1](https://arxiv.org/abs/2606.17463v1)
