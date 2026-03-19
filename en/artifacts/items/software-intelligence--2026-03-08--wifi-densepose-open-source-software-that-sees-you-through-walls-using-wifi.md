---
source: hn
url: https://github.com/ruvnet/RuView
published_at: '2026-03-08T23:42:57'
authors:
- CGMthrowaway
topics:
- wifi-sensing
- through-wall-sensing
- edge-ai
- pose-estimation
- vital-sign-monitoring
- rust
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# WiFi-DensePose – open-source software that sees you through walls using wifi

## Summary
This is an open-source edge WiFi sensing system that attempts to reconstruct human pose, detect presence, and estimate breathing and heart rate using only wireless signals rather than cameras or wearables. Its core selling points are low-cost ESP32/CSI hardware, local execution, self-supervised learning, and an engineered implementation for multi-node deployment.

## Problem
- Traditional human sensing usually relies on cameras, cloud inference, or wearables, which create issues around privacy, deployment cost, line-of-sight occlusion, and network dependence.
- Performing pose, vital-sign, or through-wall sensing using only ordinary wireless signals in an environment is difficult because CSI signals are noisy, strongly dependent on room conditions, and easily confused in multi-person settings.
- This problem matters because it could provide **contactless, non-visual, offline-capable** spatial sensing for healthcare, security, robotics, buildings, and disaster response.

## Approach
- Use CSI (Channel State Information) instead of images: human movement or breathing changes WiFi multipath scattering, and the system recovers 17 body keypoints, respiration rate, heart rate, and presence state from these disturbances.
- The signal pipeline is a hybrid of “physics + learning”: it first performs phase cleaning, Hampel filtering, SpotFi/Fresnel/BVP/spectral processing, then feeds the result into models based on Transformers, graph networks, and cross-attention.
- Multi-node, multi-frequency fusion: 4-6 ESP32 nodes cooperate via TDM, fuse across channels 1/6/11 into 168 virtual subcarriers, and apply attention-weighted fusion and coherence gate stabilization over N×(N-1) links.
- Emphasizes edge self-learning: it claims no training cameras, cloud, or manual labeling are needed, can form 128-dimensional room/activity fingerprints on-device, and continuously adapt to new environments; it also proposes MERIDIAN for cross-room generalization and SONA for continual adaptation.
- On the engineering side, the system provides a Rust primary implementation, REST/WebSocket API, WASM edge modules, RVF single-file model packaging, and standalone ESP32 operation.

## Results
- **Speed/throughput**: It claims Rust v2 delivers **810x end-to-end acceleration** over the Python v1 implementation, with motion detection improved by **5,400x**; vital-sign detection reportedly reaches **11,665 frames/s** on a single thread.
- **Hardware/deployment**: Edge nodes can cost as little as **about $1/node** (the text also repeatedly says **$8-$9 ESP32-S3**); in one multistatic setup, **4 ESP32-S3 units total $48**, forming **12 TX-RX links** and achieving **360° coverage**.
- **Real-time performance and sampling**: ESP32-S3 nodes reportedly support **28 Hz CSI streaming capture**; multi-node tracking is claimed to support **20 Hz two-person tracking**.
- **Multi-person tracking**: The text claims that under multistatic fusion, it achieves **20 Hz tracking for two people with 0 identity swaps over 10 minutes**; a single AP can distinguish about **3-5 people**, and a **4 AP** retail grid can cover about **15-20 occupants**.
- **Model/resources**: The self-learning model is claimed to run on an **$8 ESP32**, use **55 KB of memory**, and output **128-dimensional fingerprints + 17-joint pose**.
- **Validation/testing**: At the repository level, it claims **60 edge modules** have been implemented and **609 tests passing**; elsewhere it says **542+** Rust tests; an independent audit section reports **1,031 tests passed, 0 failed**. However, it **does not provide key comparative metrics such as pose error on standard academic datasets, heart-rate MAE, or cross-room generalization accuracy**, so its strongest evidence is mainly engineering benchmarks and repository-stated test results rather than paper-style quantified SOTA comparisons.

## Link
- [https://github.com/ruvnet/RuView](https://github.com/ruvnet/RuView)
