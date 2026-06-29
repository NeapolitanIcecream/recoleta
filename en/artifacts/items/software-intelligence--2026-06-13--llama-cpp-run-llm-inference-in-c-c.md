---
source: hn
url: https://llama-cpp.com/
published_at: '2026-06-13T23:50:55'
authors:
- doener
topics:
- llm-inference
- c-cpp
- quantization
- local-deployment
- cross-platform
relevance_score: 0.77
run_id: materialize-outputs
language_code: en
---

# Llama.cpp – Run LLM Inference in C/C++

## Summary
Llama.cpp is a C/C++ runtime for running LLM inference on local hardware with low overhead and broad platform support. It matters because it makes quantized models usable on CPUs and common GPUs without a separate runtime stack.

## Problem
- Running LLMs often needs large runtimes, GPUs, and platform-specific setup.
- Many users want local inference on CPUs, laptops, phones, and mixed hardware.
- Model files and execution paths need to stay portable across systems and accelerators.

## Approach
- It loads models in GGUF, a single portable file that stores weights, tokenizer data, and metadata.
- It auto-detects CPU features and available GPUs, then chooses execution paths and kernels for the machine.
- It uses quantized weights, optimized attention, and key-value caching for inference.
- It can offload some layers to GPU when available and stream tokens as they are generated.
- It supports C++11 builds with no external runtime dependencies beyond optional accelerator SDKs.

## Results
- The excerpt gives no benchmark table or accuracy numbers.
- It claims real-time response generation for local inference.
- It supports many targets: Linux, macOS, Windows, Android, iOS, FreeBSD, x86, ARM, CUDA, ROCm, Metal, Vulkan, OpenCL, and SYCL.
- It claims practical model sizes of about 2-10 GB for 7B-13B parameter models in GGUF form.
- It can run with as little as 4 GB RAM for small models, with 16 GB+ RAM and AVX2 for broader use.

## Link
- [https://llama-cpp.com/](https://llama-cpp.com/)
