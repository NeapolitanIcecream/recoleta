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
Dual-Anchoring 通过强制 Video-LLM 跟踪指令进度并记住已经过的地标，来处理视觉-语言导航中的状态漂移。论文称，这种方法能减少长时程任务中的失败，并在 VLN-CE 基准上取得新的最好或接近最好的结果。

## 问题
- 在较长的导航过程中，VLN 智能体会丢失对哪些指令步骤已经完成、哪些地标已经经过的判断。论文将这两类失败称为 **progress drift** 和 **memory drift**。
- 标准的下一动作训练可以产生局部正确的移动，但不会持续维护准确的内部任务状态，因此错误会沿着长轨迹不断累积。
- 这很关键，因为连续 3D 环境中的 VLN 依赖语言、视觉历史和当前位置之间的持续对齐，尤其是在 RxR-CE 这类长指令任务中。

## 方法
- 该方法在 StreamVLN 风格的 Video-LLM 主干上加入两个训练信号，部署时不会增加额外推理成本。
- **Instruction Progress Anchoring：** 模型在预测下一步动作前，先生成一段简短的结构化文本，描述哪些子目标已经完成、哪些还未完成。这部分训练数据来自用 Qwen3-VL 生成的 **360 万** 条进度描述样本。
- **Memory Landmark Anchoring：** 模型通过回顾式世界模型损失，学习重建最近经过地标的、基于 SAM 的目标中心特征。监督信号来自用 Qwen3/Qwen3-VL 和 SAM 特征挖掘出的 **93.7 万** 条落地地标样本。
- 地标分支使用一个可学习的空间查询解码器，对 Video-LLM 输出做交叉注意力，然后对挖掘出的地标帧的冻结 SAM 特征最小化 MSE。
- 训练采用两阶段流程：先用动作损失和两个 anchoring 损失做导航预训练，再结合 DAgger 和通用视觉-语言数据进行混合微调。

## 结果
- 在 **R2R-CE val unseen** 上，该方法报告 **SR 65.6**、**SPL 62.1**、**OSR 69.2**、**NE 4.15**。
- 在 **RxR-CE val unseen** 上，报告 **SR 61.7**、**SPL 53.3**、**NE 4.42**。
- 与 **StreamVLN** 相比，R2R-CE 上的 **SR** 从 **56.9 提升到 65.6**（**+8.7 点**），RxR-CE 上从 **52.9 提升到 61.7**（**+8.8 点**）。R2R-CE 上的 **SPL** 从 **51.9 提升到 62.1**，RxR-CE 上从 **46.0 提升到 53.3**。
- 与 **DualVLN** 相比，该方法在 **R2R-CE SR**（**65.6 vs 64.3**）、**R2R-CE SPL**（**62.1 vs 58.5**）、**RxR-CE SR**（**61.7 vs 61.4**）和 **RxR-CE SPL**（**53.3 vs 51.8**）上更高，但 **R2R-CE NE/OSR** 略差（**4.15 vs 4.05**、**69.2 vs 70.7**）。
- 摘要还声称 **Success Rate 提升 15.2%**、**长时程轨迹提升 24.7%**，并且在真实世界测试中也有提升，但给出的摘录没有展示这两项汇总结论对应的具体表格或基线。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17473v1](http://arxiv.org/abs/2604.17473v1)
