---
source: arxiv
url: https://arxiv.org/abs/2605.10819v2
published_at: '2026-05-11T16:37:07'
authors:
- Zuojin Tang
- Haoyun Liu
- Xinyuan Chang
- Changjie Wu
- Dongjie Huo
- Yandan Yang
- Bin Liu
- Zhejia Cai
- Feng Xiong
- Mu Xu
- jiachen Luo
- De Ma
- Zhiheng Ma
- Gang Pan
topics:
- vision-language-action
- latent-action-models
- robot-data-scaling
- flow-matching
- action-free-video
- robot-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models

## Summary
ALAM learns structured latent action transitions from action-free robot videos and uses them as auxiliary targets for VLA policy training. Its main claim is that algebraic consistency in the latent space improves flow-matching robot policies on MetaWorld, LIBERO, and real-world manipulation tasks.

## Problem
- VLA models need large amounts of action-labeled robot data, which is expensive to collect.
- Action-free videos are abundant, but latent codes trained only for reconstruction can predict frames while giving the policy weak targets for action generation.
- The problem matters because better use of unlabeled video could improve robot policy scaling without requiring matching action labels.

## Approach
- ALAM samples frame triplets from action-free videos and encodes each frame pair into a latent transition.
- A decoder reconstructs the target frame from the source frame and the latent transition, grounding the code in observed visual change.
- Two losses shape the latent space: composition consistency makes z(a,c) close to z(a,b) + z(b,c), and reversal consistency makes z(b,a) close to -z(a,b).
- During VLA training, the pretrained encoder is frozen. It extracts latent transition sequences from third-person and wrist-camera clips.
- A flow-matching policy co-generates latent transitions and robot actions in one interleaved sequence; only the action stream is executed at inference time.

## Results
- Representation probes report 25-85x lower additivity and reversibility errors than unstructured latent-action baselines.
- On MetaWorld MT50, π0 + ALAM reaches 85.0% average success, compared with 47.9% for π0, 66.9% for SmolVLA, and 80.6% for Evo-1.
- MetaWorld MT50 tier scores for π0 + ALAM are 89.3% Easy, 83.6% Medium, 85.0% Hard, and 82.0% Very Hard.
- On LIBERO, π0 + ALAM reaches 98.1% average success, compared with 94.1% for π0, 96.9% for π0.5, 96.9% for JALA, and 95.2% for UniVLA.
- LIBERO suite scores for π0 + ALAM are 99.2% Spatial, 99.6% Object, 99.0% Goal, and 94.4% Long.
- Pretraining uses 11 action-free video sources, 128 H20 GPUs, 39 epochs, and about 4 days; downstream fine-tuning uses 8 H20 GPUs with a π0-style flow-matching backbone.

## Link
- [https://arxiv.org/abs/2605.10819v2](https://arxiv.org/abs/2605.10819v2)
