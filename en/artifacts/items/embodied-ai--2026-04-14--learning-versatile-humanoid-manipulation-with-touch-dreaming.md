---
source: arxiv
url: http://arxiv.org/abs/2604.13015v2
published_at: '2026-04-14T17:54:17'
authors:
- Yaru Niu
- Zhenlong Fang
- Binghong Chen
- Shuai Zhou
- Revanth Krishna Senthilkumaran
- Hao Zhang
- Bingqing Chen
- Chen Qiu
- H. Eric Tseng
- Jonathan Francis
- Ding Zhao
topics:
- humanoid-manipulation
- tactile-learning
- vision-language-action
- dexterous-manipulation
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Learning Versatile Humanoid Manipulation with Touch Dreaming

## Summary
This paper presents a real-world humanoid manipulation system that combines stable whole-body control, dexterous hands, and tactile sensing. Its main model, Humanoid Transformer with Touch Dreaming (HTD), adds future-touch prediction to behavior cloning and reports large gains on contact-rich tasks.

## Problem
- Real humanoid loco-manipulation is hard because the robot must keep whole-body balance, move dexterous hands, and react to changing contact at the same time.
- Vision and proprioception alone miss parts of contact state, which hurts performance on insertion, deformable objects, tool use, and bimanual transport.
- Prior humanoid systems usually miss at least one of these pieces: whole-body control, full dexterous-hand control, tactile sensing, or tactile modeling.

## Approach
- The system has an RL-trained lower-body controller for stable locomotion and torso tracking, plus VR teleoperation, upper-body IK, and dexterous hand retargeting for data collection and execution.
- The policy model, HTD, is a multimodal encoder-decoder Transformer that takes multi-view RGB, proprioception, hand-joint force signals, and tactile inputs.
- Training uses single-stage behavioral cloning with auxiliary "touch dreaming" losses. Along with predicting action chunks, the model predicts future hand-joint forces and future tactile latents.
- Future tactile targets come from an EMA target encoder, so the model learns a latent prediction target without a separate tactile pretraining stage or an inference-time world model.
- Tactile input is encoded by hand region and finger region, then fused with the other modalities in the shared Transformer trunk.

## Results
- On 5 real-world contact-rich humanoid tasks, HTD reports a **90.9% relative improvement in average success rate** over the stronger **ACT** baseline.
- The task set includes **Insert-T**, **Book Organization**, **Towel Folding**, **Cat Litter Scooping**, and **Tea Serving**.
- The paper states **latent-space tactile prediction** beats **raw tactile prediction** by a **30% relative gain in success rate** in ablations.
- The system handles a tight-tolerance insertion task with **3.5 mm clearance**.
- Deployment runs the learned policy at **30 Hz**, while the lower-body controller, IK solver, and hand retargeter run at **50 Hz**.
- The excerpt does not provide per-task success rates, dataset size, or absolute baseline numbers, so the strongest quantitative claims available are the 90.9% average relative gain and the 30% ablation gain.

## Link
- [http://arxiv.org/abs/2604.13015v2](http://arxiv.org/abs/2604.13015v2)
