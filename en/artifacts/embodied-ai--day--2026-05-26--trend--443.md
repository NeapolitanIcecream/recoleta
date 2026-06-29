---
kind: trend
trend_doc_id: 443
granularity: day
period_start: '2026-05-26T00:00:00'
period_end: '2026-05-27T00:00:00'
topics:
- robot learning
- vision-language-action
- continual learning
- sim-to-real
- visual reinforcement learning
- humanoid robots
run_id: materialize-outputs
aliases:
- recoleta-trend-443
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action
- topic/continual-learning
- topic/sim-to-real
- topic/visual-reinforcement-learning
- topic/humanoid-robots
language_code: en
pass_output_id: 232
pass_kind: trend_synthesis
---

# Robot learning papers concentrate on execution control, retention, and cheaper real-world validation

## Overview
The period’s strongest signal is practical robot learning under real deployment constraints. Vision-language-action (VLA) models are being tested for fine execution control and skill retention, while HyperSim and SDPG reduce the real-data or GPU cost of training. Figure’s package-sorting run adds an endurance claim, but with weaker audit detail than the research papers.

## Clusters

### Steerable VLA policies
FineVLA targets a specific weakness in robot datasets: many trajectories say what task was completed, but leave out how it was done. The work adds human-verified execution instructions for arm choice, approach direction, contact region, final pose, and other action details across 47,159 selected trajectories. Training with a mix of fine-grained and raw labels gives the best reported results, with AlohaMix-OFT reaching 86.8% Easy and 82.5% Hard on RoboTwin. In real dual-arm manipulation, the same line of evidence reports 62.7/100 for a 1:1 fine-grained-to-raw mix, compared with 49.9 for raw-only training.

#### Evidence
- [FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies](../Inbox/2026-05-26--finevla-fine-grained-instruction-alignment-for-steerable-vision-language-action-policies.md): Summary gives the dataset construction, instruction dimensions, RoboTwin results, and real-world dual-arm scores.

### Continual learning for real robot skills
The continual VLA study makes forgetting measurable on hardware-style tasks. Plain sequential fine-tuning drops earlier skills hard: Stack Bowl falls from 100.0 to 15.0, Hang Cup from 97.5 to 25.0, and Press Button from 100.0 to 13.3. Experience replay changes the outcome when replay rate and action normalization are set carefully. With buffer ratio 0.2 and replay frequency 0.2, the final average score reaches 93.5, compared with 37.3 for sequential fine-tuning. The action-normalization result is a useful warning: per-task normalization collapses to a 23.7 average, suggesting deployment details can dominate the learning method.

#### Evidence
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): Summary reports the four-task dataset, forgetting numbers, replay settings, and normalization failure.

### Cheaper training and sim-to-real transfer
HyperSim and SDPG both attack the cost of training visual robot policies. HyperSim uses reconstructed scenes, adversarial synthetic trajectories, and 35 real demonstrations for co-training. In few-shot tests, mixed sim-real data reaches 95% SR3 with pi0, above the 70% real-only baseline with the same number of real demonstrations. SDPG reduces the rendering and memory burden for visual reinforcement learning by estimating action-sequence gradients with random perturbations. Its reported memory use is about 10.2 to 10.5 GB across Visual MuJoCo tasks, while the PPO estimate is about 48 to 50 GB.

#### Evidence
- [HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation](../Inbox/2026-05-26--hypersim-a-holistic-sim-to-real-framework-for-robust-robotic-manipulation.md): Summary gives HyperSim's components, few-shot setup, and success rates against real-only baselines.
- [Efficient On-policy Visual-RL via Stochastic Decoupled Policy Gradient](../Inbox/2026-05-26--efficient-on-policy-visual-rl-via-stochastic-decoupled-policy-gradient.md): Summary gives SDPG's training method, memory comparison, and single-GPU claim.

### Humanoid endurance claims need better measurement
Figure reports a 200-hour autonomous package-sorting run by Figure 03 humanoids, with 249,560 packages sorted. The task is concrete: locate the barcode on a small package and place it face-down on a conveyor. The article also gives a human comparison from an earlier 10-hour run, where the human sorted 12,924 packages and the robot sorted 12,735. The claim is useful as an endurance marker, but the source does not provide an independent audit, error rate, uptime breakdown, or comparison with existing warehouse automation.

#### Evidence
- [Figure's robots sorted packages for 200 hours straight](../Inbox/2026-05-26--figure-s-robots-sorted-packages-for-200-hours-straight.md): Summary gives the 200-hour run, package count, human comparison, and missing audit details.
