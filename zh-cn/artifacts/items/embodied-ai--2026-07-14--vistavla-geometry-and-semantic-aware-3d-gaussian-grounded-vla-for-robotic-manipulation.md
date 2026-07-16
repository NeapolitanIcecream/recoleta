---
source: arxiv
url: https://arxiv.org/abs/2607.12356v1
published_at: '2026-07-14T05:08:50'
authors:
- Mohan Liu
- Zhihao Gu
- Xuanyu Chen
- Haitian Zhang
- Kaimin Mao
- Yan Wu
- Wei-Yun Yau
- Lin Wang
topics:
- robot-foundation-model
- vision-language-action
- 3d-scene-representation
- 3d-gaussian-splatting
- robotic-manipulation
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# VistaVLA: Geometry- and Semantic-Aware 3D Gaussian-Grounded VLA for Robotic Manipulation

## Summary
## 总结
VistaVLA 通过提供紧凑且具有语义 grounding 的三维场景标记，解决视觉-语言-动作策略三维空间推理能力有限的问题。它将三维高斯特征与 Merge-then-Query 压缩相结合，并在真实环境和空间变化测试中报告了更强的操作性能。

## 问题
- 基于二维输入的 VLA 模型缺乏显式的场景级三维表示，这限制了它们在精确操作或接触密集型操作过程中对空间布局和几何约束的推理能力。
- 深度图和点云等现有三维 VLA 输入能够提供几何信息，但无法充分将与语言对齐的高层语义绑定到持久的三维位置上。
- 稠密三维表示会增加实时策略推理的计算成本，因此还需要在三维感知与 VLA 控制之间建立紧凑的接口。

## 方法
- VistaVLA 使用 RGB、深度和多视角特征渲染监督，将 SigLIP2 和 DINOv2-Large 特征提升到可学习的三维高斯基元中。它先将 2,176 维教师特征压缩为 128 维潜在编码，再进行蒸馏。
- 每个高斯基元都存储几何信息和语义特征，从而生成多视角一致的标记；这些标记的空间 grounding 遵循基元的三维位置、可见性、不透明度和深度排序。
- Merge-then-Query 首先应用空间引导且基于语义相似度的合并，将约 100,000 个高斯基元减少到约 1,000 个标记，然后使用 64 个可学习查询标记对其进行摘要，并输入 VLA 主干网络。
- 生成的三维上下文标记与图像标记和语言标记一同输入基于 VLA-Adapter 的策略。该策略预测连续机器人动作，并在执行四个动作后重新规划。

## 结果
- 在七项真实环境操作任务中，VistaVLA 报告的平均成功率比 VLA-Adapter 基线高 22.8 个百分点，并优于所评估的二维和三维基线，包括 VLA-Adapter+Depth 以及规模更大的 pi_0.5 策略。
- 在 PlaceSponge 的深度变化测试中，VistaVLA 的成功率为 9/10，VLA-Adapter 和 VLA-Adapter+Depth 均为 6/10，pi_0.5 为 7/10。
- 在 OrganizeSponge 的位置变化测试中，VistaVLA 的成功率为 3/10，而所有列出的基线均为 0/10，表明它对大幅位置变化的鲁棒性有所提升，但仍然有限。
- 在标准 LIBERO 上，论文报告的平均成功率为 96.05；在零样本 LIBERO-Pro-Swap 空间分布外基准测试中，VistaVLA 的平均成功率达到 12.2，而基线为 1.7。
- MtQ 将标记数量减少了 99%，从约 10^5 个高斯基元压缩为面向策略的 64 个摘要标记，同时保留了报告中与动作相关的空间和语义信息。
- 摘录未提供完整的消融实验结果、置信区间或真实环境中逐任务的成功率，因此无法仅根据所提供的文本完全分离高斯表示和 MtQ 的相对贡献。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.12356v1](https://arxiv.org/abs/2607.12356v1)
