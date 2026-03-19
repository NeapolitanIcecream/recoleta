---
source: arxiv
url: http://arxiv.org/abs/2603.05982v1
published_at: '2026-03-06T07:26:45'
authors:
- Ziyang Zhao
- Shuheng Wang
- Zhonghua Miao
- Ya Xiong
topics:
- vision-language-action
- robotic-harvesting
- imitation-learning
- policy-adaptation
- real-world-robotics
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# HarvestFlex: Strawberry Harvesting via Vision-Language-Action Policy Adaptation in the Wild

## Summary
This paper studies transferring open-source vision-language-action (VLA) policies to real greenhouse strawberry harvesting, a long-horizon task with heavy occlusion and fragile objects, and builds an end-to-end closed-loop system using only three-view RGB input. The authors claim that, with less than 4 hours of real demonstration data, fine-tuned VLA policies can already achieve fairly reliable real-world harvesting.

## Problem
- Target problem: enabling a robot to complete strawberry picking and placement in a real greenhouse tabletop environment, which is a **long-horizon, closed-loop, unstructured, and contact-sensitive** manipulation task.
- The difficulty is that **leaf occlusion, specular reflections, illumination changes, and post-contact state changes** cause error accumulation in traditional modular “perception-planning-control” pipelines, reducing cross-farm generalization and robustness.
- This problem matters because strawberry harvesting still relies heavily on manual labor, creating real-world pain points such as **seasonal labor shortages, rising costs, and unstable workforce supply**, while automated systems must also balance success rate, efficiency, and fruit damage rate.

## Approach
- The core method is straightforward: directly feed **three RGB image streams + robot state + language instructions** into a VLA policy, letting the model **directly output robot arm actions and air-pump gripper commands**, eliminating the need for depth point clouds, explicit geometric calibration, and hand-engineered state machines.
- The system is built on the HarvestFlex platform, using **two fixed scene cameras + one wrist-mounted camera** to improve observability during target selection, approach, and contact, while intentionally avoiding dependence on depth and precise calibration.
- For data, the authors collected **3.71 hours, 227 episodes, and 491 valid picking attempts** of real demonstrations via **VR teleoperation** to fine-tune three open-source VLA models: **π0、π0.5、WALL-OSS**, and compared **full fine-tuning** with **LoRA**.
- For deployment, the authors propose **asynchronous inference-control decoupling**: an inference thread generates action chunks in batches, while a real-time control thread executes at a fixed **30 Hz**, reducing control jitter and missed contact windows caused by synchronous inference.

## Results
- Under a unified **50-trial real greenhouse evaluation** protocol, the best result comes from **π0.5 + full fine-tuning + 6 epochs**: **74.0% success rate**, **Success Score 82.6**, **32.6 s/pick**, and **4.1% damage rate**.
- With the same 6-epoch full fine-tuning, the other model results are: **WALL-OSS 68.0% SR / 78.8 SS / 46.3 s / 3.9% DR**; **π0 60.0% SR / 72.6 SS / 38.4 s / 4.2% DR**. This suggests that π0.5 has the highest overall task completion, while WALL-OSS has slightly lower damage.
- LoRA is overall weaker than full fine-tuning: for **π0.5, 6 epochs**, LoRA achieves **64.0% SR / 73.6 SS / 38.3 s / 3.8% DR**, which is **10 percentage points lower in success rate** than full fine-tuning, though with a similar damage rate.
- As training increases from **2→4→6 epochs**, all models generally show **higher success rates and shorter cycle times**. For example, **π0.5 full fine-tuning** improves from **30.0% → 50.0% → 74.0% SR**, while cycle time decreases from **44.2s → 40.7s → 32.6s**.
- Regarding data scale, the authors emphasize that only **3.71 hours of real data** were needed to achieve “non-trivial” closed-loop harvesting capability; they also explicitly note that the main bottlenecks remain **loss of close-range observability** and **contact dynamics mismatch**.
- The abstract also claims that **asynchronous deployment outperforms synchronous deployment**, but the provided excerpt **does not include the corresponding quantitative comparison**; the strongest concrete conclusion is that asynchronous inference-control decoupling further improved real-world deployment performance.

## Link
- [http://arxiv.org/abs/2603.05982v1](http://arxiv.org/abs/2603.05982v1)
