---
source: arxiv
url: https://arxiv.org/abs/2606.32009v1
published_at: '2026-06-30T17:44:16'
authors:
- Xiaopeng Lin
- Ruoqi Yang
- Shijie Lian
- Zhaolong Shen
- Bin Yu
- Changti Wu
- Haibao Liu
- Yuxiang Zhang
- Hong Li
- Qiyuan Su
- Haochen Liu
- Xuguo He
- Yukun Shi
- Cong Huang
- Zhirui Zhang
- Bojun Cheng
- Kai Chen
topics:
- vision-language-action
- humanoid-manipulation
- human-video-learning
- robot-data-scaling
- dexterous-manipulation
- zero-shot-transfer
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Human-as-Humanoid: Enabling Zero-Shot Humanoid Learning from Ego-Exo Human Videos with Human-Aligned Embodiments

## Summary
Human-as-Humanoid converts synchronized human ego-exo videos into executable 60-DoF humanoid action labels for VLA training. The claimed gain is faster humanoid action-data collection plus real-robot deployment on several dexterous tasks without target-task robot demonstrations.

## Problem
- High-DoF humanoid VLAs need observation-action pairs in the target robot controller space, but direct humanoid teleoperation is slow, labor-heavy, and hard to diversify.
- Human egocentric videos contain useful bimanual manipulation, but they lack robot joint actions and differ from humanoids in scale, joints, hands, viewpoints, and reachable workspace.
- The problem matters because robot data volume and action-label quality limit generalist humanoid manipulation policies.

## Approach
- The authors build on PrimeU, a human-aligned upper-body humanoid with 60 controllable DoF: two 7-DoF arms, two 20-DoF dexterous hands, a 3-DoF neck, and a 3-DoF waist.
- Human demonstrations use synchronized egocentric and exocentric videos. The egocentric view matches deployment observations, while exocentric views support upper-body and hand motion recovery.
- The pipeline tracks the human, recovers upper-body and hand keypoints, smooths them, then retargets them through staged IK into PrimeU joint-space action chunks.
- Training keeps the policy output in executable joint space, while a differentiable FK loss supervises wrist pose and fingertip positions so joint predictions preserve manipulation geometry.
- The action model uses a VLM encoder and a flow-matching DiT to predict future 60-DoF action chunks; the excerpt states each chunk contains 40 future states.

## Results
- The conversion pipeline runs at about 20 FPS, close to the stated 15 Hz capture setting.
- The paper claims a 4.8–7.2x raw demonstration-throughput gain over motion-capture humanoid teleoperation in its data-collection analysis.
- An action tokenizer trained on human-derived robot actions reconstructs unseen robot trajectories with normalized MAE of 0.008 on average and 0.0097 at the 95th percentile.
- PrimeU’s anthropometric alignment is reported as shoulder breadth 40.4 cm vs 41.5 cm human reference, reach 80.3 cm vs 78.6 cm, and hand length 19.3 cm vs 19.3 cm.
- Policies post-trained only on converted human labels are reported to deploy on real humanoid tasks including ring placement, bag packing, cap twisting, and water pouring, with zero target-task robot demonstrations.
- The excerpt does not provide task success rates, ablation numbers, or comparisons against robot-demo-trained policies for those real-robot rollouts.

## Link
- [https://arxiv.org/abs/2606.32009v1](https://arxiv.org/abs/2606.32009v1)
