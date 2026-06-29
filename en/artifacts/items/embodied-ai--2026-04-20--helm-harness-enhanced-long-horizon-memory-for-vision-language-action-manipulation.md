---
source: arxiv
url: http://arxiv.org/abs/2604.18791v1
published_at: '2026-04-20T19:57:35'
authors:
- Zijian Zeng
- Fei Ding
- Huiming Yang
- Xianwei Li
topics:
- vision-language-action
- long-horizon-manipulation
- episodic-memory
- failure-recovery
- robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation

## Summary
HELM improves long-horizon vision-language-action manipulation by adding explicit memory, action checking before execution, and recovery after failure. The paper argues that larger context windows alone do not fix long-horizon errors in reactive VLA policies.

## Problem
- VLA models do well on short tasks but break on longer manipulation sequences with many subgoals. In the paper's example, OpenVLA gets 91.2% on LIBERO-SPATIAL but drops to 58.4% on LIBERO-LONG.
- The paper says this matters because long-horizon tasks need the robot to remember completed subgoals, reject bad actions before they execute, and recover after mistakes instead of compounding them.
- The authors identify three failure sources in reactive execution: memory gap, verification gap, and recovery gap. In 83 failed LIBERO-LONG episodes, 41% had memory failures, 33% verification failures, 26% recovery failures, and 18% showed multiple modes.

## Approach
- HELM wraps a frozen VLA with three modules: an Episodic Memory Module, a learned State Verifier, and a Harness Controller.
- The Episodic Memory Module stores keyframes and task-state records, indexes them with CLIP embeddings, retrieves the top-3 relevant past states, and appends that retrieved history as structured text to the VLA input.
- The State Verifier is the main learned piece. It is a small 3-layer MLP that takes the current observation, the proposed action, the current subgoal, and retrieved memory context, then predicts the probability that the action will fail before execution.
- The Harness Controller uses that failure score to decide whether to execute, roll back to a prior checkpoint, or replan. It also tracks subgoals and allows up to 3 recovery attempts.
- The core claim is that long-horizon success needs memory-conditioned pre-execution failure prediction, not just a longer token history. The verifier depends on retrieved memory: removing memory from the verifier drops AUROC from 0.847 to 0.791.

## Results
- On LIBERO-LONG, HELM with OpenVLA improves task success rate from 58.4% to 81.5%, a gain of 23.1 percentage points. Increasing OpenVLA context from H=8 to H=32 only reaches 63.8% (+5.4 pp), and even H=64 reaches 65.1%.
- On LIBERO-LONG, HELM also improves subgoal completion rate from 74.2% to 89.3% and recovery success rate from 12.3% to 54.2%.
- Against baselines on LIBERO-LONG TSR: Oracle Memory gets 72.4%, Rule Verifier 65.2%, Ensemble x5 67.9%, LoRA(50K) 69.3%, Reflexion 63.1%, HELM-Fwd 76.3%, and HELM 81.5%.
- On CALVIN ABC->D, average completed chains rise from 3.02 for OpenVLA to 3.58 for HELM. With Octo, HELM improves TSR from 51.2% to 72.8%, a gain of 21.6 pp.
- Ablations on LIBERO-LONG show each part matters: removing EMM drops TSR by 11.2 pp, removing SV drops 8.4 pp, removing rollback drops 6.3 pp, and removing both EMM and SV drops 19.1 pp.
- Mechanism results: CLIP retrieval reaches 81.5% TSR versus 64.3% for random and 71.4% for recency-based retrieval; SV AUROC peaks at 0.847 with a 5-step failure horizon; HELM reduces memory failures by 76%, verification failures by 61%, and recovery failures by 82% per 100 episodes.

## Link
- [http://arxiv.org/abs/2604.18791v1](http://arxiv.org/abs/2604.18791v1)
