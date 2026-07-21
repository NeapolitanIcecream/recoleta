---
source: arxiv
url: https://arxiv.org/abs/2607.18231v1
published_at: '2026-07-20T17:58:31'
authors:
- Ruicheng Li
- Qixiu Li
- Ruichun Ma
- Yu Deng
- Lin Luo
- Zhiying Du
- Jianfeng Xiang
- Huizhi Liang
- Ruicheng Wang
- Jiaolong Yang
- Baining Guo
topics:
- robot-foundation-model
- vision-language-action
- force-sensing
- contact-rich-manipulation
- robot-memory
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# FM-VLA: Force-based Memory for Vision-Language-Action Models in Contact-Rich Manipulation

## Summary
FM-VLA adds compact force-history memory to a vision-language-action policy for contact-rich tasks whose progress is difficult to observe visually. On three bimanual manipulation tasks, it reaches 83.3% average success while adding only 3.3 ms of inference latency over the base policy.

## Problem
- Memoryless VLAs cannot reliably count repeated contacts, track hidden interaction progress, or recover episode history when the current image looks unchanged.
- Visual-memory methods require extra image tokens and can miss events such as repeated button presses with negligible visual motion.
- The paper evaluates this problem on three tasks with an AgiBot G1 bimanual robot: finding a block under cups, pressing buttons a specified number of times, and wiping a dish for a specified number of passes.

## Approach
- A force-history VAE compresses noisy 6-axis wrist force/torque sequences into eight latent memory tokens using task-agnostic time-series reconstruction pretraining.
- The latent force tokens condition the flow-matching action expert alongside the current images and language instruction, allowing the policy to retain contact events over an episode.
- A projected one-second window of joint positions and gripper states supplies short-term motion context and reduces repetitive pre-contact behavior.
- Exponential-moving-average smoothing and randomized noise pre-padding reduce sensor noise and prevent the model from using history length as a shortcut.

## Results
- FM-VLA achieves 100.0% success on the cups task, 72.2% on buttons, and 77.8% on wiping, for 83.3% average success across 18 trials per task.
- It outperforms the memoryless pi_0.5 baseline, which averages 27.8% success, TA-VLA at 22.2%, and the visual-memory pi-MEM baseline at 53.7%.
- On button pressing, FM-VLA reaches 72.2% versus 33.3% for pi-MEM; on wiping, it reaches 77.8% versus 50.0% for pi-MEM, indicating an advantage when contact events are visually ambiguous.
- Removing either memory stream reduces average success to 25.9% with force history only and 40.7% with state history only; the combined VAE-based design exceeds GRU and Q-Former variants at 33.3% and 57.4%, respectively.
- Inference latency is 64.0 ms on an RTX 4090, only 3.3 ms above the 60.7 ms base policy and below pi-MEM at 99.8 ms with five visual-memory frames.
- The evidence is limited to three tasks, one bimanual robot, and 18 evaluation trials per task; the authors also note that the fixed eight-token bottleneck may limit much longer histories containing hundreds of contact events.

## Link
- [https://arxiv.org/abs/2607.18231v1](https://arxiv.org/abs/2607.18231v1)
