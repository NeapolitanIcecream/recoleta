---
source: arxiv
url: https://arxiv.org/abs/2607.14695v1
published_at: '2026-07-16T07:56:43'
authors:
- Yuanchun Guo
- Bingyan Liu
topics:
- vision-language-action
- robot-foundation-model
- streaming-inference
- real-time-control
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Reflex: Real-Time VLA Control through Streaming Inference

## Summary
Reflex enables real-time streaming inference for flow-matching vision-language-action policies by separating timestep-invariant perception from timestep-dependent action denoising. On LIBERO and Kinetix, it reports up to 2.58× faster inference, 50 Hz stable streaming, up to 54% lower reaction latency, and no measured task-performance degradation.

## Problem
- Flow-matching VLA policies require iterative denoising, so synchronous inference can block robot execution and increase reaction latency in dynamic manipulation.
- Standard KV caching is mathematically invalid when timestep conditioning changes representations throughout the network, while full recomputation is too slow for 50–100 Hz control.
- Long-running mixed-precision streaming can become numerically unstable, limiting reliable deployment.

## Approach
- Reflex partitions the attention context into a pinned instruction prefix, a sliding visual-history window, and a dynamic flow-generation suffix. It caches the first two regions and recomputes only timestep-dependent states, reducing updates to O(1) for a fixed context window while matching full-batch attention.
- An asynchronous pipeline runs visual encoding and action generation on separate streams, overlapping perception with execution rather than making the robot wait for each inference cycle.
- AdaRMSNorm computes variance in FP32 and uses timestep and proprioceptive-state conditioning to reduce BFloat16 activation collapse during continuous streaming.
- Future-conditional state prediction compensates for inference delay, while operator fusion and preallocated ring buffers reduce kernel-launch and memory-allocation overhead.

## Results
- On LIBERO with Pi0.5, inference latency falls from 135.2 ms to 52.4 ms, a 2.58× speedup; the larger 3.1B-parameter Pi0 reaches 2.73× speedup.
- Reflex maintains 0.00 MSE against full-batch attention for fixed inputs and a fixed observation window on both LIBERO and Kinetix, whereas the Naive Cache baseline reports MSE greater than 1.0 because it ignores timestep conditioning.
- Peak VRAM decreases by 27% on LIBERO and 24% on Kinetix, and the system achieves stable 50 Hz streaming with reaction-latency reductions of up to 54%.
- The reported task evaluations maintain performance parity on LIBERO and show no performance degradation from streaming; the provided excerpt does not include the complete task-success table or all Kinetix numerical results.
- The exactness guarantee applies to Partitioned Attention under fixed inputs, not to asynchronous scheduling, future-state prediction, or mixed-precision behavior; the method also excludes architectures whose perception encoder receives denoising-timestep conditioning.

## Link
- [https://arxiv.org/abs/2607.14695v1](https://arxiv.org/abs/2607.14695v1)
