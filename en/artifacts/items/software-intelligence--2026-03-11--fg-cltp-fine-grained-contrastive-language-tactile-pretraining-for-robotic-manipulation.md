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
- robotic-manipulation
- tactile-learning
- multimodal-pretraining
- contrastive-learning
- vision-language-action
relevance_score: 0.33
run_id: materialize-outputs
language_code: en
---

# FG-CLTP: Fine-Grained Contrastive Language Tactile Pretraining for Robotic Manipulation

## Summary
FG-CLTP proposes a pretraining framework that aligns tactile 3D point clouds with language containing numerical information for finer-grained robotic contact perception and manipulation. It aims to upgrade "coarse semantic touch" into "quantifiable physical touch" and further connect it to action policies.

## Problem
- Existing tactile-language models mostly learn **qualitative descriptions**, such as "rough," "hard," and "strong pressure," but struggle to express the **quantitative contact states** truly needed for manipulation, such as force magnitude, contact depth, position, and principal axis orientation.
- 2D tactile image representations are often **sensor-dependent**, easily mixing in hardware- and lighting-related artifacts, which limits cross-sensor generalization and sim-to-real transfer.
- The lack of a pretraining approach that provides both **large-scale multimodal data** and precise correspondence between language and physical quantities makes it difficult to translate high-level semantics into low-level fine control.

## Approach
- Builds the **Contact3D** dataset, containing **100k** tactile 3D point cloud-language paired samples, covering **136** objects, with annotations for contact states such as force/torque, contact position, area, principal axis, and sliding/twisting.
- Uses **discretized numerical tokenization** to bucket continuous physical quantities into language tokens, such as depth, area, position, and angle, allowing the model to write "digitized physical states" directly into text prompts.
- Adopts multimodal contrastive learning over **3D tactile point clouds + language + tactile images**, aligning them in a shared feature space; the language encoder keeps the original vocabulary frozen and learns only the newly added numerical tokens, reducing forgetting.
- Adds an **auxiliary regression loss** to directly supervise continuous attributes such as depth, position, and principal axis, improving the representation's sensitivity to fine-grained physical quantities.
- Proposes **3D-TLA** downstream, connecting the pretrained tactile encoder to a policy network based on flow matching for contact-rich manipulation.

## Results
- The paper claims that FG-CLTP achieves **95.9%** classification accuracy and reduces regression **MAE by 52.6%** relative to the SOTA.
- On offline classification benchmarks, it reports **90.6%** shape classification accuracy, as well as **97.6%** depth classification accuracy and **97.6%** position classification accuracy.
- The abstract claims that using a 3D point cloud representation enables a **3.5% sim-to-real gap** and provides stronger cross-sensor generalization.
- In terms of dataset scale, Contact3D includes **4 sensor types, 136 objects, and 100k samples**, and compared with multiple existing datasets in the table, it more completely covers depth, force, language, and dynamic attributes.
- The regression table is truncated in the excerpt, so it is not possible to fully verify the specific values for all tasks, the names of the best baselines, or the per-task improvement margins; however, the paper explicitly claims significant advantages over strong baselines in contact-state understanding and real-world manipulation tasks.

## Link
- [http://arxiv.org/abs/2603.10871v1](http://arxiv.org/abs/2603.10871v1)
