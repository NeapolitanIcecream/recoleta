---
source: arxiv
url: https://arxiv.org/abs/2607.20061v1
published_at: '2026-07-22T12:05:13'
authors:
- Hanjing Ye
- Tianle Zeng
- Jiazhao Zhang
- Shaoan Wang
- Zibo Zhang
- Weisi Situ
- Yuchen Zhou
- Yonggen Ling
- Hong Zhang
topics:
- embodied-visual-tracking
- vision-language-action
- robot-foundation-model
- target-identification
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# ReferTrack: Referring Then Tracking for Embodied Visual Tracking

## Summary
## 摘要
ReferTrack 将目标选择与航点预测分开，同时将两者保留在同一个视觉-语言-动作策略中，从而改进具身视觉跟踪。在单前视摄像头的 EVT-Bench 设置下，该方法使用一个 4B 参数模型，仅通过监督微调，在三个划分上都取得了当前最佳结果。

## 问题
- 移动机器人必须仅依靠机载视觉，持续跟随自然语言指定的人，同时保持 1–3 米的距离并让该人处于视野内。
- 在拥挤或存在歧义的场景中，VLA 策略可能通过难以监督、且与图像检测关联较弱的抽象空间 token 进行推理；可靠的目标识别十分重要，因为识别错误会直接削弱跟踪与导航效果。

## 方法
- ReferTrack 首先运行 YOLO11 和 ByteTrack，将检测到的行人放入带索引的边界框目录中，然后预测一个 Refer-CoT token，用于选择指令所指的人，或选择 `<NO_EXIST>` 选项。
- 随后，模型以所选索引为条件预测航点，先将目标识别转化为对图像空间候选目标的有监督离散选择，再生成导航动作。
- 一个滑动窗口队列保存历史上选定的边界框，并通过 temporal-viewpoint-bbox indicator（TVBI）token 将其几何信息注入视觉历史，为目标提供特定的运动线索。
- 模型在 130 万条模拟跟踪轨迹和 130 万条基于 SYNTH-PEDES 构建的自定义 Refer-QA 样本上进行联合训练，使用轨迹损失、指代损失和文本损失，并对 Qwen3-4B 主干网络及辅助模块进行完全微调。

## 结果
- 在单视角 EVT-Bench 上，ReferTrack 在 Single-Target Tracking 中取得 89.4% SR、92.5% TR 和 1.6% CR；在 Distracted Tracking 中取得 73.3% SR、81.8% TR 和 7.6% CR；在 Ambiguity Tracking 中取得 74.1% SR、85.7% TR 和 7.7% CR。
- 与单视角 TrackVLA++ 基线相比，该方法在 Distracted Tracking 上将 SR 提高 6.8 个百分点、TR 提高 13.0 个百分点；在 Ambiguity Tracking 上将 SR 提高 22.9 个百分点、TR 提高 22.3 个百分点。
- 在 Distracted Tracking 上，同时移除 Refer-CoT 和 TVBI 后，性能降至 55.7% SR 和 71.4% TR；仅移除 TVBI 后，性能降至 70.4% SR 和 80.8% TR。
- 使用真实目标边界框的 oracle 变体在 Distracted Tracking 上达到 81.5% SR 和 84.7% TR，而完整模型为 73.3% 和 81.8%；因此，论文将目标识别确定为当前仍待解决的主要瓶颈之一。
- 论文还报告了在腿式机器人和人形机器人上的真实部署结果，将其作为仿真到现实迁移能力的证据；但所提供的摘录没有给出部署指标，也没有提供受控的真实环境基线比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.20061v1](https://arxiv.org/abs/2607.20061v1)
