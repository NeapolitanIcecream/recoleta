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
- robot-manipulation
- novel-view-synthesis
- camera-adaptation
- zero-shot-robustness
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models

## Summary
This paper proposes AnyCamVLA, which uses real-time novel view synthesis to “transform” test-time camera images back into the training-time viewpoint, enabling a frozen VLA to adapt in a zero-shot manner to changes in camera pose and intrinsics. Its goal is to address the extreme fragility of robot policies to camera viewpoint changes, which otherwise often require re-collecting demonstrations and re-fine-tuning at deployment time.

## Problem
- Existing fine-tuned vision-language-action models (VLAs) are highly sensitive to camera viewpoint changes; in real unstructured environments, even slight camera shifts can significantly reduce manipulation success rates.
- This matters because changes in camera extrinsics, intrinsics, and even handheld moving cameras are common in robot deployment; if every such change requires re-sampling demonstrations and re-fine-tuning, the cost of deploying large models becomes very high.
- The paper notes, for example, that a wrist camera shift of only **3 cm** can halve the success rate; related prior evaluations have shown success rates dropping from **>90%** to **<30%**.

## Approach
- The core idea is simple: **do not modify the policy, only the input images**. At test time, the RGB image from the current camera viewpoint is synthesized in real time into an image “as if captured from the training camera viewpoint,” and then fed into the original frozen VLA.
- To achieve this, the authors model the camera adaptation module \(\mathcal{F}\) as a feed-forward novel view synthesis model, which takes the test image and the test/training camera parameters as input and outputs an image in the training viewpoint.
- The method is plug-and-play: **it requires no additional demonstration data, no policy fine-tuning, and no network architecture changes**, and in principle applies to any RGB-based policy/VLA.
- The adaptation module can handle changes in both camera extrinsics and intrinsics, and supports differing numbers of input and output cameras; the paper uses LVSM, where synthesizing 2 outputs from 2 inputs has a latency of **36.55 ms** at **256×256**, about **27 FPS**, while VLA control runs at about **10 Hz**, so the added overhead is small.
- To reduce the simulation domain gap, the authors fine-tune only the viewpoint synthesis model on a self-built multi-view simulation dataset (**491** scenes, **64** viewpoint variations per scene), while **not using any action data**, keeping the policy itself frozen.

## Results
- Under unseen agent camera viewpoint perturbations in **LIBERO**, **Ours-π** achieves an average success rate of **94.5%** on **All Suites**, significantly outperforming the base policy **π0.5 at 67.9%**, **OpenVLA-OFT at 62.1%**, and also surpassing data-augmentation fine-tuning methods **π0.5\* at 87.2%** and **GeoAwareVLA at 86.1%**.
- Under the more fine-grained **All Suites / Large** perturbation setting, **Ours-π reaches 92.5%**, compared with **π0.5 at 39.9%**, **OpenVLA-OFT at 46.2%**, and **GeoAwareVLA at 84.0%**; this indicates a more pronounced robustness advantage under large viewpoint changes.
- Under unseen wrist camera perturbations in **LIBERO-Long**, **Ours-π** achieves **91.8/89.6/84.4%** on **Small/Medium/Large**, averaging **88.6%**; this compares with **π0.5\* at 83.1%**, the base **π0.5 at 28.6%**, and **GeoAwareVLA at 5.2%**.
- In the viewpoint adaptation ablation study (**LIBERO-Long**), **Ours-π** achieves an average success rate of **88.6%** and image quality of **23.20 dB PSNR**, outperforming **Depth projection at 81.1% / 18.27 dB**, **Homography at 31.7% / 14.72 dB**, and **no adaptation at 49.0% / 13.64 dB**.
- The paper also claims that even under camera extrinsic changes as large as **15 cm translation and 60° rotation**, performance degradation remains small; it further validates robustness to changes in extrinsics, intrinsics, and handheld cameras (such as iPhone, ZED, and RealSense) in real robot settings, though the excerpt does not provide corresponding quantitative results.
- Compared with data-augmentation fine-tuning, the authors report that zero-shot input adaptation avoids poor cross-task generalization as well as **catastrophic forgetting** of performance on the original viewpoint during fine-tuning; Figure 3 provides trend-level evidence, though the excerpt does not include a complete numeric table.

## Link
- [http://arxiv.org/abs/2603.05868v1](http://arxiv.org/abs/2603.05868v1)
