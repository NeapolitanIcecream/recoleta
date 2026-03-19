---
source: arxiv
url: http://arxiv.org/abs/2603.05868v1
published_at: '2026-03-06T03:44:23'
authors:
- Hyeongjun Heo
- Seungyeon Woo
- Sang Min Kim
- Junho Kim
- Junho Lee
- Yonghyeon Lee
- Young Min Kim
topics:
- vision-language-action
- camera-adaptation
- novel-view-synthesis
- zero-shot-transfer
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models

## Summary
This paper proposes AnyCamVLA, a zero-shot camera adaptation framework for Vision-Language-Action models (VLAs) that improves robustness to camera viewpoint changes **without additional demonstration data, policy fine-tuning, or network architecture modification**. The core idea is to synthesize the current camera image in real time into the training-time viewpoint at test time, and then pass it to a frozen VLA to execute actions.

## Problem
- When deploying VLAs on robots, they often need to adapt to new environments, but they are highly sensitive to changes in camera pose and intrinsics; even slight shifts can cause a significant drop in performance. The paper notes that a wrist camera displacement of only **3 cm** can halve the success rate.
- This matters because changes in camera extrinsics, intrinsics, and even handheld mobile capture are common in real home and office environments; if every change requires recollecting demonstrations and fine-tuning, deployment costs for large models become very high.
- Existing methods either rely on large amounts of multi-view data augmentation and retraining, or introduce depth/point cloud/3D features and modify the architecture, making it difficult to preserve the original capabilities and scalability of RGB pre-trained VLAs.

## Approach
- The problem is reframed from “making the policy learn all viewpoints” to “transforming the test viewpoint back to the training viewpoint”: given a test image, test camera parameters, and training camera parameters, a camera adaptation module first synthesizes an image from the training viewpoint, which is then fed into the frozen policy.
- This adaptation module uses a feed-forward novel view synthesis model (**LVSM** in the paper), which can handle changes in both **extrinsics and intrinsics** and supports different numbers of input and output cameras.
- The overall pipeline is simple: capture test camera images → synthesize training-view images → feed them into the original VLA → output actions; therefore it is plug-and-play and can be used with any RGB-based policy.
- Because novel view synthesis only changes the visual input and does not alter policy parameters, it avoids extra robot demonstrations, policy forgetting, and architectural modification, while preserving as much as possible the visual-language priors already learned by the VLA.
- Runtime meets real-time requirements: the paper reports that LVSM has a latency of **36.55 ms** at **256×256** with 2 input and 2 output views, about **27 FPS**; the paper’s figure indicates adaptation at about **30 Hz** and VLA control at about **10 Hz**.

## Results
- Under unseen agent camera viewpoint perturbations in **LIBERO**, **Ours-π** achieves an average success rate of **94.5%** across **All Suites**, significantly outperforming the baselines **π0.5: 67.9%**, **OpenVLA-OFT: 62.1%**, and **GeoAwareVLA: 86.1%**; under large perturbations, Ours-π still reaches **92.5%**, while π0.5 is only **39.9%** and OpenVLA-OFT is **46.2%**.
- On more fine-grained suites, Ours-π achieves an average success rate of **98.0%** on **LIBERO-Object**, higher than data-augmentation fine-tuning **π0.5*: 94.4%**; on **LIBERO-Long**, it averages **88.6%**, higher than **π0.5*: 74.3%** and **GeoAwareVLA: 82.9%**.
- Under unseen wrist camera viewpoint perturbations on **LIBERO-Long**, **Ours-π** achieves an average success rate of **88.6%**, outperforming **π0.5*: 83.1%** and far exceeding **π0.5: 28.6%** and **GeoAwareVLA: 5.2%**; under large perturbations, Ours-π still achieves **84.4%**.
- The viewpoint adaptation ablation study (LIBERO-Long) shows: **π0.5** achieves **92.4%** success on the original viewpoint; without adaptation, the average success rate on new viewpoints is **49.0%**; **Homography 31.7%**; **Depth projection 81.1%**; **Ours-π 88.6%**. At the same time, image quality measured by **PSNR** is highest for **Ours-π at 23.20 dB**, higher than **Depth 18.27 dB**, **Homography 14.72 dB**, and no adaptation **13.64 dB**.
- The paper also claims that in real-world robot manipulation, it can consistently improve viewpoint robustness for **extrinsics, intrinsics, and freely handheld cameras** (such as iPhone, ZED, and RealSense), and that performance degrades only slightly under camera changes of up to **15 cm translation and 60° rotation**; however, the provided excerpt does not include detailed numerical tables for those real-world experiments.

## Link
- [http://arxiv.org/abs/2603.05868v1](http://arxiv.org/abs/2603.05868v1)
