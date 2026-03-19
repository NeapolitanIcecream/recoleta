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
language_code: zh-CN
---

# AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models

## Summary
本文提出 AnyCamVLA，用实时新视角合成把测试时相机画面“变回”训练时视角，从而让冻结的 VLA 在零样本条件下适应相机位姿与内参变化。其目标是解决机器人策略对相机视角极度脆弱、部署时频繁需要重新收集示范和微调的问题。

## Problem
- 现有经过微调的视觉-语言-动作模型（VLA）对相机视角变化非常敏感，在真实非结构化环境里，轻微相机偏移都会显著降低操控成功率。
- 这种问题很重要，因为机器人部署中相机外参、内参甚至手持移动拍摄都常见；若每次变化都要重采样示范并重新微调，大模型落地成本很高。
- 论文举例指出：腕部相机仅 **3 cm** 偏移就可能让成功率减半；相关已有评测中，成功率可从 **>90%** 降到 **<30%**。

## Approach
- 核心方法很简单：**不改策略，只改输入图像**。在测试时把当前相机视角下的 RGB 图像，实时合成为“仿佛来自训练相机视角”的图像，再送入原始冻结 VLA。
- 为实现这一点，作者将相机适配模块 \(\mathcal{F}\) 建模为前馈式新视角合成模型，输入测试图像和测试/训练相机参数，输出训练视角图像。
- 该方法是 plug-and-play：**不需要额外示范数据、不需要策略微调、不需要改网络结构**，理论上适用于任何 RGB-based policy/VLA。
- 适配模块可处理相机外参和内参变化，并支持输入/输出相机数量不同；文中采用 LVSM，2 输入合成 2 输出在 **256×256** 下延迟 **36.55 ms**，约 **27 FPS**，而 VLA 控制约 **10 Hz**，因此额外开销很小。
- 为缩小仿真域差距，作者只对视角合成模型在自建多视角仿真数据上做微调（**491** 个场景、每场景 **64** 个视角变化），且**不使用任何动作数据**，保持策略本身冻结。

## Results
- 在 **LIBERO** 的未见 agent camera 视角扰动上，**Ours-π** 在 **All Suites** 平均成功率达到 **94.5%**，显著高于基础策略 **π0.5 的 67.9%**、**OpenVLA-OFT 的 62.1%**，也高于数据增强微调 **π0.5\* 的 87.2%** 与 **GeoAwareVLA 的 86.1%**。
- 在更细粒度的 **All Suites / Large** 扰动下，**Ours-π 为 92.5%**，而 **π0.5 为 39.9%**、**OpenVLA-OFT 为 46.2%**、**GeoAwareVLA 为 84.0%**；说明大视角变化下鲁棒性优势更明显。
- 在 **LIBERO-Long** 的未见 wrist camera 扰动上，**Ours-π** 分别在 **Small/Medium/Large** 取得 **91.8/89.6/84.4%**，平均 **88.6%**；对比 **π0.5\* 的 83.1%**、基础 **π0.5 的 28.6%**、**GeoAwareVLA 的 5.2%**。
- 在视角适配消融中（LIBERO-Long），**Ours-π** 平均成功率 **88.6%**、图像质量 **23.20 dB PSNR**，优于 **Depth projection 的 81.1% / 18.27 dB**、**Homography 的 31.7% / 14.72 dB**、以及**无适配的 49.0% / 13.64 dB**。
- 论文还声称，即使在**高达 15 cm 平移、60° 旋转**的相机外参变化下，性能退化依然很小；并在真实机器人场景中验证了对外参、内参和手持相机（如 iPhone、ZED、RealSense）变化的稳健性，但摘录中未给出对应真实实验的量化数字。
- 与数据增强微调相比，作者报告零样本输入适配避免了跨任务泛化差、以及微调过程对原始视角性能的**灾难性遗忘**；图 3 提供了趋势性证据，但摘录未包含完整数值表。

## Link
- [http://arxiv.org/abs/2603.05868v1](http://arxiv.org/abs/2603.05868v1)
