---
source: arxiv
url: http://arxiv.org/abs/2603.04639v1
published_at: '2026-03-04T21:59:32'
authors:
- Yinpei Dai
- Hongze Fu
- Jayjun Lee
- Yuejiang Liu
- Haoran Zhang
- Jianing Yang
- Chelsea Finn
- Nima Fazeli
- Joyce Chai
topics:
- robot-benchmark
- vision-language-action
- memory-augmented-policy
- generalist-robot-policy
- long-horizon-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies

## Summary
RoboMME introduces a large-scale benchmark specifically for evaluating the “memory ability” of robotic generalist policies, and systematically compares multiple memory designs on a unified \(\pi_{0.5}\) backbone. The paper’s core conclusion is that there is no one-size-fits-all solution for robot memory: different tasks require different memory representations and injection methods.

## Problem
- Most existing robotic manipulation evaluations do not **explicitly require memory**; success is often possible using only the current observation, so they cannot truly measure long-horizon, history-dependent capabilities.
- The small number of existing memory-related benchmarks and methods use **narrow task coverage, non-unified protocols, and different backbones**, making fair comparison across memory methods difficult and making it hard to determine which conclusions generalize.
- This matters because real robot tasks often depend on past information, such as **counting, tracking under occlusion, referential disambiguation, and imitating prior demonstrations**; without reliable memory, generalist robot policies struggle to handle long-horizon and non-Markovian scenarios.

## Approach
- The authors build **RoboMME**: a standardized simulation benchmark for memory-augmented manipulation, organized into four task suites corresponding to four cognitive memory types: **temporal, spatial, object, procedural memory**.
- The benchmark includes **16 tasks, 1,600 demonstrations, and 770k training timesteps**. The tasks are intentionally designed to be **non-Markovian, partially observable, and dynamically changing**, and they cover video conditioning, language instructions, subgoals, and keyframe annotations.
- On a unified **\(\pi_{0.5}\)** VLA backbone, the authors implement **14 memory-augmented variants**, comparing three classes of memory representation: **symbolic** (language subgoals), **perceptual** (historical visual tokens), and **recurrent** (compressed hidden states summarizing history).
- They also compare three memory injection mechanisms: **memory-as-context** (directly concatenating memory tokens to the input), **memory-as-modulator** (using memory to modulate intermediate layers of the action network), and **memory-as-expert** (adding a separate memory expert branch).
- Put simply, this paper first creates a benchmark specifically designed to test whether a robot “remembers what happened in the past,” and then attaches different “memory plugins” to the same robot model for a fair comparison.

## Results
- In terms of benchmark scale and coverage, RoboMME includes **16 tasks / 1,600 demonstrations / 770k timesteps**, with an average of about **481 steps** per trajectory. By comparison, MemoryBench has only **3 tasks / 300 demos**, and MIKASA-robo(VLA) has **12 tasks / 1,250 demos / average 72 steps**, showing that RoboMME is more oriented toward long-horizon and systematic memory evaluation.
- In task length, several tasks are clearly long-horizon, such as **VideoPlaceOrder with an average of 1134 steps**, **VideoPlaceButton 974 steps**, **VideoRepick 687 steps**, and **BinFill 604 steps**, reinforcing dependence on history rather than instantaneous perception.
- In evaluation setup, the authors compare **14 in-house VLA variants + 4 existing methods** under unified conditions, using a **512-token memory budget**, evaluating on **50 episodes per task, 800 episodes total**, and averaging over **3 random seeds and the last 3 checkpoints**, improving the controllability of the comparison.
- The paper’s strongest empirical conclusion is that **no single memory representation or integration strategy is consistently best across all tasks**; memory effectiveness is **highly task-dependent**, directly challenging generalization claims drawn by prior work from a small number of custom tasks.
- Qualitatively, the authors claim that **symbolic memory** is better at **counting and short-horizon reasoning**, while **perceptual memory** is more important for **time-sensitive and action/trajectory-related behaviors**.
- Across all variants, the authors claim that **perceptual memory + memory-as-modulator** provides the best **balance between performance and computational efficiency**; however, since the excerpt does not provide the specific average success-rate numbers from the full main results table, those exact gains relative to \(\pi_{0.5}\) or other baselines cannot be listed accurately here.

## Link
- [http://arxiv.org/abs/2603.04639v1](http://arxiv.org/abs/2603.04639v1)
