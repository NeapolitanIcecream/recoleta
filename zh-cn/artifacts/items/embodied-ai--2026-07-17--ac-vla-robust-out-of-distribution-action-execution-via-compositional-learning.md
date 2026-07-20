---
source: arxiv
url: https://arxiv.org/abs/2607.15714v1
published_at: '2026-07-17T07:51:03'
authors:
- Xiaojiang Peng
- Kai Peng
- Jie Lu
- Zheng Lian
- Zitong YU
- Xiaobo Wang
topics:
- vision-language-action
- robot-foundation-model
- compositional-generalization
- out-of-distribution
- robot-manipulation
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# AC-VLA: Robust Out-of-Distribution Action Execution via Compositional Learning

## Summary
## 摘要
AC-VLA 通过结合子任务监督与基于状态的腕部摄像头输入屏蔽，提升视觉-语言-动作模型在组合式分布外任务中的执行能力。在 LIBERO 上，它将 π₀.₅ 在 Spatial-OOD 和 Goal-OOD 上的成功率提升至 64.2% 和 73.3%；同时，在消融实验中将分布内成功率保持在 96.7%，在标准测试套件中保持在 98.0–98.4%。

## 问题
- VLA 模型往往记忆完整的任务轨迹，并依赖腕部视角的视觉捷径，因此当熟悉的抓取与放置子技能以新的物体-目标或空间配置重新组合时，模型会失效。
- 这一点很重要，因为标准分布内成功率可能掩盖较差的组合泛化能力：π₀.₅ 在 LIBERO-Spatial 上达到 98.8%，但在 Spatial-OOD 上只有 35.5%。

## 方法
- LLM 将每条指令分解为有序子任务，同时，本体感知对齐器利用夹爪状态变化和末端执行器的低位移对轨迹进行分段，从而无需人工标注即可生成密集的离线子任务监督。
- 混合训练结合完整示范与分解后的子任务片段，在保持长时程连贯性的同时，教会策略重新组合可复用的动作。
- 在闭合夹爪阶段，该方法屏蔽腕部摄像头输入并保留第三人称视角，促使模型在放置过程中进行全局空间定位，同时在接近和抓取阶段保留腕部反馈。
- 这些组件与架构无关，并在 π₀.₅ 和 GR00T-N1 VLA 主干上进行评估，无需修改其架构或推理流程。

## 结果
- 在 LIBERO-OOD 上，采用 π₀.₅ 的 AC-VLA 在 Spatial-OOD 和 Goal-OOD 上分别达到 64.2% 和 73.3%，较原始 π₀.₅ 分别提高 28.7 和 26.7 个百分点；总体平均成功率达到 87.3%，而原始 π₀.₅ 为 78.6%。
- 采用 GR00T-N1 的 AC-VLA 在 Spatial-OOD 和 Goal-OOD 上分别达到 36.4% 和 44.0%，较该主干分别提高 18.5 和 19.9 个百分点，同时标准测试套件上的成功率保持在 92.3–99.1%。
- 消融实验显示，混合原始任务与子任务训练取得了 51.6%/67.5% 的分布外成功率，而原始任务训练为 35.5%/46.6%，同时保持 96.6% 的分布内成功率；加入屏蔽后，分布外成功率进一步提高至 64.2%/73.3%，分布内成功率为 96.7%。
- 在使用 6 自由度 PIPER 机械臂进行的真实世界评估中，AC-VLA 将分布外成功率从 35.0% 提高到 82.5%，将总体性能从 64.4% 提高到 85.6%；分布内成功率则从 93.7% 变为 88.7%。
- 摘要片段报告了 LIBERO、LIBERO-OOD、四项真实世界分布内任务以及两个分布外变体上的结果；未提供超出这些评估范围的更广泛证据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15714v1](https://arxiv.org/abs/2607.15714v1)
