---
source: arxiv
url: http://arxiv.org/abs/2603.14371v1
published_at: '2026-03-15T13:23:56'
authors:
- Xiangyu Li
- Huaizhi Tang
- Xin Ding
- Weijun Wang
- Ting Cao
- Yunxin Liu
topics:
- vision-language-action
- kv-cache
- multi-task-inference
- robotics
- continuous-batching
relevance_score: 0.69
run_id: materialize-outputs
language_code: en
---

# OxyGen: Unified KV Cache Management for Vision-Language-Action Models under Multi-Task Parallelism

## Summary
OxyGen proposes a unified KV cache management mechanism for vision-language-action models, enabling robots to run multitask inference such as actions and language in parallel under the same observation. It treats the KV cache as a core resource shared across tasks and over time, thereby significantly improving on-device inference efficiency.

## Problem
- Although existing MoT vision-language-action models architecturally support multitask outputs, inference systems usually still execute tasks in isolation, causing the same observation to be encoded repeatedly.
- This isolated KV cache management leads to two kinds of inefficiency: **redundant prefill computation** and **GPU resource contention**, which are especially severe in scenarios where actions require hard real-time performance while language generation can be delayed across frames.
- This problem is important because embodied agents need to control robots while also conversing / memorizing / planning, whereas on-device systems typically have only limited compute such as a single GPU.

## Approach
- The core method is **unified KV cache management**: treating the KV cache generated from shared observations as a “first-class shared resource,” rather than having each task hold its own independent copy.
- **Cross-task KV sharing**: within the same frame, the observation is prefilling once to obtain a shared KV cache, which is then reused simultaneously by the action expert and language expert, avoiding redundant encoding.
- **Cross-frame continuous batching**: language generation is decoupled from the per-frame control loop, allowing multiple language requests to be continuously resumed and batch-processed across multiple control frames; action tasks are still completed within each frame to meet hard deadlines.
- The system uses a unified KV manager to store “resumable generation state,” including KV cache, generated tokens, and termination flags, and supports store/retrieve/update/remove and batch/unbatch operations.
- The authors implement this on top of **π_{0.5}** and deploy it within the openpi framework as a scheduling/execution optimization layer above the model, without modifying the model itself.

## Results
- The paper claims that on a single **NVIDIA RTX 4090**, for multitask parallel inference with **π_{0.5}**, OxyGen achieves **up to 3.7× speedup** relative to isolated execution.
- Under representative robotic configurations and across **3 benchmarks** (**LIBERO, DROID, ALOHA**), the system simultaneously reaches **over 200 tokens/s** language throughput and **70 Hz** action frequency.
- The authors explicitly state that the two additional overheads in isolated execution include **1.4× slowdown caused by redundant computation** and **2.6× slowdown caused by resource contention** (citing Sec. 4.3).
- The paper also claims that the above speedup comes **without action quality degradation**, and checks task success rate on **LIBERO** to verify that action quality is not reduced.
- In the provided excerpt, aside from the throughput / frequency / speedup numbers above, no finer-grained per-benchmark value tables, exact success-rate percentages, or complete quantitative comparisons with the Parallel baseline are provided.

## Link
- [http://arxiv.org/abs/2603.14371v1](http://arxiv.org/abs/2603.14371v1)
