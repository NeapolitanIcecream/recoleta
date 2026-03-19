---
source: arxiv
url: http://arxiv.org/abs/2603.07904v1
published_at: '2026-03-09T02:52:57'
authors:
- Zihao Zheng
- Hangyu Cao
- Sicheng Tian
- Jiayu Chen
- Maoliang Li
- Xinhao Sun
- Hailong Zou
- Zhaobo Zhang
- Xuanzhe Liu
- Donggang Cao
- Hong Mei
- Xiang Chen
topics:
- vision-language-action
- dynamic-quantization
- edge-inference
- embodied-ai
- robot-deployment
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# DyQ-VLA: Temporal-Dynamic-Aware Quantization for Embodied Vision-Language-Action Models

## Summary
This paper proposes DyQ-VLA, a temporal-dynamic-aware quantization framework for embodied vision-language-action models that dynamically switches activation bit-widths based on the robot's current motion stage. It aims to significantly reduce memory usage and accelerate inference in simulation and on real robots with almost no loss in control performance.

## Problem
- Although VLA models are powerful, their inference overhead is high, making real-time deployment on edge devices difficult, which directly limits the practicality of embodied intelligence systems.
- Existing static quantization uses fixed precision for the entire task and ignores the large difference in error tolerance between “coarse motion” and “fine manipulation” during robot execution, so it either wastes compute or fails at critical stages.
- More challenging still, the system lacks a sufficiently lightweight, real-time-computable “sensitivity proxy” to determine how many bits are most appropriate at each moment.

## Approach
- The core idea is simple: use lower bits to speed up inference when the robot's actions are “coarse and error-insensitive”; switch back to higher bits or even BF16 when actions are “fine and error-sensitive” to reduce failures in critical operations.
- The method has two parts: first, sensitivity-aware switching uses real-time kinematic signals to decide when to change precision; second, kinematic-guided bit allocation uses those signals to determine whether to allocate 2/4/8/16 bit at the current step.
- The authors find that VLA quantization sensitivity has clear temporal dynamics, and they track it with two types of kinematic proxies: Motion Fineness reflects whether translational motion is delicate, and Angular Jerk reflects whether rotational change is abrupt; their correlations with true sensitivity reach **r=0.90** and **r=0.87**, respectively.
- The system adopts a **static W4 + dynamic A-bit** paradigm: weights are fixed at INT4, while activations switch across steps between **2/4/8 bit** and **BF16**, avoiding the bandwidth overhead caused by dynamically changing weights.
- To prevent frequent oscillatory switching, the framework introduces a hysteresis/delay window mechanism; at the same time, it maps continuous sensitivity into discrete bit choices for constant-time online lookup through offline calibration.

## Results
- The abstract claims that DyQ-VLA uses only **30.9%** of the original model's memory footprint while maintaining **99.5%** of its original performance.
- In terms of speed, the method achieves **1.49×** simulation speedup and up to **1.43×** real-world speedup.
- For sensitivity modeling, the kinematic proxies are strongly correlated with quantization sensitivity: **Motion Fineness r=0.90** and **Angular Jerk r=0.87**, supporting the key hypothesis of “using real-time motion state to guide quantization.”
- The paper also uses progressive perturbation analysis to show that even if local quantization error peaks during some coarse-motion stages, task success rate can still remain high, indicating that “local error magnitude” and “whether the final task fails” are not linearly aligned. This is exactly the basis on which dynamic quantization outperforms static quantization.
- The excerpt does not provide more detailed full experimental table information, such as dataset-level breakdown scores, itemized numerical comparisons with GPTQ/AWQ/QVLA/SQAP-VLA, error bars, or significance tests.

## Link
- [http://arxiv.org/abs/2603.07904v1](http://arxiv.org/abs/2603.07904v1)
