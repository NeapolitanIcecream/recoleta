---
source: arxiv
url: http://arxiv.org/abs/2604.08410v2
published_at: '2026-04-09T16:10:20'
authors:
- Fan Yang
- Wenrui Chen
- Guorun Yan
- Ruize Liao
- Wanjun Jia
- Dongsheng Luo
- Jiacheng Lin
- Kailun Yang
- Zhiyong Li
- Yaonan Wang
topics:
- vision-language-action
- dexterous-manipulation
- 3d-gaussian-splatting
- zero-shot-robotics
- affordance-grounding
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields

## Summary
BLaDA is a zero-shot, modular pipeline for language-driven dexterous manipulation in 3D scenes. It converts open-vocabulary instructions into structured manipulation constraints, finds functional 3D contact regions in a 3D Gaussian Splatting scene, and turns them into wrist and finger commands.

## Problem
- Functional dexterous grasping needs language understanding, precise 3D localization of the right object part, and finger-level control at the same time.
- Existing end-to-end VLA systems need large training datasets and are hard to interpret, while modular affordance methods often depend on fixed affordance labels, 2D or sparse 3D perception, and weak links between semantics and execution.
- This matters for robots in unstructured environments, where the same object may need different grasps for different intents such as handover, use, press, or open.

## Approach
- The system parses a natural-language instruction into a structured sextuple: available grasp region, finger roles, grasp type, force level, task intent, and tool topology. The paper calls this module Knowledge-guided Language Parsing (KLP).
- KLP uses an LLM plus a hand-designed knowledge base to map open-vocabulary instructions into a small set of executable constraints such as `hold`, `press`, `click`, `open` and topology types such as `rod`, `handle`, `knob`, `surface`.
- A TriLocation module builds a semantic 3D Gaussian Splatting scene from multi-view observations, then finds a main functional point by CLIP similarity and predicts two more points so the three points form a grasp triangle in 3D.
- The 3D Gaussian representation is trained with hierarchical object and part features, using YOLO, SAM, CLIP, and DINO-v2, plus a context-aware cropping step to reduce part-level semantic drift.
- A KGT3D+ execution module maps the three localized points and parsed semantic constraints into a wrist pose, hand orientation, finger joint commands, and force settings for physically interpretable dexterous execution.

## Results
- The abstract claims BLaDA significantly outperforms prior methods on affordance grounding precision and functional manipulation success rate across categories and tasks.
- The introduction claims superior zero-shot functional success rates and pose-consistency metrics on complex benchmarks with multiple categories, tasks, and objects.
- The provided excerpt does not include the quantitative tables or exact numbers, so the claimed gains cannot be verified from this text alone.
- Concrete claimed advantages are: zero-shot open-vocabulary instruction following, object-part hierarchical localization in 3D scenes, and finger-level intent-conditioned control without task-specific policy training for semantic grounding.

## Link
- [http://arxiv.org/abs/2604.08410v2](http://arxiv.org/abs/2604.08410v2)
