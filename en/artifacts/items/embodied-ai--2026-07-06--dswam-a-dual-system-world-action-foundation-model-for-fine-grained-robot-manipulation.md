---
source: arxiv
url: https://arxiv.org/abs/2607.04927v1
published_at: '2026-07-06T10:57:01'
authors:
- Jian Zhu
- Jianjun Zhang
- Taiyi Su
- Tianbin Liu
- Zhangyuan Wang
- Kai Xie
- Zitai Huang
- Chong Ma
- Youzhang He
- Tianjian Wang
- Hanyang Wang
- Weihao Ding
- Yi Xu
topics:
- world-action-model
- vision-language-action
- robot-foundation-policy
- deformable-manipulation
- real-time-robot-control
- subtask-planning
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# DSWAM: A Dual-System World Action Foundation Model for Fine-Grained Robot Manipulation

## Summary
DSWAM pairs a World Action Model executor with an optional vision-language subtask planner for fine-grained robot manipulation. It claims stronger execution than matched VLA baselines in real folding tasks and broad simulated bimanual success.

## Problem
- WAM robot policies can model physical scene change, but they usually lack an explicit language interface for turning coarse household commands into executable subtasks.
- VLA-vs-WAM robot results are hard to compare when papers use different robots, data, tasks, and success rules.
- The issue matters because household manipulation often needs both contact-rich execution and simple task decomposition, especially for deformable objects and multi-step goals.

## Approach
- System 1 is the default WAM executor. It takes multi-view RGB images, language, and proprioception, then predicts continuous dual-arm action chunks.
- System 2 is a vision-language planner based on a Rynnbrain4B-style model. It sees 5 recent frames sampled at 1 Hz plus the global prompt, then emits the next executable subtask or `done`.
- The executor trains with action prediction plus video co-training under a flow-matching loss, so future visual tokens teach physical dynamics during training.
- At inference, the executor predicts actions directly and does not generate future video, which cuts latency and avoids control depending on generated frames.
- Deployment adds real-time chunking, asynchronous execution, and TensorRT BF16 acceleration so policy queries do not stop robot control.

## Results
- On the matched DeMaVLA real-world folding benchmark, DSWAM raises average success from 92.5% to 96.3% and cuts average completion time from 2'18" to 1'44". The System 2 planner is disabled for this comparison.
- The folding benchmark uses an ALOHA-style dual-arm robot, 4 garment categories, 2 instances per category, and 10 trials per instance, with the same platform, data, task protocol, and success criteria as DeMaVLA.
- On RoboTwin 2.0, DSWAM reports 92.38% average success on clean tasks and 91.90% under randomized object poses and scene layouts across 50 bimanual manipulation tasks.
- In the System 2 sorting study, subtask supervision improves real-world execution stability by increasing success rate and reducing rollout mistakes, but the excerpt does not provide exact sorting numbers.
- The paper reports that BF16 TensorRT keeps close agreement with PyTorch while reducing policy-query latency, but the excerpt does not give a latency value.

## Link
- [https://arxiv.org/abs/2607.04927v1](https://arxiv.org/abs/2607.04927v1)
