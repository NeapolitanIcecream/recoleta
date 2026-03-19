---
source: hn
url: https://tiny-whale.vercel.app/
published_at: '2026-03-07T23:07:46'
authors:
- tantara
topics:
- webgpu-inference
- browser-llm
- on-device-ai
- multimodal-chat
- privacy-preserving
relevance_score: 0.1
run_id: materialize-outputs
language_code: en
---

# Show HN: Run Qwen3.5 0.8B in browser (Web and Extension)

## Summary
This is a local inference application that runs open-source multimodal small models directly in the browser, relying on WebGPU to enable serverless, telemetry-free, offline-capable chat and visual question answering. It primarily emphasizes privacy, local execution, and ease of use, rather than proposing a new model or learning algorithm.

## Problem
- Traditional online LLM services usually depend on cloud APIs, creating issues around privacy leakage, network dependence, latency, and barriers to use.
- Users who want to try local AI often need to install complex environments, while usable products that run models natively in the browser are still relatively rare.
- For multimodal capabilities such as image question answering, many tools still require uploading data to servers, which matters significantly in sensitive-data scenarios.

## Approach
- Uses **WebGPU** to execute model inference directly on the user's local GPU, so all computation stays within the browser.
- Provides a browser-based chat interface; after loading an open-source model (the title mentions **Qwen3.5 0.8B**), users can chat locally without registration and without an API.
- Supports **multimodal input**; users can upload images and ask questions, with image processing also completed locally.
- Provides generation parameter controls such as temperature, top-p, top-k, and repetition penalty, letting users tune generation behavior like in a local playground.
- After the model is loaded, it can be used **offline**; the core mechanism is to move inference to the frontend rather than sending requests to a remote service.

## Results
- The text provides no standard benchmark results; it **does not** report accuracy, latency, throughput, memory usage, or quantitative comparisons with other systems.
- The strongest concrete claim is that **all inference runs locally on the GPU via WebGPU**, and that there is **no server, no API calls, and no telemetry**.
- It claims the model can **work offline** after loading, implying subsequent use does not require a persistent internet connection, but no offline performance figures are given.
- It claims support for **multimodal input** (uploading images and asking questions), with processing **completed locally**, but does not specify the range of supported models or visual task metrics.
- The most specific example in the title is that **Qwen3.5 0.8B** can run in the browser, but the excerpt does not report load time, frame rate, token/s, or relative improvement over a baseline.

## Link
- [https://tiny-whale.vercel.app/](https://tiny-whale.vercel.app/)
