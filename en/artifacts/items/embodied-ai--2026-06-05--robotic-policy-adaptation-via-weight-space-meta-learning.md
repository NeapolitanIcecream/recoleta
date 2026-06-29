---
source: arxiv
url: https://arxiv.org/abs/2606.07217v1
published_at: '2026-06-05T12:29:28'
authors:
- Christian Bianchi
- Siamak Yousefi
- Alessio Sampieri
- Andrea Roberti
- Luca Rigazio
- Fabio Galasso
- Luca Franco
topics:
- vision-language-action
- robot-policy-adaptation
- weight-space-meta-learning
- lora-adaptation
- zero-shot-robot-learning
- libero-benchmark
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Robotic Policy Adaptation via Weight-Space Meta-Learning

## Summary
WIZARD adapts a frozen vision-language-action robot policy by predicting task-specific LoRA weights from a language instruction and a short demonstration video. It removes target-task action labels and test-time fine-tuning, then reports large gains on held-out LIBERO tasks.

## Problem
- Large VLA robot policies still fail on unseen manipulation tasks and usually need action-labeled demonstrations plus fine-tuning for each new task.
- This matters because per-task fine-tuning adds data collection, compute, and adapter storage costs before a robot can handle a new task.
- The paper cites a large adaptation gap: pretrained $\pi_{0.5}$ gets 0% success on LIBERO-Spatial, fine-tuning on related LIBERO datasets reaches 19%, and direct target-task fine-tuning reaches 94%.

## Approach
- WIZARD first trains LoRA expert adapters for tasks in the meta-training set while keeping the VLA backbone frozen.
- It encodes each task using the frozen VLA encoder on the task language prompt and visual demonstration, then averages episode embeddings into one task embedding.
- A meta-network learns the mapping from task embedding to expert LoRA weights, using weight reconstruction, per-layer scale prediction, and cosine alignment losses.
- The LoRA tensor is structured by VLA components, with separate vision, language, and action parts, so the generator respects the policy architecture.
- At inference, a new prompt and short video produce a LoRA adapter in one forward pass; the robot policy then runs with the generated adapter and no gradient update.

## Results
- On held-out LIBERO-Spatial, WIZARD reaches 0.40 average success, compared with 0.19 for MT-VLA with $\pi_{0.5}$, 0.09 for MT-VLA with OpenVLA-OFT, 0.02 for nearest-neighbor adapter retrieval, and 0.97 for task-specific experts.
- On individual LIBERO-Spatial tasks, WIZARD reports 0.90 on Task 1, 0.82 on Task 3, and 0.84 on Task 4; on Task 6 it reaches 0.28 versus 0.02 for the strongest listed MT-VLA baseline, a 14x gain.
- On held-out LIBERO-Goal, WIZARD reaches 0.22 average success, compared with 0.14 for MT-VLA with $\pi_{0.5}$, 0.05 for OpenVLA-OFT, 0.02 for nearest-neighbor retrieval, and 0.93 for experts; Tasks 5 and 9 both reach 0.86.
- On held-out LIBERO-Object, performance is low but above the baselines: WIZARD averages 0.03 success versus 0.01 for MT-VLA with $\pi_{0.5}$ and 0.00 for nearest-neighbor and OpenVLA-OFT; experts average 0.97.
- On LIBERO-10 subtask metrics, WIZARD reports 0.09/0.07 average success for A/B subtasks, compared with 0.03/0.03 for MT-VLA with $\pi_{0.5}$ and 0.01/0.01 for OpenVLA-OFT; the text says full-task zero-shot completion remains 0.00.
- The abstract claims up to about 2x improvement on unseen dataset collections and up to about 14x on unseen tasks. A real Franka Emika Panda test is described with a 7-DoF arm, three RealSense cameras, 15 Hz VLA outputs, and 1 kHz low-level control, but the excerpt gives no real-world success-rate numbers.

## Link
- [https://arxiv.org/abs/2606.07217v1](https://arxiv.org/abs/2606.07217v1)
