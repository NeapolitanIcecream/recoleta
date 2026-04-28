---
source: arxiv
url: http://arxiv.org/abs/2604.13733v1
published_at: '2026-04-15T11:17:54'
authors:
- Angelo Moroncelli
- Roberto Zanetti
- Marco Maccarini
- Loris Roveda
topics:
- vision-language-action
- reinforcement-learning
- robot-manipulation
- sim2real
- sample-efficiency
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Jump-Start Reinforcement Learning with Vision-Language-Action Regularization

## Summary
VLAJS uses a pretrained vision-language-action model to speed up reinforcement learning for robot manipulation. It gives sparse action hints early in training, then removes them so the RL policy can keep improving on its own.

## Problem
- On-policy RL for robot manipulation learns slowly on long-horizon tasks and tasks with sparse or poorly shaped rewards because exploration and credit assignment are weak.
- Vision-language-action models contain useful task priors, but they run at low control rates, depend on pretrained data, and are not a good drop-in controller for precise closed-loop manipulation.
- The paper asks how to use VLA knowledge to improve RL sample efficiency without forcing the policy to imitate the teacher forever.

## Approach
- The method, **VLAJS**, augments PPO with sparse guidance from a pretrained VLA teacher such as OpenVLA.
- The teacher is queried only a few times per rollout, at most 20% of rollout steps. Each low-rate teacher action is expanded into short guidance targets over the next few control steps.
- Instead of matching teacher actions with MSE, VLAJS uses a **directional action-consistency loss**: it aligns the RL policy's action direction with the teacher using cosine similarity for translation and rotation, while letting PPO choose action magnitude.
- Guidance is **transient**. The query rate and auxiliary-loss weight decay as rollout reward improves, and guidance is permanently turned off once recent reward improvement is monotonic and exceeds a threshold of 3.
- The learned controller stays a high-frequency state-based PPO policy. Teacher actions are never executed directly in the environment.

## Results
- Evaluated on **6 ManiSkill manipulation tasks**: lifting, pick-and-place, peg reorientation, peg insertion, poking, and pushing, with a subset transferred to a **real Franka Panda** robot.
- The paper claims VLAJS **consistently outperforms PPO and distillation-style baselines** and cuts required environment interactions by **more than 50% on several tasks**.
- For long-horizon experiments, task horizons are increased by **10x**, and sparse teacher querying remains practical, while standard dense RPD is omitted because training time is too high.
- The teacher is **OpenVLA-best** with about **40% average success rate** as a standalone source of guidance.
- Real-world tests claim **zero-shot sim-to-real transfer** and robustness to clutter, object variation, background changes, and external perturbations.
- The excerpt does **not include the numeric values from the main result tables** for SR at t*, AUC, or per-task baseline gaps, so the strongest quantitative claim available here is the **>50% reduction in environment interactions on several tasks**.

## Link
- [http://arxiv.org/abs/2604.13733v1](http://arxiv.org/abs/2604.13733v1)
