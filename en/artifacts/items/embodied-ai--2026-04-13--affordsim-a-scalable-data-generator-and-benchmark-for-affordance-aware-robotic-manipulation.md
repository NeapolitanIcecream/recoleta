---
source: arxiv
url: http://arxiv.org/abs/2604.11674v1
published_at: '2026-04-13T16:21:44'
authors:
- Mingyang Li
- Haofan Xu
- Haowen Sun
- Xinzhe Chen
- Sihua Ren
- Liqi Huang
- Xinyang Sui
- Chenyang Miao
- Qiongjie Cui
- Zeyang Liu
- Xingyu Chen
- Xuguang Lan
topics:
- robot-simulation
- affordance-learning
- vision-language-robotics
- sim2real
- imitation-learning
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation

## Summary
AffordSim is a simulation system and benchmark for robotic manipulation that uses 3D affordance predictions to generate task-correct trajectories at scale. The paper shows that current imitation-learning policies do well on simple grasping but still struggle on tasks where the robot must act on specific functional object regions.

## Problem
- Existing simulation data generators for robot manipulation do not use object affordances when choosing grasps and motions, so they often produce physically valid but task-wrong trajectories.
- This matters for tasks such as pouring from a cup rim, grasping a mug by the handle, or hanging a mug on a hook, where success depends on contacting the right part of the object.
- Manual grasp design does not scale, and generic grasp methods such as AnyGrasp ignore task semantics.

## Approach
- AffordSim takes a natural-language task, uses a VLM to build a scene in NVIDIA Isaac Sim, captures object point clouds, predicts 3D affordance maps with VoxAfford, then plans grasps and motions from those maps.
- VoxAfford is an open-vocabulary 3D affordance detector: given a query such as "graspable handle" or "pourable rim," it scores points on the object for how suitable they are for that interaction.
- The grasp selector samples candidate grasps around high-affordance regions and scores each one by two factors: how much it contacts high-affordance points and whether the robot can reach it without collision.
- The system supports four robot arms: Franka FR3, Franka Panda, UR5e, and Kinova.
- For sim-to-real transfer, AffordSim adds five kinds of domain randomization, including DA3-based 3D Gaussian background reconstructions from 10-20 real photos.

## Results
- Benchmark: 50 tasks across 7 categories, with 4 imitation-learning baselines trained on 300 demonstrations per task. On 17 representative tasks, average success rates were BC 16%, ACT 35%, Diffusion Policy 44%, and Pi 0.5 61%.
- Simple grasping is much easier than affordance-heavy tasks: grasping reached 53-93% success, while pouring into a narrow cup reached 1-43%, mug hanging reached 0-47%, and long-horizon tasks reached 0-21% depending on the method.
- Example task results: `pick_banana` scored 53/63/87/93% for BC/ACT/DP/Pi 0.5; `pour_cup_into_bowl` scored 1/24/36/43%; `hang_mug_on_rack` scored 0/10/17/47%.
- Affordance ablation on trajectory generation: Manual grasp design averaged 87%, AnyGrasp 20%, VoxAfford 61%, and human affordance labels 92%. On `pour_into_cup`, AnyGrasp got 0% while VoxAfford got 63%; on `pour_into_pan`, AnyGrasp got 20% while VoxAfford got 80%.
- Cross-embodiment trajectory generation success was 94% for Franka FR3, 92% for Panda, 83% for UR5e, and 95% for Kinova.
- Zero-shot sim-to-real on a real Franka FR3 with Pi 0.5 reached 60% on grasping, 30% on placing, 20% on stacking, 40% on push/pull, 20% on pouring, and 10% on mug hanging, for a 30% average. The paper also reports VoxAfford itself improves open-vocabulary 3D affordance detection by about 8 mIoU over prior methods.

## Link
- [http://arxiv.org/abs/2604.11674v1](http://arxiv.org/abs/2604.11674v1)
