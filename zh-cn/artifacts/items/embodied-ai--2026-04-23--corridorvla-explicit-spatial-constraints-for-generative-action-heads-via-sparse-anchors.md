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
## 总结
CorridorVLA 通过预测少量未来末端执行器运动锚点，并用它们来塑造动作损失，为视觉-语言-动作策略加入了显式空间约束。在 LIBERO 和 LIBERO-Plus 上，它在 SmolVLA 和 GR00T 上都带来了稳定提升，而且几乎不需要改动架构。

## 问题
- 许多 VLA 模型把空间引导放在潜在特征或视觉特征里传递，所以动作头只能间接获得位置和运动信息。
- 在机器人操作中，生成的动作轨迹可能偏离合理的空间推进，尤其是在 flow matching 这类随机生成式动作头下。
- 这很重要，因为更好的空间引导能提高长时序、接触密集型操作基准上的任务成功率，比如 LIBERO 和 LIBERO-Plus。

## 方法
- 模型预测 **稀疏空间锚点**：在动作块中的选定时间步上，预测少量未来末端执行器 3D 增量位置。
- 这些锚点定义了目标空间演化周围的一条 **走廊**。如果生成轨迹超出这个容差区域，损失会把它拉回；如果它留在区域内，仍会用一致性项进一步修正。
- 动作输出增加了末端执行器增量位置字段（`extra-A`），让动作头和锚点预测使用同一种物理量。
- 训练由三部分组成：基础 flow-matching 损失、锚点预测损失，以及带缓冲项和走廊内累计一致性项的走廊正则项，并在较低噪声水平下赋予更高权重。
- 这个方法很轻量：论文使用 `K=3` 个锚点 token，其余骨干网络和训练设置基本不变。

## 结果
- **LIBERO，SmolVLA：** `SmolVLA-Corr` 的成功率从 **86.5%** 升到 **90.95%**，提高 **4.45 个百分点**。按类别看，Long/Goal/Object/Spatial 从 **72.0/89.0/87.0/98.0** 变为 **85.2/90.8/95.8/92.0**。
- **LIBERO-Plus，SmolVLA：** 成功率从 **45.37%** 升到 **57.74%**，提高 **12.37 个百分点**（文中写作 **12.4%**）。按类别看，得分从 **46.53/35.89/66.2/32.85** 变为 **49.27/55.27/72.36/54.04**。
- **LIBERO-Plus，GR00T：** `GR00T-Corr` 的成功率从 **75.23%** 升到 **83.21%**，提高 **7.98 个百分点**。按类别看，得分从 **62.21/68.54/84.55/85.64** 变为 **74.55/85.75/88.4/84.14**。
- **锚点目标选择：** 预测 **增量位置** 比绝对位置更好，在 LIBERO 4-in-1 上，平均成功率是 **87.5%**；绝对位置是 **86.5%**，基础模型也是 **86.5%**。
- **组件组合：** 在 LIBERO 上，`merge` 达到 **89.0%**，`+L_buf` 达到 **89.5%**，`+L_cons` 达到 **90.4%**，完整的走廊损失达到 **90.95%**，说明走廊里的两个项都有效。
- 论文称新增计算开销可以忽略，因为方法主要只增加了 **3 个未来状态预测 token**，并改动训练目标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21241v1](http://arxiv.org/abs/2604.21241v1)
