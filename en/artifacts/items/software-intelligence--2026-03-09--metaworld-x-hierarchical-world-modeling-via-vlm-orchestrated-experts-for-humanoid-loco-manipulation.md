---
source: arxiv
url: http://arxiv.org/abs/2603.08572v1
published_at: '2026-03-09T16:28:26'
authors:
- Yutong Shen
- Hangxu Liu
- Penghui Liu
- Jiashuo Luo
- Yongkang Zhang
- Rex Morvley
- Chen Jiang
- Jianwei Zhang
- Lei Zhang
topics:
- humanoid-robotics
- world-models
- mixture-of-experts
- vision-language-models
- imitation-learning
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation

## Summary
MetaWorld-X proposes a hierarchical framework for integrated loco-manipulation control in humanoid robots. It decomposes complex control into multiple specialized experts, then uses a VLM-supervised router to combine these experts according to task semantics. Its goal is to simultaneously improve motion naturalness, stability, training efficiency, and cross-task compositional generalization.

## Problem
- This work addresses the problem that **for high-degree-of-freedom humanoid robots performing locomotion and manipulation simultaneously, a single policy struggles to stably learn multi-skill compositions**; monolithic policies are prone to cross-skill gradient interference, motion conflicts, jitter, falling, and unnatural poses.
- This matters because loco-manipulation is a core capability for humanoid robots to perform real-world multi-stage tasks; if control is unstable or motions are unnatural, it becomes difficult to reliably complete complex tasks.
- Although existing world model/RL methods offer advantages in sample efficiency, long-horizon prediction bias, value overestimation, and optimization focused solely on task return often fail to guarantee biomechanical plausibility and compositional generalization.

## Approach
- The core idea is simple: **do not force one large policy to learn everything**. Instead, first train a set of “specialist doctor”-style expert policies (SEP), each responsible only for basic skills such as standing, walking, running, sitting, carrying, and reaching.
- These experts are trained through **imitation-constrained reinforcement learning with human motion priors**: MoCap motions are retargeted to the robot, and energy rewards based on joint position/velocity alignment are used to encourage the robot to imitate natural human motion, thereby producing more natural and stable motor primitives.
- On top of the experts, the authors design a **VLM-supervised Intelligent Routing Mechanism (IRM)**: the VLM provides guidance on “which experts are more relevant” based on task semantics, then the router outputs weights for each expert and combines multiple expert actions through weighted aggregation.
- Router training has two stages: first, coarse alignment using task-level semantic priors, then temporal behavior refinement using few-shot demonstrations; as training progresses, the VLM guidance weights decay, and the router gradually transitions from being “taught” to “autonomous routing.”
- At inference time, the system no longer queries the VLM frequently and retains only the low-latency routing network, enabling real-time control of humanoid robots for multi-stage tasks.

## Results
- On the Humanoid-bench basic skill evaluation, **Ours (IRM)** significantly outperforms baselines in both peak return and convergence speed: for example, **Walk 1118.7±7.1 vs TD-MPC2 644.2±162.3, convergence steps 0.5M vs 1.8M**; **Run 2056.9±13.6 vs TD-MPC2 66.1±4.7, 1.0M vs 2.0M**; **Carry 963.5±5.1 vs 438.0±72.9, 0.5M vs 1.9M**.
- Other basic skills also improve substantially: **Stand 815.9±0.3 vs TD-MPC2 749.8±63.1, 0.6M vs 1.8M**; **Sit 862.2±2.1 vs 733.9±120.6, 0.6M vs 1.1M**. Compared with DreamerV3, PPO, and SAC, it also generally achieves higher returns and faster convergence.
- In success rate (10 trials), after 500k steps the authors’ method reaches: **Stand 9/10, Walk 9/10, Run 9/10, Sit 8/10, Carry 9/10**; whereas TD-MPC2 achieves only **3/10, 3/10, 2/10, 4/10, 3/10**, and DreamerV3 achieves **2/10, 2/10, 1/10, 3/10, 2/10**.
- It also outperforms baselines on complex manipulation tasks: **Door 470.0±2.2 vs TD-MPC2 285.0±12.0**, **Basketball 250.0±11.9 vs 148.4±3.3**, **Push 70.0±2.1 vs -113.8±6.8**, **Truck 1500.0±15.6 vs 1213.2±1.1**, **Package -5200.0±47.2 vs -6788.5±552.7**.
- Ablation experiments show the modules are complementary: on the Door task, the **Full Model** achieves **12.64w steps, return 303.95**, outperforming **TD-MPC2 at 32.38w, 198.42**; **w/o Router** can still succeed but performs worse (**20.36w, 296.57**); **w/o VLM** cannot train successfully; **w/o IL** fails and the step count tends toward infinity, indicating that both VLM semantic routing and imitation learning priors are critical.
- The paper also claims **few-shot and zero-shot compositional generalization** capability, but in the provided excerpt, aside from the routing schedule and task performance, this part does not include more detailed standalone quantitative metrics.

## Link
- [http://arxiv.org/abs/2603.08572v1](http://arxiv.org/abs/2603.08572v1)
