---
source: arxiv
url: https://arxiv.org/abs/2606.17924v1
published_at: '2026-06-16T13:38:03'
authors:
- Bochen Yang
- Lianlei Shan
topics:
- vision-language-action
- robot-foundation-model
- world-model
- latent-planning
- long-horizon-manipulation
- generalist-robot-policy
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# PearlVLA: Progressive Embodied Action-Plan Refinement in Latent Space

## Summary
## 摘要
PearlVLA 在解码机器人动作之前，为 OpenVLA 风格策略加入多轮潜在规划。论文声称其在 LIBERO 上达到 98.7% 平均成功率，高于摘录中列出的 VLA 基线。

## 问题
- 直接解码 VLA 动作速度快，但策略在执行前几乎没有机会修正计划。
- 文本链、像素级子目标和动作候选搜索可以改善规划，但会增加延迟，或与连续机器人控制产生不匹配。
- 这个问题会影响长时程操作，因为抓取、运动方向或任务理解中的早期小错误可能导致后续任务失败。

## 方法
- 模型以 OpenVLA-7B 为起点，将最终 meta-query token 拆分为固定视觉定位 token 和可写入的潜在计划 token。
- 每轮优化都会把当前潜在计划映射为 world-query 向量，向冻结的 UWM 潜在世界模型查询一个无动作的未来观测潜变量，并将该未来信息反馈到计划中。
- Future-Guided RefineNet 对计划 token 写入残差修正。较大的早期更新处理粗粒度任务方向，较小的后期更新调整计划。
- 经过 K 轮优化后，轻量动作头将最终潜在计划并行解码为一个 H 步连续动作块。
- 第二个训练阶段 CRG-PRL 从同一个优化状态采样 M=8 个残差编辑，用 Robometer-4B 为编辑后的想象未来评分，在组内标准化奖励，并用 PPO 风格目标更新 RefineNet，同时保持部署时推理路径为确定性路径。

## 结果
- PearlVLA 报告在 LIBERO 的 Spatial、Object、Goal 和 Long 套件上达到 98.7% 平均成功率。
- 摘录列出了较强的 LIBERO 基线：π0.5 平均 97.5%，VLANeXt 为 97.4%，FLOWER 为 96.9%，UniVLA 为 95.2%。
- 同一张表还列出了该范围以下的较早回归或分类 VLA 基线：OpenVLA 为 76.5%，WorldVLA 为 79.1%，CoT-VLA 为 83.9%，NORA 平均成功率为 87.9%。
- LIBERO 使用 4 个套件，每个套件 10 个任务，每个套件 500 条专家演示；报告指标为任务成功率。
- 冻结的潜在世界模型为 UWM，在 LIBERO-90 无动作视频上进行了 50K 步后训练，该数据与 4 个评估套件不重叠。
- 摘录说明主 LIBERO 模型使用 K=4 轮优化，CRG-PRL 奖励分组对每个状态使用 M=8 个分支。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17924v1](https://arxiv.org/abs/2606.17924v1)
