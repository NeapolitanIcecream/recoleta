---
source: arxiv
url: https://arxiv.org/abs/2606.27144v1
published_at: '2026-06-25T15:17:43'
authors:
- Jiayu Yang
- Tao Yang
- Xiang Chang
- Fei Chao
- Changjing Shang
- Qiang Shen
topics:
- vision-language-action
- flow-matching
- mixture-of-experts
- robot-manipulation
- phase-routing
- simulated-evaluation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# PAMAE: Phase-Aware-MoE Action Experts Towards Reliable Flow-Matching Vision-Language-Action Policies

## Summary
PAMAE adds phase-aware sparse MoE action experts to flow-matching VLA policies for multi-stage robot manipulation. It reports higher simulated task success than π0, π0.5, ProgressVLA, and ablated variants.

## Problem
- Flow-matching VLA policies often use one shared action expert for all execution stages, which can mix approach, contact, transport, insertion, and release control patterns.
- Multi-stage manipulation needs stage-dependent velocity fields and action sensitivities; errors matter most in long-horizon and contact-rich tasks.
- Prior MoE VLA methods usually route experts by task, embodiment, scale, or modality rather than low-level execution phase.

## Approach
- PAMAE keeps the pretrained VLA backbone and the flow-matching action generation process, then replaces the shared action expert with a sparse mixture of action experts.
- The reported setup uses M=6 experts with top-k=3 routing, increasing a π0-based model from 300M to 450M parameters.
- The router uses the VLA context, flow time, and lightweight execution cues: gripper state, gripper change, previous action norm, and normalized progress t/T.
- Training assigns coarse pseudo phase labels for pre-contact, contact/manipulation, and post-contact using gripper closing and end-effector motion thresholds.
- A two-stage schedule first warms up experts with the flow-matching loss, then adds phase prediction, phase-conditioned routing alignment, routing smoothness, and load balancing; phase labels are not needed at inference.

## Results
- On five simulated multi-stage manipulation tasks with 100 runs per task, PAMAE(π0) improves average success from 73.8% to 83.0%, a +9.2 point gain over π0.
- PAMAE(π0.5) improves average success from 85.8% to 91.4%, a +5.6 point gain over π0.5.
- Per-task PAMAE(π0.5) success rates are 93.0% on Table-Cleaning, 89.0% on Drawer-Cycle, 92.0% on Lid-Open, 86.0% on Shelf-Insert, and 97.0% on Cup-Upright.
- PAMAE(π0) also exceeds ProgressVLA average success, 83.0% versus 78.2%.
- The routing analysis reports an average dominant-expert run length of 8 action chunks and 89.0% phase-conditioned dominance purity for PAMAE(π0).
- Ablations on the π0 backbone report 83.0% average success for full PAMAE, 78.2% without Stage 1 warm-up, 76.2% without routing alignment, and 79.2% without the phase prediction loss, compared with 73.8% for base π0.

## Link
- [https://arxiv.org/abs/2606.27144v1](https://arxiv.org/abs/2606.27144v1)
