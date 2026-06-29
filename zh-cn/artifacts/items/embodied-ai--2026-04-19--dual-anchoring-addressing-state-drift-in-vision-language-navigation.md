---
source: arxiv
url: http://arxiv.org/abs/2604.17473v1
published_at: '2026-04-19T15:03:38'
authors:
- Kangyi Wu
- Pengna Li
- Kailin Lyu
- Lin Zhao
- Qingrong He
- Jinjun Wang
- Jianyi Liu
topics:
- vision-language-navigation
- video-llm
- world-model
- instruction-following
- long-horizon-navigation
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Dual-Anchoring: Addressing State Drift in Vision-Language Navigation

## Summary
## 摘要
Dual-Anchoring 通过强制 Video-LLM 跟踪指令进度并记住经过的地标，来应对视觉语言导航中的状态漂移。论文声称，这样能减少长时程失败，并在 VLN-CE 基准上取得新的或接近最优的结果。

## 问题
- 在较长的导航回合中，VLN 代理会丢失对哪些指令步骤已经完成、哪些地标已经经过的跟踪。论文把这类失败称为 **进度漂移** 和 **记忆漂移**。
- 标准的下一步动作训练可以生成局部正确的移动，但不会维持准确的内部任务状态，所以错误会在长轨迹中不断累积。
- 这很重要，因为连续 3D 环境中的 VLN 依赖语言、视觉历史和当前位置之间持续对齐，尤其是在 RxR-CE 这类长指令上。

## 方法
- 该方法在 StreamVLN 风格的 Video-LLM 主干上增加了两个训练信号，部署时没有额外推理开销。
- **指令进度锚定：** 模型在预测下一步动作前，先生成一段简短的结构化文本，描述已完成与剩余的子目标。这里的训练数据来自 **360 万** 个用 Qwen3-VL 生成的进度描述样本。
- **记忆地标锚定：** 模型学习重建最近经过的地标对应的、基于 SAM 的目标中心特征，使用回溯式世界模型损失。监督来自用 Qwen3/Qwen3-VL 和 SAM 特征挖掘出的 **93.7 万** 个有标注地标样本。
- 地标分支使用一个可学习的空间查询解码器，对 Video-LLM 输出做交叉注意力，然后用该挖掘地标帧的冻结 SAM 特征作为目标，最小化 MSE。
- 训练采用两阶段流程：先做带动作损失和两个锚定损失的导航预训练，再做 DAgger 和混合微调，加入通用视觉语言数据。

## 结果
- 在 **R2R-CE val unseen** 上，方法报告 **SR 65.6**、**SPL 62.1**、**OSR 69.2**、**NE 4.15**。
- 在 **RxR-CE val unseen** 上，报告 **SR 61.7**、**SPL 53.3**、**NE 4.42**。
- 与 **StreamVLN** 相比，R2R-CE 的 **SR** 从 **56.9 提升到 65.6**（**+8.7** 个点），RxR-CE 的 **SR** 从 **52.9 提升到 61.7**（**+8.8** 个点）。R2R-CE 的 **SPL** 从 **51.9 提升到 62.1**，RxR-CE 的 **SPL** 从 **46.0 提升到 53.3**。
- 与 **DualVLN** 相比，该方法在 **R2R-CE SR**（**65.6 vs 64.3**）、**R2R-CE SPL**（**62.1 vs 58.5**）、**RxR-CE SR**（**61.7 vs 61.4**）和 **RxR-CE SPL**（**53.3 vs 51.8**）上更高，但 **R2R-CE NE/OSR** 略差（**4.15 vs 4.05**、**69.2 vs 70.7**）。
- 摘要还声称 **成功率提升 15.2%**，以及 **长时程轨迹提升 24.7%**，并且在真实世界测试中也有提升，但摘录没有给出这两个汇总说法对应的具体表格或基线。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17473v1](http://arxiv.org/abs/2604.17473v1)
