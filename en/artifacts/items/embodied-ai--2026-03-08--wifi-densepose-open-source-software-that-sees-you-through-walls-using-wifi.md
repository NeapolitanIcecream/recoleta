---
source: hn
url: https://github.com/ruvnet/RuView
published_at: '2026-03-08T23:42:57'
authors:
- CGMthrowaway
topics:
- wifi-sensing
- csi-pose-estimation
- through-wall-sensing
- edge-ai
- self-supervised-learning
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# WiFi-DensePose – open-source software that sees you through walls using wifi

## Summary
This is an open-source camera-free human sensing system based on WiFi CSI, aimed at enabling pose estimation, presence detection, and vital-sign inference on local edge devices, and it even claims through-wall operation. It extends the academic concept of WiFi DensePose into a deployable software/firmware stack, emphasizing self-learning, low cost, and offline operation.

## Problem
- Traditional visual sensing depends on cameras, wearables, or cloud models, and is limited in privacy-sensitive settings, under occlusion, in smoke/dust, in line-of-sight-constrained situations, and in through-wall scenarios.
- Existing WiFi pose research often relies on synchronized camera supervision for training, making low-cost, long-term, adaptive deployment in real rooms difficult.
- There is a need for a human/environment sensing approach that can leverage existing wireless signals, run in real time at the edge, and minimize the need for labels and connectivity; this is important for security, medical monitoring, smart spaces, and robotic perception in non-line-of-sight environments.

## Approach
- The core mechanism is simple: human movement, breathing, or heartbeat disturbs indoor WiFi radio waves; the system reads the resulting CSI disturbances (subcarrier amplitude/phase) and turns them into “human pose + vital signs + room fingerprint.”
- The sensing pipeline is: ESP32/CSI devices collect CSI → multi-channel/multi-node fusion (e.g. 3 channels × 56 subcarriers = 168 virtual subcarriers) → coherence gating to filter noise → signal processing (Hampel, SpotFi, Fresnel, BVP, spectrograms) → Transformer/GNN/attention backbone → outputs 17 keypoints, breathing/heart rate, presence state, etc.
- The system emphasizes “self-learning” and edge deployment: it learns 128-dimensional environment embeddings/room fingerprints from raw WiFi data, claiming no dependence on cameras, labels, or the cloud; the model is said to run on ESP32-class hardware, with the text stating a model size of about 55 KB.
- Coverage and occlusion robustness are improved through a multi-static mesh design: N nodes form N×(N-1) transmit-receive links, combined with cross-view attention fusion, Kalman tracking, and an environmental field model to reduce blind spots and support multi-person tracking.
- It also adds cross-environment generalization/domain-invariant design (MERIDIAN), using hardware normalization, an adversarial domain classifier, and geometric conditioning, attempting to achieve “train once, deploy in any room.”

## Results
- The paper excerpt **does not provide pose accuracy numbers on standard academic benchmarks** (such as MPJPE/PCK, specific dataset comparisons, error bars, or SOTA rankings), so its human pose / through-wall sensing accuracy cannot be verified.
- On engineering performance, the project claims that Rust v2 delivers **810x end-to-end speedup** over Python v1, including **5,400x improvement** in motion detection; single-threaded vital-sign detection throughput is **11,665 frames/s**.
- In terms of device and system scale, it claims a single AP can distinguish about **3–5 people**, with near-linear scaling across multiple APs; one example says a retail mesh with **4 APs** can cover about **15–20 occupants**.
- For multi-static configurations, it claims that **4 ESP32-S3 nodes (total cost about $48)** can produce **12 TX-RX measurement links**, and increase bandwidth from **20→60 MHz** through channel hopping; it also claims **20 Hz two-person tracking** with **zero identity swaps** over **10 minutes**.
- For edge/hardware metrics, the ESP32-S3 pipeline is claimed to support **28 Hz CSI streaming collection**, edge module sizes of about **5–30 KB**, local decision latency of **<10 ms**, and a full model compressed to **55 KB** running on an approximately **$8** ESP32.
- In terms of validation and engineering completeness, the text claims multiple test suites of **542+**, **609**, and **1,031** all passed, along with **7/7** audit checks passed; however, these speak more to code/implementation completeness than to scientific validation of sensing-task performance.

## Link
- [https://github.com/ruvnet/RuView](https://github.com/ruvnet/RuView)
