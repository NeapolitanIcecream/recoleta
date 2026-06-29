---
source: arxiv
url: https://arxiv.org/abs/2606.13578v1
published_at: '2026-06-11T17:03:53'
authors:
- Baochang Ren
- Xinjie Liu
- Xi Chen
- Yanshuo Liu
- Chenxi Li
- Daqi Gao
- Zeqin Su
- Jintao Xing
- Zirui Xue
- Rui Li
- Xiangyu Zhao
- Shuofei Qiao
- Minting Pan
- Wangmeng Zuo
- Lei Bai
- Dongzhan Zhou
- Ningyu Zhang
- Huajun Chen
topics:
- vision-language-action
- robot-foundation-model
- scientific-lab-automation
- simulation-data-generation
- cross-embodiment
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# LabVLA: Grounding Vision-Language-Action Models in Scientific Laboratories

## Summary
LabVLA targets robot execution of written laboratory protocols, where current vision-language-action policies fail on lab instruments, liquids, and multi-step bench workflows. It pairs a synthetic lab data engine with a two-stage policy so a pretrained VLM can map lab instructions to robot actions across embodiments.

## Problem
- Existing VLA policies are mostly trained on household and tabletop data, so they do not learn lab-specific objects, contact precision, or protocol workflows.
- Real laboratory data is costly to collect because it needs specialized instruments, safety checks, and domain supervision.
- The same lab protocol must run on different robot embodiments with different cameras, grippers, workspaces, and action spaces.

## Approach
- RoboGenesis builds lab scenes in simulation from generated 3D assets, validated layouts, and configurable robot profiles.
- It composes long-horizon workflows from atomic skills such as pick, pour, press, stir, open, and close.
- It applies domain randomization after workflow validation so the same protocol can vary in lighting, clutter, camera pose, object appearance, and placement without changing task semantics.
- It exports only successful rollouts as LabEmbodied-Data with multicamera observations, robot state, actions, and step-level annotations.
- LabVLA trains a Qwen3-VL-4B-Instruct backbone first with FAST action tokens, then with flow matching and a DiT action expert under stop-gradient knowledge insulation.

## Results
- RoboGenesis generates a LabAssetLibrary with 2,947 annotated assets and 1,000+ textures, then uses them to build 10,000 laboratory scenes.
- The supported robot pool covers 16 robot platforms, including single-arm, bimanual, and mobile-manipulator setups.
- The paper reports that composite workflows with more than 20 skill steps still achieve collection success rates above 75%.
- On LabUtopia, LabVLA claims the highest average success rate among all evaluated baselines in both in-distribution and out-of-distribution settings.
- The excerpt does not give the exact LabUtopia success numbers or baseline values, so the strongest stated result is the rank-order claim plus the reported data scale.

## Link
- [https://arxiv.org/abs/2606.13578v1](https://arxiv.org/abs/2606.13578v1)
