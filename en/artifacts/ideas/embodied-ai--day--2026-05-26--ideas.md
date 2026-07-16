---
kind: ideas
granularity: day
period_start: '2026-05-26T00:00:00'
period_end: '2026-05-27T00:00:00'
run_id: 1c06e363-c98d-489c-b975-2263ff49b7ab
status: succeeded
topics:
- robot learning
- vision-language-action
- continual learning
- sim-to-real
- visual reinforcement learning
- humanoid robots
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action
- topic/continual-learning
- topic/sim-to-real
- topic/visual-reinforcement-learning
- topic/humanoid-robots
language_code: en
pass_output_id: 233
pass_kind: trend_ideas
upstream_pass_output_id: 232
upstream_pass_kind: trend_synthesis
---

# VLA Policy Update Controls

## Summary
Robot teams can act on three concrete workflow changes: add execution-level labels to VLA demonstration data, gate continual fine-tuning with replay and action-scaling checks, and test sim-real co-training before collecting large new manipulation datasets. Figure’s 200-hour package-sorting report is useful as a durability claim, but it needs error logs, uptime data, and a baseline comparison before it supports a deployment workflow.

## Execution-level annotation for VLA demonstration datasets
VLA data teams should add a short execution annotation pass to manipulation demonstrations where the goal label hides important choices. The useful fields are operational: active arm, target object, approach direction, contact region, motion path, orientation, final configuration, and recovery behavior. FineVLA shows a practical version of the workflow: convert heterogeneous robot datasets into a shared format, cluster redundant demonstrations with dynamic time warping, then annotate a representative subset rather than every trajectory.

The payoff is better control over how a robot completes the same task. FineVLA reports that mixed fine-grained and raw goal labels performed best, with AlohaMix-OFT reaching 86.8% Easy and 82.5% Hard on RoboTwin. In real dual-arm manipulation, a 1:1 fine-grained-to-raw mix scored 62.7/100, compared with 49.9 for raw-only training. A cheap internal test is to pick one high-volume task with multiple valid executions, label a clustered subset, and measure compliance on the fields that operators can see, such as pose, approach direction, and contact point.

### Sources
- [FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies](../Inbox/2026-05-26--finevla-fine-grained-instruction-alignment-for-steerable-vision-language-action-policies.md): FineVLA describes the annotation workflow, selected 47,159 representative trajectories, and reports simulation and real dual-arm gains from mixed fine-grained and raw labels.
- [FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies](../Inbox/2026-05-26--finevla-fine-grained-instruction-alignment-for-steerable-vision-language-action-policies.md): The paper excerpt gives the key mixed-label results and the largest real-world gains on pose, color, and approach direction.

## Continual VLA fine-tuning gate with replay and action-normalization checks
Robot learning teams that update a deployed VLA policy with new task data need a retention gate before each release. The gate should rerun earlier hardware-style tasks, sample old demonstrations through experience replay, and verify that action normalization has stayed consistent across tasks. The failure mode is large enough to treat as a release blocker: in the continual VLA study, plain sequential fine-tuning dropped Stack Bowl from 100.0 to 15.0, Hang Cup from 97.5 to 25.0, and Press Button from 100.0 to 13.3.

The same study gives a concrete starting configuration. Experience replay with buffer ratio 0.2 and replay frequency 0.2 reached a final average score of 93.5 across Stack Bowl, Hang Cup, Press Button, and Fold Towel, while sequential fine-tuning ended at 37.3. The action-scaling check matters as much as the replay setting: per-task normalization collapsed to a 23.7 average, while fixed normalization reached 93.5. A small adoption step is to add a four-task regression suite and fail a model update when any old task falls below a set score or when normalization statistics change without an explicit ablation.

### Sources
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): The summary reports the forgetting results, replay settings, final scores, and the action-normalization collapse.
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): The paper abstract and introduction frame continual real-world VLA learning as a deployment requirement for retaining old skills while adding new ones.

## Few-shot sim-real co-training for manipulation tasks with bottleneck perturbations
Manipulation teams blocked by real demonstration cost can run a smaller validation loop before scheduling a large data collection campaign. HyperSim’s pattern is concrete: reconstruct the scene background, generate synthetic manipulation trajectories around task bottleneck poses, perturb target pose and orientation to produce recovery motions, then co-train on simulation data plus a small set of real demonstrations.

The reported numbers support a practical pilot size. On a deep-bin sorting task with more than 400 real-world executions, HyperSim mixed synthetic data with 35 real demonstrations. With pi0, the mixed setting reached 95% SR3, compared with 70% for the real-only baseline using the same number of real demonstrations. The first internal check should be narrow: choose one bin-picking or sorting cell, record 35 real demonstrations, generate perturbation-heavy synthetic recovery data, and compare mixed training against a real-only run on fixed evaluation trials.

### Sources
- [HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation](../Inbox/2026-05-26--hypersim-a-holistic-sim-to-real-framework-for-robust-robotic-manipulation.md): HyperSim describes high-fidelity scene rendering, adversarial synthetic trajectories, 35 real demonstrations, and the mixed sim-real results against real-only baselines.
- [HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation](../Inbox/2026-05-26--hypersim-a-holistic-sim-to-real-framework-for-robust-robotic-manipulation.md): The paper excerpt states the pipeline components and reports 400 real-world task executions with 80% and 95% sim-to-real success rates for the tested models.
