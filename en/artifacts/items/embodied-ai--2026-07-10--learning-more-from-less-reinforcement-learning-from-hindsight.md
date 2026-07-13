---
source: arxiv
url: https://arxiv.org/abs/2607.09042v1
published_at: '2026-07-10T02:17:41'
authors:
- Iris Xu
- Sunshine Jiang
- John Marangola
- Nitish Dashora
- Richard Li
- Thomas Liu
- Zexue He
- Yuheng Zhi
- Alex Pentland
- Pulkit Agrawal
- Zhang-Wei Hong
topics:
- vision-language-action
- robot-reinforcement-learning
- hindsight-relabeling
- sample-efficiency
- robot-data-scaling
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Learning More from Less: Reinforcement Learning from Hindsight

## Summary
Learning from Hindsight (LfH) improves reinforcement-learning post-training for vision-language-action models by turning failed robot rollouts into training data for the behaviors they actually performed. It reports about 5x better sample efficiency on OOD LIBERO-PRO tasks and faster improvement on a physical Franka robot.

## Problem
- Sparse success rewards make most early manipulation rollouts useless: groups where every trajectory fails have zero reward variance and produce no GRPO update.
- Robot rollouts are slow and costly, so discarding most collected trajectories limits VLA post-training.
- The problem matters because better use of existing rollouts can reduce the physical data and training steps needed to improve a robot policy.

## Approach
- For a low-success group, a VLM watches a failed trajectory and generates a language instruction describing the behavior the robot actually achieved, such as "pick up the mug."
- The same VLM scores every trajectory in the group against this shared hindsight instruction, assigning rewards of 0, 0.5, or 1.
- LfH applies GRPO to the hindsight-labeled group with an importance correction for actions sampled under the original instruction, then combines this update with the standard GRPO update.
- Relabeling is used mainly for low-reward groups, while groups with useful reward for the commanded task retain the original training signal.

## Results
- On out-of-distribution LIBERO-PRO tasks, LfH reaches the final performance of standard GRPO in about 5 training steps versus nearly 30, giving roughly a 5x sample-efficiency improvement.
- LfH keeps about 70% to 80% of trajectory groups usable for training, compared with about 20% to 40% for standard GRPO and GRPO with RoboMETER dense rewards.
- In a LIBERO-90 example, LfH retains nearly 80% of groups and raises success from zero to 60%, while standard GRPO remains at zero during the reported training period.
- LfH outperforms the RoboMETER dense progress-reward baseline, showing that relabeling the task can help more than adding denser feedback toward a task the policy rarely approaches.
- Results transfer across the pi0.5, GR00T, and OpenVLA-OFT backbones and to a physical Franka FR3 robot. With 160 real-world rollouts, LfH reaches 56% success versus 22% for GRPO; at 128 rollouts, its success rate is about twice as high.
- Instruction relabeling and reward relabeling alone provide only marginal gains, while random rewards fail to match the full method, supporting the need to couple semantically grounded instructions with rewards.

## Link
- [https://arxiv.org/abs/2607.09042v1](https://arxiv.org/abs/2607.09042v1)
