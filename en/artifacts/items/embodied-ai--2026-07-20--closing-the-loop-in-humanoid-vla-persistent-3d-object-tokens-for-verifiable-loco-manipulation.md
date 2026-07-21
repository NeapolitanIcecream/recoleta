---
source: arxiv
url: https://arxiv.org/abs/2607.18016v1
published_at: '2026-07-20T14:52:46'
authors:
- Peng Ren
- Haoyang Ge
- Jiang Zhao
- Cong Huang
- Yukun Shi
- Pei Chi
- Kai Chen
topics:
- robot-foundation-model
- vision-language-action
- humanoid-loco-manipulation
- object-centric-grounding
- execution-verification
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Closing the Loop in Humanoid VLA: Persistent 3D Object Tokens for Verifiable Loco-Manipulation

## Summary
POT-VLA gives a humanoid VLA policy persistent, role-indexed 3D object tokens that support both action generation and physical execution verification. On a Unitree G1, it raises matched task success from 39/80 to 71/80 across eight real-world loco-manipulation task families.

## Problem
- Long-horizon humanoid tasks require the robot to track the same objects through walking, grasping, contact, occlusion, placement, and recovery.
- The paper addresses object-state divergence: the object representation used to choose an action can differ from the state used to verify whether the physical goal was achieved, causing wrong-object actions, premature subtask completion, and ineffective recovery.
- This matters because metric 3D relations such as containment, support, alignment, and handover distance determine whether a manipulation actually succeeded.

## Approach
- Persistent Object Tokenization (POT) converts RGB-D observations into role-indexed 3D records for entities such as TARGET, DESTINATION, SUPPORT, and HANDOVER_PARTNER. The default representation uses 8 slots with 33 features per slot, including position, extent, visibility, confidence, and spatial relations.
- POT-VLA inserts these object tokens into the GR00T-N1.7 whole-body action head, while keeping the same Unitree G1 embodiment, action representation, and runtime as the matched direct baseline.
- After each short-horizon action chunk, the system refreshes the same object memory and applies geometric predicates to determine whether the intended relation holds.
- Predicate outcomes trigger continued execution, retry, re-observation, re-grounding, or replanning; uncertain object evidence does not count as confirmed task completion.

## Results
- In 80 real-world trials spanning eight task families, POT-VLA achieved 71/80 successes versus 39/80 for the matched direct GR00T-N1.7 baseline.
- The largest task-level improvements were cup stacking (8/10 versus 1/10), garment transport to a basket (9/10 versus 3/10), drawer/tray interaction (8/10 versus 4/10), and two-ball placement (9/10 versus 5/10).
- On a four-task ablation subset, the direct baseline achieved 15/40, verifier-only achieved 22/40, POT tokens only achieved 31/40, and the full system achieved 34/40, indicating that token conditioning supplied most of the gain while verification added further improvement.
- Under object-state shifts, POT-VLA scored 9/10 on novel object instances, 9/10 on shifted layouts, 9/10 with distractors, and 8/10 under mid-execution perturbations, compared with 6/10, 5/10, 8/10, and 4/10 for the direct baseline.
- In an external Being-0-aligned reference that was not a local reproduction, POT-VLA achieved 44/50 successes versus 37/50 reported by the Being-0 paper.

## Link
- [https://arxiv.org/abs/2607.18016v1](https://arxiv.org/abs/2607.18016v1)
