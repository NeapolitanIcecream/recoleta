---
source: arxiv
url: http://arxiv.org/abs/2604.21331v1
published_at: '2026-04-23T06:37:22'
authors:
- Zhen Zhang
- Weinan Wang
- Hejia Sun
- Qingpeng Ding
- Xiangyu Chu
- Guoxin Fang
- K. W. Samuel Au
topics:
- dexterous-manipulation
- vision-language-action
- diffusion-policy
- fingertip-vision
- real-world-robotics
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# FingerViP: Learning Real-World Dexterous Manipulation with Fingertip Visual Perception

## Summary
FingerViP adds a small camera to each fingertip of a five-finger robot hand and trains a diffusion policy that uses those views together with a third-person camera. The paper targets dexterous manipulation in tight, occluded scenes where wrist-only or external views miss the contact area.

## Problem
- Standard dexterous manipulation setups often rely on one wrist camera or distant external cameras, and both can lose sight of the object and finger contacts in cluttered or confined spaces.
- This matters for real-world dexterous tasks such as insertion, pressing, retrieval behind occlusions, and long-horizon hand-object interaction, where failure often comes from poor local perception near contact.
- Multi-finger hands need both scene-level context and close-range contact-relevant observations; prior camera placements give only part of that information.

## Approach
- The system mounts an embedded miniature RGB camera in each fingertip of a 20-DoF robotic hand, giving five hand-centric views plus one third-view camera.
- A whole-body visuomotor policy takes six images, 26 joint angles, fingertip camera poses from forward kinematics, and per-finger joint currents, then predicts 26-DoF arm-hand actions.
- The policy is a transformer-based diffusion model trained from human teleoperation demonstrations. In simple terms, it learns to map recent observations to the next sequence of robot joint commands by denoising candidate actions.
- Image features come from a frozen CLIP ViT-B/16 encoder. Fingertip visual tokens are augmented with camera pose encodings to align moving viewpoints with robot state, and with finger current encodings to give contact cues such as loading or slip.
- The policy fuses fingertip views for local contact information and the third-view camera for global scene context.

## Results
- Across four challenging real-world tasks, FingerViP reports an overall success rate of **80.8%**.
- On **confined-box button pressing**, trained with **255** demonstrations of average length **7.2 s**, FingerViP achieves **73.8%** overall success over **42** evaluation rollouts and outperforms wrist-camera, third-view, fingertip-only, and mixed-camera baselines according to the paper.
- The hardware and data pipeline include **5** fingertip cameras, **1** third-view camera, a **20-DoF** hand, and **26-DoF** whole-body control with action prediction horizon **n=16** and execution length **m=8**.
- Fingertip cameras run at **30 Hz** with **640×480** resolution; teleoperation tracking runs at **60 Hz** and robot control at **100 Hz**; the reported average latency across five fingertip cameras is **6.7 ms**.
- The abstract names four real-world evaluation tasks: pressing buttons inside a confined box, retrieving sticks from an unstable support, retrieving objects behind an occluding curtain, and long-horizon cabinet opening with object retrieval.
- The provided excerpt does not include the full task-by-task quantitative table beyond the **73.8%** button-pressing result and the **80.8%** overall success figure, so stronger per-baseline numeric comparisons are not available here.

## Link
- [http://arxiv.org/abs/2604.21331v1](http://arxiv.org/abs/2604.21331v1)
