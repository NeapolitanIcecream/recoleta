---
source: hn
url: https://tiny-whale.vercel.app/
published_at: '2026-03-07T23:07:46'
authors:
- tantara
topics:
- browser-llm
- webgpu
- local-inference
- privacy-preserving-ai
- multimodal-chat
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Show HN: Run Qwen3.5 0.8B in browser (Web and Extension)

## Summary
This is a local inference application that runs open-source large models directly in the browser, using WebGPU to enable chat and multimodal interaction without servers or APIs. It emphasizes privacy, local offline availability, and a low-friction experience, demonstrating the feasibility of on-device LLMs in web pages and extensions.

## Problem
- Traditional AI chat products usually rely on cloud inference, bringing issues of **privacy leakage, network dependence, latency, and usage cost**.
- It is difficult for users to directly experience local large-model capabilities **without registration and without deploying a backend**, especially in a browser environment.
- Multimodality and controllable generation parameters often require complex toolchains, while ordinary users lack an **instant-use local AI playground**.

## Approach
- Uses **WebGPU** to execute all model inference on the user's local GPU, allowing the model to run locally in the browser or extension.
- Adopts a **pure frontend local execution** approach: no server, no API calls, no telemetry, and usable offline after the model is loaded.
- Supports **open-source LLM chat** and **multimodal input**, such as uploading images and completing understanding and Q&A locally.
- Provides **generation parameter controls** such as temperature, top-p, top-k, and repetition penalty, allowing users to fine-tune output behavior.

## Results
- The project claims it can run **Qwen3.5 0.8B** in the browser, and supports both **Web and browser extension** formats.
- It explicitly claims **100% local inference**: data “never leaves the device,” with **no server, no API calls, no telemetry**.
- It explicitly claims the model **can work offline after loading**, making it more suitable than online cloud-based solutions for privacy-sensitive and weak-network scenarios.
- Supports **local multimodal processing**: users can upload images and perform Q&A, with processing completed on the local machine.
- The text does not provide **quantitative benchmark results**; it gives no specific numerical comparisons for latency, throughput, VRAM usage, accuracy, or relative baselines.
- The strongest concrete claims are: **free, private, fast, no sign-up required**, while providing a local AI interaction experience with adjustable sampling parameters.

## Link
- [https://tiny-whale.vercel.app/](https://tiny-whale.vercel.app/)
