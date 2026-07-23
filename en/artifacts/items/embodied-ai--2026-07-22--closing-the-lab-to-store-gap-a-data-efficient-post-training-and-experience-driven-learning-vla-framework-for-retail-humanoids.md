---
source: arxiv
url: https://arxiv.org/abs/2607.20345v1
published_at: '2026-07-22T16:30:51'
authors:
- "Roger Sala Sis\xF3"
- "Tiago Silv\xE9rio"
- Jakob Sand
- Tran Nguyen Le
topics:
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- real-world-deployment
- experience-driven-learning
- ood-detection
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Closing the Lab-to-Store Gap: A Data-Efficient Post-Training and Experience-Driven Learning VLA Framework for Retail Humanoids

## Summary
DEED is a systems framework for adapting the GR00T N1.6 vision-language-action model to real-world retail humanoid restocking with limited robot data. It combines data-efficient post-training, experience-driven refinement, and latent-space distribution monitoring on a Unitree G1-Edu.

## Problem
- VLA policies often perform well on benchmarks but fail during deployment because of execution errors, distribution shifts, inconsistent demonstrations, and environmental variation.
- Offline imitation policies cannot learn from their own deployment experience, which limits recovery and continual improvement in long-horizon tasks such as supermarket restocking.
- This matters because reliable humanoid operation in human-designed environments depends on practical data, control, and monitoring choices as much as on the foundation-model architecture.

## Approach
- Align camera, recording, and control frequencies; curate demonstrations for balanced state coverage, efficient behavior, consistent actions, recoveries, and limited uncontrolled variation.
- Highlight task-relevant visual regions with adapted IA-VLA masks, use binary hand control, smooth predicted actions with a Butterworth filter, and record continuous multi-subtask episodes.
- Adapt RECAP to the decoupled GR00T architecture by adding an "Advantage=True/False" text prefix and training a vision-language value function to label actions by expected progress; human corrective interventions are force-labeled positive.
- Reinitialize each refinement iteration from the original GR00T checkpoint and collect autonomous rollouts plus human recoveries for further training.
- Fit a Gaussian mixture model in the VLA's latent state space and use nearest-component Mahalanobis distance, joint-level scores, and empirical thresholds to identify distribution shifts.

## Results
- The evaluation uses a Unitree G1-Edu with Dex-3 hands on a physical supermarket chip-restocking task, initialized from the GR00T-N1.6-G1-PnPAppleToPlate checkpoint.
- The initial dataset contains 81 teleoperation demonstrations, approximately 51.5 minutes of operation, and a 20-dimensional action space with three RGB cameras recorded at 30 FPS and control recorded at 25 Hz.
- Two refinement iterations added 116 autonomous rollout episodes: 41 successful and 75 failed, totaling approximately 56.9 minutes of autonomous operation.
- The combined teleoperation and autonomous data contains approximately 108.4 minutes of robot operation, and all training, value estimation, and inference ran on a single NVIDIA RTX 5090 workstation.
- The provided excerpt reports that targeted data design and post-training converted a policy that failed under naive fine-tuning into a competent real-world system, but it does not provide comparative success-rate metrics against baselines or quantify the improvement from each DEED component.
- The study also reports a practical limitation: repeated refinement can degrade performance when self-generated rollouts dominate the training distribution, motivating checkpoint reinitialization and distribution monitoring.

## Link
- [https://arxiv.org/abs/2607.20345v1](https://arxiv.org/abs/2607.20345v1)
