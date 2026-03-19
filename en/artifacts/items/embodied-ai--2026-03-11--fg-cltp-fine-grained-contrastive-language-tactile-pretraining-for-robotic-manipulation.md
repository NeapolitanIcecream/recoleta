---
source: arxiv
url: http://arxiv.org/abs/2603.10871v1
published_at: '2026-03-11T15:21:54'
authors:
- Wenxuan Ma
- Chaofan Zhang
- Yinghao Cai
- Guocai Yao
- Shaowei Cui
- Shuo Wang
topics:
- tactile-learning
- vision-language-action
- robot-manipulation
- sim2real
- contrastive-pretraining
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# FG-CLTP: Fine-Grained Contrastive Language Tactile Pretraining for Robotic Manipulation

## Summary
FG-CLTP proposes a pretraining framework that aligns 3D tactile point clouds with language augmented by numeric tokens, enabling robots to understand not only “what contact feels like,” but also “how large it is, how deep it is, and in which direction it is oriented.” It is paired with a 100k-scale Contact3D dataset and a downstream 3D-TLA policy for contact-rich manipulation.

## Problem
- Existing tactile-language representations mostly remain at the level of **qualitative descriptions**, such as “hard,” “rough,” or “pressed very deep,” but struggle to express the **quantitative contact states** truly needed for robot control, such as force magnitude, contact depth, position, and principal axis orientation.
- 2D tactile image representations often **depend heavily on sensor appearance and lighting**, resulting in poor cross-sensor generalization and making them unsuitable for a unified robotic foundation model.
- There is a lack of large-scale tactile data that both covers **multidimensional contact physical quantities** and is suitable for language alignment and policy learning, limiting fine-grained manipulation capability and sim2real transfer.

## Approach
- Build the **Contact3D** dataset: containing **100k** tactile-language samples, **136** objects, and **4 sensor types**, with each sample including a 3D deformation point cloud, tactile image, force/torque, and contact-state annotations.
- Use **3D tactile point clouds** as the unified representation, avoiding sensor-specific artifacts in 2D tactile images and emphasizing physical cues such as geometric deformation and shear.
- Propose **discrete numeric tokenization**: bin continuous contact attributes such as depth, area, position, and principal axis angle, then write them into language prompts so the model aligns “numeric physical quantities” with “language semantics.”
- Use **contrastive learning** to jointly align tactile point clouds, language, and tactile images; freeze the original CLIP vocabulary and learn only the newly added numeric tokens to reduce forgetting.
- Add an **auxiliary regression loss** to directly supervise continuous physical quantities such as depth, position, and principal axis; and propose **3D-TLA** downstream, connecting this representation to a flow matching-based VLA policy for action generation.

## Results
- The abstract claims that FG-CLTP achieves **95.9% classification accuracy** in contact-state understanding and reduces **regression MAE by 52.6%** relative to the SOTA.
- In linear-probe classification experiments, the model reaches **90.6%** shape classification accuracy, as well as **97.6%** depth classification accuracy and **97.6%** position classification accuracy.
- The paper claims that the 3D point-cloud representation achieves a **3.5% sim-to-real gap** and stronger cross-sensor generalization; however, the provided excerpt does not include more detailed tables or comparison details.
- In terms of data scale, Contact3D covers **136 objects** and **100k samples**, which is larger and more comprehensive than TCL3D with **117 objects / 50k** and TacQuad with **124 objects / 72k** as listed in the table.
- The regression table excerpt shows that the compared baselines include **TVL, AnyTouch, UniTouch, CLTP**; the full per-metric values for FG-CLTP are truncated in the provided text, but the authors explicitly claim it is best overall.
- For downstream manipulation experiments, the authors claim significant gains over strong baselines on **contact-rich manipulation tasks**, but the currently provided content does not include specific success-rate figures, task names, or statistical significance values.

## Link
- [http://arxiv.org/abs/2603.10871v1](http://arxiv.org/abs/2603.10871v1)
