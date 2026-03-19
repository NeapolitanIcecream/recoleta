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
- robot-inference
- parallel-serving
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# OxyGen: Unified KV Cache Management for Vision-Language-Action Models under Multi-Task Parallelism

## Summary
OxyGen proposes a unified KV cache management method for vision-language-action models (VLAs), enabling robots to perform multitask inference such as action generation and language generation in parallel under the same observation. Its core contribution is treating the KV cache as a resource shared across tasks and over time, thereby significantly improving on-device inference efficiency.

## Problem
- Although existing MoT VLAs architecturally support multimodal, multitask outputs, inference systems still usually execute each task independently, causing shared observations to be repeatedly prefilling and creating redundant computation.
- Even when part of the computation can be shared, different tasks still contend for resources on constrained hardware such as a single GPU; in particular, action tasks have hard real-time frequency requirements, while language generation can be completed across multiple frames, so their timing constraints are asymmetric.
- This matters because real embodied agents need to manipulate while also conversing / memorizing / planning; if inference cannot run efficiently in parallel, the multitask capabilities of MoT VLAs are difficult to truly deploy on robots at the edge.

## Approach
- The core mechanism is **unified KV cache management**: the VLM backbone KV cache produced from shared observations is treated as a “first-class shared resource,” rather than having each task maintain its own isolated cache.
- **Cross-task KV sharing**: for the same frame of observation, prefill is performed only once, and the resulting KV is reused by both the action expert and the language expert, avoiding repeated encoding of the same input.
- **Cross-frame continuous batching**: language generation is decoupled from the per-frame control loop; action tasks still complete within the current frame, while language requests retain resumable state and continue batched decoding across frames.
- The system uses a unified KV manager to maintain the resumable state for each language request (KV, generated tokens, termination flags), supporting store/retrieve/update/remove as well as batch/unbatch operations, enabling interruption recovery without recomputation.
- This method is implemented on top of $pi_{0.5}$ and openpi, and is an inference/scheduling-layer optimization that largely does not modify the model itself, making it compatible with methods such as compression, pruning, and asynchronous control.

## Results
- The paper claims that on a single **NVIDIA RTX 4090**, based on **$pi_{0.5}$**, and evaluated across **3 benchmarks (LIBERO, DROID, ALOHA)**, OxyGen achieves **up to 3.7× speedup** for multitask parallel inference compared with an isolated-execution baseline.
- In the same system, it can **simultaneously** achieve **200+ tokens/s** language decoding throughput and **70 Hz** action frequency, meeting the need for parallel high-frequency control and continuous language generation.
- The paper breaks the root cause of inefficiency into two parts: **repeated prefill** causes about **1.4× slowdown**, while inter-task **resource contention** causes about **2.6× slowdown**; OxyGen mitigates these two problems through cross-task sharing and cross-frame batching respectively.
- The paper explicitly states that when evaluated on **LIBERO** using the official $pi_{0.5}$-LIBERO checkpoint, OxyGen **does not reduce action quality / task success rate** while accelerating inference, but the provided excerpt does not include specific success-rate values.
- Compared with simple parallelization (such as multi-process GPU sharing) or sequential isolated execution, the authors argue that the key breakthrough is not merely task concurrency, but unified KV cache management that both reduces latency and increases throughput.

## Link
- [http://arxiv.org/abs/2603.14371v1](http://arxiv.org/abs/2603.14371v1)
