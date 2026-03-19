---
source: arxiv
url: http://arxiv.org/abs/2603.03380v1
published_at: '2026-03-03T03:20:52'
authors:
- Justin Williams
- Kishor Datta Gupta
- Roy George
- Mrinmoy Sarkar
topics:
- vision-language-action
- edge-robotics
- quantization
- on-device-inference
- ros2
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics

## Summary
LiteVLA-Edge presents a practical deployment path for embedded robotics: quantize a compact vision-language-action model and run it entirely on Jetson Orin for local closed-loop control. The paper’s focus is not to propose a new policy learning objective, but to demonstrate that low-latency, offline, ROS 2-compatible multimodal control is feasible at the edge.

## Problem
- Existing VLA models often rely on >7B parameters and desktop/cloud GPUs, making it difficult to satisfy embedded robotics constraints on power, bandwidth, and latency.
- Although earlier lightweight approaches can run on edge devices, inference is often on the order of seconds and only supports open-loop execution, preventing timely feedback to environmental changes.
- This matters because field robots, disconnected/GPS-denied environments, and tactical or mobile platforms all require local, low-latency, stable closed-loop control.

## Approach
- Use the compact multimodal backbone **SmolVLM-256M** to map input images and language instructions directly into structured action tokens, then dequantize them into robot control values (such as `Twist` velocity commands).
- Training uses supervised image-to-action fine-tuning: first **FP32** + **LoRA (r=8, α=8)** to preserve action precision, then post-training **4-bit GGUF quantization (Q4_K_M)** to fit edge hardware.
- Deployment is based on **llama.cpp CUDA**, offloading all **42 layers** to the Jetson AGX Orin GPU; at the same time, context is limited to **512** and output to at most **12 tokens** to reduce KV cache overhead.
- The system connects the perception-reasoning-action pipeline in a modular **ROS 2** manner, preserving safety overrides, debuggability, and compatibility with a lower-level **100 Hz** controller.

## Results
- On **Jetson AGX Orin / Orin NX**, end-to-end local inference reaches an average latency of **150.5 ms**, corresponding to an inference frequency of **6.64 Hz / approximately 6.6 Hz**; the paper claims about **~220% improvement** relative to a prior baseline.
- Latency jitter during continuous operation is extremely low: the reported standard deviation is **0.125 ms** (**0.13 ms** in the table), with a minimum of **150.4 ms** and a maximum of **151.0 ms**, across **300** measurements.
- Compared with systems listed in the paper: **OpenVLA (7B, RTX 4090)** reaches only **partial ~5 Hz**; **EdgeVLA (~1B, A100-40GB)** reaches **~10 Hz**; **LiteVLA-Edge (256M, Jetson AGX Orin)** reaches **6.6 Hz** with fully local closed-loop operation.
- The paper claims this frequency has crossed the practical threshold for closed-loop visual servoing (it gives **6–10 Hz** as the entry range for closed-loop visual motion control), enabling robots to respond to dynamic changes within a single human attention window.
- It does not provide success rates, generalization rates, or real manipulation task scores on standard robotic task benchmarks; the strongest empirical conclusion is mainly **deployment feasibility, low latency, low jitter, and stable closed-loop operation**.

## Link
- [http://arxiv.org/abs/2603.03380v1](http://arxiv.org/abs/2603.03380v1)
