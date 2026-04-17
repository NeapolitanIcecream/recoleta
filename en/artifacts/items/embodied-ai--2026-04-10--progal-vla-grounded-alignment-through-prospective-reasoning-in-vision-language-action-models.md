---
source: arxiv
url: http://arxiv.org/abs/2604.09824v1
published_at: '2026-04-10T18:56:48'
authors:
- Nastaran Darabi
- Amit Ranjan Trivedi
topics:
- vision-language-action
- robot-grounding
- ambiguity-detection
- generalist-robot-policy
- 3d-scene-representation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# ProGAL-VLA: Grounded Alignment through Prospective Reasoning in Vision-Language-Action Models

## Summary
ProGAL-VLA is a vision-language-action model that forces the robot to verify which 3D scene entity an instruction refers to before acting. The paper targets a common VLA failure mode where the policy ignores language and follows visual shortcuts.

## Problem
- Existing VLA systems often show **language ignorance**: changing the instruction does not change behavior enough, because the policy leans on visual priors instead of instruction meaning.
- This matters for robot manipulation because a robot can pick the wrong object, fail on spatial or relational commands, or become unstable when the scene or camera changes.
- Standard multimodal fusion does not check whether the intended symbolic goal actually matches a real, actionable entity in the current 3D scene.

## Approach
- ProGAL-VLA splits the system into a **slow planner** and a **fast controller**. The planner maps the instruction and observation to a short symbolic sub-goal such as `grasp_red_block`.
- A **Grounded State Module (GSM)** builds an entity-centric 3D scene representation with tracked objects and short-term memory, so the model reasons over objects rather than raw image patches.
- A **State Alignment Cross Attention (SACA)** module matches the symbolic sub-goal to the 3D entities and outputs a **verified goal embedding** `g_t`. The action policy receives this verified embedding, not raw language.
- Training adds a **Grounding Alignment Contrastive (GAC)** loss, an InfoNCE-style objective that pulls the symbolic goal toward the correct entity embedding and pushes it away from wrong entities.
- The attention entropy over entities is used as an ambiguity score. High entropy means the instruction does not identify one object clearly, so the model can abstain and ask for clarification.

## Results
- On **LIBERO-Plus** robustness, ProGAL-VLA reports **85.5 total** versus **79.6** for **OpenVLA-OFT+** and **17.3** for base **OpenVLA**.
- Under **robot perturbations** on LIBERO-Plus, performance rises from **30.3** to **71.5**. Other reported category scores include **camera 93.2** vs **92.8**, **language 93.6** vs **85.8**, and **layout 86.7** vs **77.6** compared with OpenVLA-OFT+.
- The paper claims **3x-4x lower language ignorance** across simple, spatial, and relational instructions.
- Grounded entity retrieval improves from **0.41 to 0.71 Recall@1** with **N=8** candidates.
- On the **Custom Ambiguity Benchmark**, ambiguity detection reaches **AUROC 0.81** versus **0.52** and **AUPR 0.79**.
- On ambiguous inputs, clarification behavior rises from **0.09 to 0.81** without reducing success on unambiguous instructions, according to the paper.

## Link
- [http://arxiv.org/abs/2604.09824v1](http://arxiv.org/abs/2604.09824v1)
