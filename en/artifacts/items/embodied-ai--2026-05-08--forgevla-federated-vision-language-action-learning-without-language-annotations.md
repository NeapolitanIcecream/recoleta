---
source: arxiv
url: https://arxiv.org/abs/2605.07474v1
published_at: '2026-05-08T09:20:56'
authors:
- Yuhao Zhou
- Yunpeng Zhu
- Yang Zhou
- Jindi Lyu
- Jian Lan
- Zhangyuan Wang
- Dan Si
- Thomas Seidl
- Qing Ye
- Jiancheng Lyu
topics:
- vision-language-action
- federated-learning
- robot-data-scaling
- language-annotation
- non-iid-robotics
- manipulation-benchmarks
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ForgeVLA: Federated Vision-Language-Action Learning without Language Annotations

## Summary
ForgeVLA trains VLA robot policies from distributed vision-action logs without manual language annotations or raw-data pooling. It adds on-device instruction classification, a contrastive planning loss, and server-side adaptive aggregation to improve federated VLA training under non-i.i.d. robot data.

## Problem
- VLA models need vision-language-action triplets, but many deployed robots only log synchronized images and actions.
- Robot logs often cannot be centralized because they come from factories, hospitals, warehouses, or other private settings.
- Federated VLA training suffers under client heterogeneity; the paper identifies vision-language feature collapse as a failure mode where task embeddings lose separation.

## Approach
- A server fine-tunes a pretrained VLM on a small public VLA dataset to build an embodied instruction classifier.
- Each client runs that classifier locally on its own vision-action pairs and maps each sample to a predefined instruction set, creating pseudo VLA triplets on-device.
- Clients train an InternVLA-M1 based VLA model with the normal action loss plus a contrastive planning loss that pulls each sample toward a global task embedding for its predicted instruction.
- The server keeps and updates a global task representation bank from client task embeddings.
- The server aggregates client model updates with an adaptive objective that preserves each client update direction while staying close to weighted averaging.

## Results
- On LIBERO-Goal, ForgeVLA reaches 55.2% success and 100% Pass@50, compared with FedAvg at 28.8% success and 80% Pass@50; the centralized upper bound is 75.8% success.
- On LIBERO-Object, ForgeVLA reaches 98.6% success and 100% Pass@50, compared with FedAvg at 97.6% success and the centralized model at 98.8%.
- On LIBERO-Spatial, ForgeVLA reaches 72.6% success and 100% Pass@50, compared with FedAvg at 68.6% success and 90% Pass@50; the centralized model reaches 85.8%.
- On LIBERO-10, ForgeVLA reaches 63.6% success and 100% Pass@50, compared with FedAvg at 52.8% success and the centralized model at 79.0%.
- The reported gains over FedAvg are +26.4 points on LIBERO-Goal, +1.0 on LIBERO-Object, +4.0 on LIBERO-Spatial, and +10.8 on LIBERO-10.
- The main ForgeVLA experiments use a 3,882.72M-parameter InternVLA-M1 model with 128.10M trainable parameters, 10 clients, 20 communication rounds, and 5 local epochs per round.

## Link
- [https://arxiv.org/abs/2605.07474v1](https://arxiv.org/abs/2605.07474v1)
