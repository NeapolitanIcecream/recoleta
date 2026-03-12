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
---

# AnyCamVLA: Zero-Shot Camera Adaptation for Viewpoint Robust Vision-Language-Action Models

## Summary
本文提出 AnyCamVLA，一种面向视觉-语言-动作模型（VLA）的零样本相机适配框架，在**不增加示教数据、不微调策略、不改网络结构**的前提下提升相机视角鲁棒性。核心思想是在测试时把当前相机图像实时合成为训练时视角，再交给冻结的 VLA 执行动作。

## Problem
- VLA 在机器人部署时常需适应新环境，但对相机位姿与内参变化非常敏感，哪怕轻微偏移也会显著掉点；文中提到腕部相机仅 **3 cm** 位移就可能让成功率减半。
- 这很重要，因为真实家庭/办公室场景中的相机外参、内参、甚至手持移动拍摄都很常见；若每次变化都重新收集演示并微调，大模型部署成本很高。
- 现有方法要么依赖大量多视角数据增强和再训练，要么引入深度/点云/3D 特征并修改架构，难以保留 RGB 预训练 VLA 的原始能力与可扩展性。

## Approach
- 把问题从“让策略学会所有视角”改成“把测试视角变回训练视角”：给定测试图像、测试相机参数和训练相机参数，先通过相机适配模块合成训练视角图像，再输入冻结策略。
- 该适配模块使用前馈式新视角合成模型（文中采用 **LVSM**），可处理**外参和内参**变化，并支持输入/输出相机数量不同。
- 整体流程很简单：采集测试相机图像 → 合成训练视角图像 → 输入原始 VLA → 输出动作；因此是 plug-and-play，可用于任意 RGB-based policy。
- 由于新视角合成只改视觉输入，不改策略参数，所以避免了额外机器人示教、策略遗忘和架构改造，同时尽量保留 VLA 已学到的视觉-语言先验。
- 运行上满足实时性：文中报告 LVSM 在 **256×256**、2 输入到 2 输出视角时延 **36.55 ms**，约 **27 FPS**；论文图示中适配约 **30 Hz**、VLA 控制约 **10 Hz**。

## Results
- 在 **LIBERO** 的未见过 agent camera 视角扰动上，**Ours-π** 在 **All Suites** 的平均成功率达到 **94.5%**，显著高于基线 **π0.5: 67.9%**、**OpenVLA-OFT: 62.1%**、**GeoAwareVLA: 86.1%**；其中大扰动下 Ours-π 仍有 **92.5%**，而 π0.5 仅 **39.9%**、OpenVLA-OFT 为 **46.2%**。
- 在更细分套件上，Ours-π 在 **LIBERO-Object** 的平均成功率为 **98.0%**，高于数据增强微调 **π0.5*: 94.4%**；在 **LIBERO-Long** 平均为 **88.6%**，高于 **π0.5*: 74.3%** 与 **GeoAwareVLA: 82.9%**。
- 在未见过 wrist camera 视角扰动、**LIBERO-Long** 上，**Ours-π** 平均成功率 **88.6%**，优于 **π0.5*: 83.1%**、远高于 **π0.5: 28.6%** 和 **GeoAwareVLA: 5.2%**；大扰动下 Ours-π 仍有 **84.4%**。
- 视角适配消融实验（LIBERO-Long）显示：原始视角上的 **π0.5** 成功率为 **92.4%**；无适配在新视角平均 **49.0%**；**Homography 31.7%**；**Depth projection 81.1%**；**Ours-π 88.6%**。同时图像质量 **PSNR** 最高为 **23.20 dB**（Ours-π），高于 **Depth 18.27 dB**、**Homography 14.72 dB**、无适配 **13.64 dB**。
- 论文还声称在真实机器人操作中，对**外参、内参、自由手持相机**（如 iPhone、ZED、RealSense）都能稳定提升视角鲁棒性，并且在**最高 15 cm 平移、60° 旋转**的相机变化下性能退化很小；但给定摘录未提供对应真实实验的详细数值表。

## Link
- [http://arxiv.org/abs/2603.05868v1](http://arxiv.org/abs/2603.05868v1)
