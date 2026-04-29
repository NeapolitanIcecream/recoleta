---
source: arxiv
url: http://arxiv.org/abs/2604.21241v1
published_at: '2026-04-23T03:17:50'
authors:
- Dachong Li
- ZhuangZhuang Chen
- Jin Zhang
- Jianqiang Li
topics:
- vision-language-action
- robot-manipulation
- spatial-grounding
- flow-matching
- libero-benchmark
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# CorridorVLA: Explicit Spatial Constraints for Generative Action Heads via Sparse Anchors

## Summary
## 摘要
CorridorVLA 通过预测少量未来末端执行器运动锚点，并用这些锚点塑造动作损失，为视觉-语言-动作策略加入了显式空间约束。在 LIBERO 和 LIBERO-Plus 上，这种方法几乎不需要改动架构，就让 SmolVLA 和 GR00T 都取得了稳定提升。

## 问题
- 许多 VLA 模型通过潜在特征或视觉特征传递空间引导，因此动作头只能间接获得位置和运动信息。
- 在机器人操作中，生成的动作轨迹可能偏离合理的空间推进过程，尤其是在 flow matching 这类带随机性的生成式动作头下更明显。
- 这很重要，因为更好的空间引导可以提高 LIBERO 和 LIBERO-Plus 这类长时程、重接触操作基准上的任务成功率。

## 方法
- 模型预测**稀疏空间锚点**：即动作 chunk 中选定时间步上，少量未来末端执行器 3D delta-position。
- 这些锚点围绕目标空间演化定义出一条**走廊**。如果生成轨迹超出这个容差区域，损失会把它拉回；如果轨迹仍在走廊内，一致性项也会继续细化它。
- 动作输出扩展了末端执行器 delta-position 字段（`extra-A`），这样动作头和锚点预测器使用的是同一种物理量。
- 训练由三部分组成：基础 flow-matching 损失、锚点预测损失，以及 corridor 正则项。后者包含一个 buffer 项和一个走廊内的累积一致性项，并且在较低噪声水平下赋予更高权重。
- 这个方法很轻量：论文使用 `K=3` 个 anchor token，其余主干网络和训练设置基本保持不变。

## 结果
- **LIBERO, SmolVLA：** **SmolVLA-Corr** 的成功率从 **86.5%** 提高到 **90.95%**，增加 **4.45 个点**。Long/Goal/Object/Spatial 四类分数从 **72.0/89.0/87.0/98.0** 变为 **85.2/90.8/95.8/92.0**。
- **LIBERO-Plus, SmolVLA：** 成功率从 **45.37%** 提高到 **57.74%**，增加 **12.37 个点**（文中写作 **12.4%**）。各类别分数从 **46.53/35.89/66.2/32.85** 变为 **49.27/55.27/72.36/54.04**。
- **LIBERO-Plus, GR00T：** **GR00T-Corr** 的成功率从 **75.23%** 提高到 **83.21%**，增加 **7.98 个点**。各类别分数从 **62.21/68.54/84.55/85.64** 变为 **74.55/85.75/88.4/84.14**。
- **锚点目标选择：** 在 LIBERO 4-in-1 上，预测 **delta-position** 优于预测绝对位置，平均成功率分别为 **87.5%** 和 **86.5%**；基础模型也是 **86.5%**。
- **组件组合：** 在 LIBERO 上，`merge` 达到 **89.0%**，`+L_buf` 达到 **89.5%**，`+L_cons` 达到 **90.4%**，完整 corridor loss 达到 **90.95%**，说明两个走廊项都有帮助。
- 论文称新增计算开销可以忽略，因为该方法主要只增加了 **3 个未来状态预测 token**，并修改了训练目标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21241v1](http://arxiv.org/abs/2604.21241v1)
