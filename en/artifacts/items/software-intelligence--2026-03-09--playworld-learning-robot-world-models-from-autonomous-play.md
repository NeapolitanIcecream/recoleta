---
source: arxiv
url: http://arxiv.org/abs/2603.09030v2
published_at: '2026-03-09T23:58:07'
authors:
- Tenny Yin
- Zhiting Mei
- Zhonghe Zheng
- Miyu Yamane
- David Wang
- Jade Sceats
- Samuel M. Bateman
- Lihan Zha
- Apurva Badithela
- Ola Shorinwa
- Anirudha Majumdar
topics:
- robot-world-models
- autonomous-play
- video-diffusion
- robot-manipulation
- policy-evaluation
relevance_score: 0.24
run_id: materialize-outputs
language_code: en
---

# PlayWorld: Learning Robot World Models from Autonomous Play

## Summary
PlayWorld proposes a framework for training action-conditioned video world models from robot autonomous play data, aiming to more realistically predict contact-rich manipulation processes. The core idea is to avoid relying on success-biased human demonstrations; instead, robots continuously explore and collect diverse interactions under unsupervised conditions, and these data are then used to train a high-fidelity video simulator.

## Problem
- Existing robot video world models are mostly trained on human demonstration data, whose distribution is biased toward successful trajectories, making it difficult for models to cover critical contact events such as failures, collisions, slipping, and deformation.
- Once the policy deviates from the training distribution at test time, video models tend to exhibit physically inconsistent phenomena such as objects appearing/disappearing out of nowhere, duplication, and incorrect motion, which undermines the reliability of policy evaluation, planning, and reinforcement learning.
- This problem matters because robotic manipulation depends precisely on accurate modeling of contact dynamics; if the world model becomes distorted at key contact moments, downstream automatic evaluation and policy improvement will fail.

## Approach
- PlayWorld uses a **VLM task proposer** to automatically generate diverse natural-language instructions from the current scene image, and then a pretrained **VLA executor** carries them out, forming unsupervised, self-evolving robot “play” data.
- It induces more behavior modes through instruction perturbation and naturally varying initial states. Rather than relying on reward design or simple action noise, it expands state-action coverage using “semantically different task intents.”
- To support long-term unattended collection, the system includes lightweight safety filtering and a VLM-based scene reset mechanism, enabling continuous autonomous operation for up to about 8 hours, including overnight data collection.
- The world model uses a pretrained stable video diffusion backbone, jointly predicts 3 camera views, and is fine-tuned from DROID pretrained weights to learn a finer-grained mapping from actions to video dynamics.
- To mitigate redundancy and long-tail distributions in play data, the authors design a curriculum based on CLIP “distance to successful trajectories”: the model first learns common, easy transitions, then gradually incorporates rarer and more difficult interaction samples.

## Results
- On the interaction-centric benchmark, **Robot Play (6h)** outperforms **Human Demo (6h)** on perceptual metrics across multiple contact scenarios. For example: successful scenes LPIPS **0.082 vs 0.084**, SSIM **0.870 vs 0.867**; missed grasp **0.066/0.883 vs 0.080/0.875**; slide **0.077/0.865 vs 0.090/0.850**; slip **0.078/0.871 vs 0.090/0.865**; collision **0.074/0.888 vs 0.086/0.852**.
- Scaling to **Robot Play (30h)** brings further gains. For example, successful-scene LPIPS drops to **0.071**, slide reaches **0.073/0.876**, and slip reaches **0.072/0.879**, indicating that autonomous play data continue to provide benefits at larger scale, whereas human demonstration data saturate earlier.
- With curriculum learning, the model reaches some of its best results: successful scenes **LPIPS 0.070 / SSIM 0.880**, slide **0.071 / 0.890**, slip **0.070 / 0.884**, collision **0.072 / 0.893**, suggesting that the training order for long-tail interactions is also critical.
- The paper claims that, for policy evaluation and failure prediction, PlayWorld achieves up to **40%** improvement over human-collected data.
- The paper further claims that, after reinforcement learning fine-tuning inside the world model, the success rate of policies deployed on real robots improves by **65%** compared with the pretrained policy.
- In terms of data collection, the system can perform **up to 8 hours of continuous fully autonomous collection** on the existing DROID platform, and supports overnight unsupervised collection, demonstrating strong scalability.

## Link
- [http://arxiv.org/abs/2603.09030v2](http://arxiv.org/abs/2603.09030v2)
