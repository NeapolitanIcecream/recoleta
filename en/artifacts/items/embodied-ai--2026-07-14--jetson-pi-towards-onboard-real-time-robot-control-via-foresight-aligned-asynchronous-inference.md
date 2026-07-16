---
source: arxiv
url: https://arxiv.org/abs/2607.12659v1
published_at: '2026-07-14T11:38:36'
authors:
- Zebin Yang
- Qi Wang
- Yunhe Wang
- Xiurui Guo
- Bo Yu
- Shaoshan Liu
- Jiafeng Xu
- Hao Dong
- Meng Li
topics:
- vision-language-action
- robot-foundation-model
- edge-inference
- asynchronous-control
- robotic-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference

## Summary
Jetson-PI enables faster onboard VLA control on low-power devices by aligning asynchronous action prediction with the future environment and optimizing edge inference. On NVIDIA Jetson Orin, it reports up to 8.66× higher control frequency than naive PyTorch and 5.41× higher than vla.cpp, while improving LIBERO success over VLASH.

## Problem
- VLA inference is too slow for low-power onboard hardware: the paper reports about 1.4 seconds per inference, or 0.7 Hz, for π₀.₅ on Jetson Orin.
- Asynchronous inference removes pauses but predicts actions from stale observations, causing perception-execution misalignment and delayed reactions as the environment changes.
- This matters because high-end GPUs increase power use and can reduce robot battery life; the paper reports a 6.0× battery-life reduction for an RTX 4090 compared with onboard devices such as Jetson Orin.

## Approach
- A 40M-parameter future correction module predicts a compressed future VLM representation from the current representation and the actions already committed for execution.
- The action expert uses this predicted future representation to generate actions for the time when inference finishes, rather than acting on the outdated observation.
- Confidence-based scheduling skips VLM calls when the predicted future representation is reliable and invokes the VLM when confidence falls below a threshold, while allowing the action expert to run more frequently.
- The edge inference system applies CUDA graph reuse, GPU-resident intermediate buffers, and flow-matching graph unrolling to reduce communication and repeated graph-launch overhead on Jetson hardware.

## Results
- On Jetson Orin, the reported control frequency improves by 8.66× over naive PyTorch and 5.41× over vla.cpp; the abstract also reports a 14.8% average success-rate improvement over VLASH on LIBERO.
- In the Orin ablation, naive π₀.₅ reaches 0.70 Hz with 1,420.8 ms total latency; scheduling reduces reaction time to 674.9 ms and raises frequency to 1.48 Hz, while graph reuse, buffering, and unrolling reach 6.06 Hz with 412.9 ms total latency.
- On LIBERO using π₀.₅ across latency settings Δ=1–9, foresight correction averages 97.0% on LIBERO-Spatial, 98.0% on LIBERO-Object, 96.5% on LIBERO-Goal, and 92.2% on LIBERO-10; adding scheduling raises these to 97.4%, 98.6%, 96.8%, and 92.5%, respectively.
- The reported experiments cover simulation and real-robot deployment across Jetson Orin and Thor, but the provided excerpt does not include the full Thor latency table or detailed real-robot metrics.

## Link
- [https://arxiv.org/abs/2607.12659v1](https://arxiv.org/abs/2607.12659v1)
