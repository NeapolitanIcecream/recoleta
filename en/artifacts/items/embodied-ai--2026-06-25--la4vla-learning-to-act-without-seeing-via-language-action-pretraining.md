---
source: arxiv
url: https://arxiv.org/abs/2606.27295v1
published_at: '2026-06-25T17:13:02'
authors:
- Tao Lin
- Yuxin Du
- Yiran Mao
- Zewei Ye
- Yilei Zhong
- Bing Cheng
- Yiming Wang
- Jiting Liu
- Yang Tian
- Junchi Yan
- Feiran Wu
- Zenan Meng
- Hu Wei
- Yuqian Fu
- Gen Li
- Bo Zhao
topics:
- vision-language-action
- robot-pretraining
- language-action
- robot-data-scaling
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# LA4VLA: Learning to Act without Seeing via Language-Action Pretraining

## Summary
LA4VLA trains robot policies on language, proprioception, and actions before standard VLA training, so the policy learns instruction-conditioned motion patterns without image shortcuts. It builds 33,116 human-verified language-action episodes from DROID and reports higher simulated and real-world success rates for a 1B-parameter VLA model.

## Problem
- Standard VLA pretraining gives each long trajectory one high-level instruction but hundreds of image-action pairs, so language-action supervision is sparse compared with vision-action supervision.
- The paper's diagnostic shows a standard VLA policy follows directions with paired images but fails when images are removed, mismatched, or conflicting; this matters because real robot scenes vary in viewpoint, background, lighting, layout, and object appearance.

## Approach
- LA4VLA splits existing expert demonstrations into short atomic action segments such as grasp, lift, lower, transport, press, rotate, and reorient.
- A Qwen-3-VL-Plus segmentation pipeline uses sampled video frames, robot-state keyframe hints, primitive definitions, and the original task instruction to propose segment boundaries and low-level action descriptions.
- Human annotators score candidate segments from 0 to 3 and keep segments with score at least 2.
- The final LA pretraining input removes images and keeps the low-level instruction, proprioceptive states, and action trajectory; the paper tests LA-only, sequential LA-to-VLA, and mixed LA-VLA pretraining.

## Results
- The dataset starts with 9,560 DROID VLA episodes and produces 56,899 VLM-generated candidates; after verification it keeps 33,116 LA episodes with 1,524,990 frames.
- Average frames per episode drop from 287.83 in original VLA episodes to 46.05 in final LA episodes, giving shorter segments tied to local action instructions.
- In the diagnostic over 100 direction-following cases, paired visual input reaches DAR 0.98 and DCS 0.95, while visual-removed input drops to DAR 0.63 and DCS 0.16; conflicting visual input drops to DAR 0.35 and DCS 0.03.
- LA4VLA-1B reports 87.53% average success on MetaWorld, 96.28% on LIBERO, and 83.3% on real-world manipulation tasks.
- Mixed LA-VLA pretraining improves LA4VLA-1B over the no-pretraining baseline by 17.80 percentage points on MetaWorld, 3.43 points on LIBERO, and 45.0 points on real-world tasks.

## Link
- [https://arxiv.org/abs/2606.27295v1](https://arxiv.org/abs/2606.27295v1)
