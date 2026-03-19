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
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics

## Summary
LiteVLA-Edge presents a practical deployment path for embedded robotics: quantize a compact vision-language-action model and run it entirely on Jetson Orin, enabling offline, low-latency, closed-loop control. The paper’s focus is not to introduce a new control objective, but to demonstrate the timing feasibility and engineering reproducibility of local multimodal control on edge devices.

## Problem
- Existing VLA models are typically large, rely on the cloud or desktop-class GPUs, and are difficult to deploy locally in robotic scenarios constrained by power and connectivity.
- Although earlier lightweight approaches can run on edge devices, their inference latency often reaches the order of seconds, allowing only open-loop execution and preventing rapid feedback to dynamic environments.
- This matters because if robots cannot generate actions locally with low latency, they are unlikely to operate safely and reliably in field, tactical, GPS-constrained, or bandwidth-constrained environments.

## Approach
- Use a compact SmolVLM-256M multimodal backbone to map RGB images and language instructions into structured action tokens, which are then dequantized into robot velocity commands.
- Training uses supervised image-to-action fine-tuning, with LoRA fine-tuning in FP32 (rank=8, alpha=8) to preserve action precision.
- For deployment, the trained model is post-training quantized to GGUF 4-bit (Q4_K_M), significantly compressing the model to fit the memory and bandwidth constraints of edge devices.
- Inference uses the CUDA backend of llama.cpp, offloading all 42 layers to the Jetson AGX Orin GPU and setting n_ctx=512 with a maximum output of 12 tokens to reduce KV-cache overhead.
- The system is integrated into a modular ROS 2 perception-reasoning-execution pipeline, where the VLA runs at about 6.6 Hz inference while the low-level controller maintains a 100 Hz heartbeat, balancing semantic reasoning with stable execution.

## Results
- Under the Jetson AGX Orin/Orin NX deployment configuration, the mean end-to-end inference latency is **150.5 ms**, corresponding to an inference rate of **6.64 Hz**; this is the paper’s core quantitative result.
- Latency jitter is extremely low: standard deviation is about **0.125-0.13 ms**, minimum **150.4 ms**, and maximum **151.0 ms**; on this basis, the authors claim the system exhibits deterministic, low-jitter ROS 2 closed-loop operation.
- The paper claims roughly **220% improvement** relative to prior baselines, advancing capability from multi-second open-loop inference to around **150 ms** suitable for closed-loop reactive control.
- Compared with systems in the table: **LiteVLA-Edge 256M** achieves **closed-loop 6.6 Hz** on **Jetson AGX Orin**; **OpenVLA 7B** depends on **RTX 4090** and reaches only **partial ~5 Hz**; **EdgeVLA ~1B** reaches about **10 Hz** on **A100-40GB**. Based on this, the authors emphasize a better “reasoning-to-Hz” balance on low-power hardware.
- The evaluation reports a total of **300 runs** and notes that the latency statistics come from multiple rounds of closed-loop simulation after warm-up; however, it **does not provide task success rate, real-robot manipulation accuracy, or performance gains on standard benchmark datasets**. The evidence is concentrated mainly on deployment latency and system operability.

## Link
- [http://arxiv.org/abs/2603.03380v1](http://arxiv.org/abs/2603.03380v1)
