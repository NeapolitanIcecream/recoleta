---
source: arxiv
url: https://arxiv.org/abs/2606.23686v1
published_at: '2026-06-22T17:59:53'
authors:
- Rongxu Cui
- Zongzheng Zhang
- Jingrui Pang
- Haohan Chi
- Jinbang Guo
- Saining Zhang
- Shaoxuan Xie
- Xin Jin
- Yao Mu
- Jiaolong Yang
- Guocai Yao
- Xianyuan Zhan
- Ya-Qin Zhang
- Hao Zhao
topics:
- vision-language-action
- robot-safety-benchmark
- collision-avoidance
- semantic-safety
- robot-data-generation
- human-robot-interaction
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models

## Summary
LIBERO-Safety is a benchmark and dataset for testing whether VLA robot policies can finish manipulation tasks without unsafe contact or unsafe instruction following. It adds parametric safety scenarios, generated collision-free demonstrations, and a cross-model evaluation that shows current VLAs still fail often under safety constraints.

## Problem
- Current VLA benchmarks test task completion more than safe execution, so a policy can look strong while colliding with clutter, human hands, or held objects.
- This matters because deployment near people requires collision control, safe hand-object interaction, and refusal of harmful commands.
- Human teleoperation limits data scale; the paper reports 7.4 minutes per task for teleoperation, which slows collection of safety data.

## Approach
- The benchmark defines safety tasks with UBDDL, an extension of BDDL that samples scene layouts, object poses, camera settings, visual variation, sensor noise, dynamic entities, and safety predicates.
- It splits safety into 5 suites: affordance-aware grasping, human-robot interaction, tabletop spatial avoidance, free-space hand-object avoidance, and semantic safety reasoning. Each suite has 3 levels, L0-L2.
- A human gives sparse object-centric keyposes. CuRobo turns those keyposes into full robot motions while checking collisions at every timestep.
- The data generator creates multiple spatial variants per keypose and samples combinations, so one human keypose script can produce many demonstrations.

## Results
- The benchmark contains 75 tasks: 5 suites × 3 levels × 5 tasks. The generated scenes include 7,603 unique scenes, 953 objects, and 462 hand-object pairs.
- The dataset has 19,664 human-screened, collision-free demonstrations across 40 physical-safety training tasks. The authors omit all L2 tasks and the semantic reasoning suite from training to keep those tests unseen.
- Data collection effort drops from 7.4 to 1.8 minutes per task versus human teleoperation in Table 2, with planner collision checks replacing human-dependent safety checks.
- The evaluation covers 8 VLA policies for physical safety and 2 embodied foundation models for semantic refusal, using 10 trials per task and 3 random seeds for physical rollouts.
- OpenVLA-OFT reaches 79.3% SR on AAG-L1, 80.0% on HRI-L1, 41.3% on TSA-L1, and 50.7% on FSHOA-L1, but falls to 1.3% on AAG-L2 and 42.7% on FSHOA-L2.
- pi0.5 is the strongest named baseline in the shown table: 84.7% SR on HRI-L0, 88.7% on HRI-L1, 83.3% on HRI-L2, and 51.3% on FSHOA-L2. It still has large gaps on hard physical safety, including 35.3% on AAG-L2.

## Link
- [https://arxiv.org/abs/2606.23686v1](https://arxiv.org/abs/2606.23686v1)
