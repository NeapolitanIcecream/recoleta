---
source: arxiv
url: https://arxiv.org/abs/2604.28192v3
published_at: '2026-04-30T17:59:52'
authors:
- Hao Chen
- Jiaming Liu
- Zhonghao Yan
- Nuowei Han
- Renrui Zhang
- Chenyang Gu
- Jialin Gao
- Ziyu Guo
- Siyuan Qian
- Yinxi Wang
- Peng Jia
- Shanghang Zhang
- Pheng-Ann Heng
topics:
- vision-language-action
- robot-rl
- latent-reasoning
- generalist-robot-policy
- robot-data-scaling
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning

## Summary
LaST-R1 is an RL post-training method for VLA robot policies that trains latent reasoning embeddings and action tokens together. It reports 99.9% average success on LIBERO after one demonstration per task and gains up to 22.5% over a supervised baseline in real robot tasks.

## Problem
- Latent-reasoning VLA policies can model physical state changes before acting, but prior versions depend on static imitation learning and costly expert demonstrations.
- Action-only RL post-training improves closed-loop behavior, but it does not train the internal latent reasoning path that conditions the action.
- The problem matters because manipulation policies face compounding errors, changing scenes, and long-horizon tasks where fixed demonstrations do not cover enough states.

## Approach
- LaST-R1 starts from Qwen3-VL-4B with SigLIP2-Large vision encoding, then generates latent reasoning embeddings before decoding robot action tokens.
- The latent targets come from DINOv3 CLS features, selected to match the VLA hidden size, so the policy has compact visual state targets without running DINOv3 at inference.
- Latent-to-Action Policy Optimization, or LAPO, applies RL to both the latent sequence and the action sequence with step-level likelihood ratios and PPO-style clipping.
- The model treats latent embeddings as decision variables, so rewards from task success update the reasoning path as well as the emitted action chunk.
- An adaptive latent CoT mechanism learns when to emit a latent_end token, choosing shorter or longer reasoning horizons from candidate positions during rollout.

## Results
- On LIBERO, LaST-R1 reports 99.9% average success across four suites using one demonstration per task for warm-up; the strongest listed prior RL baseline, pi_RL, reports 98.3% average and uses two camera views.
- LIBERO suite scores are 99.8% Spatial, 100.0% Object, 100.0% Goal, and 99.8% Long.
- On LIBERO-Long, LaST-R1 reports 99.8% success, compared with 94.5% for OpenVLA-OFT and 94.0% for pi_RL, a 5.3 point gain over the best listed prior score.
- Compared with SFT-only baselines trained on 50 trajectories per task, LaST-R1 exceeds OpenVLA at 76.5%, GR00T-N1 at 93.9%, pi_0 at 94.2%, pi_0.5 at 96.9%, and OpenVLA-OFT at 97.1% average LIBERO success.
- In real-world deployments, the paper claims up to a 22.5% average improvement over a supervised fine-tuning method across four complex tasks, with 90% average success in single-arm and dual-arm settings.
- The paper also claims zero-shot generalization after LAPO post-training to unseen objects, backgrounds, and lighting conditions, but the excerpt does not include the full numeric table for those tests.

## Link
- [https://arxiv.org/abs/2604.28192v3](https://arxiv.org/abs/2604.28192v3)
