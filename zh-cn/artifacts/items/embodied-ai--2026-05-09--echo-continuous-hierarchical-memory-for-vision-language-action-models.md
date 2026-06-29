---
source: arxiv
url: https://arxiv.org/abs/2605.10993v1
published_at: '2026-05-09T13:06:33'
authors:
- Yanbin Hu
- Jin Cui
- Jiayi Lu
- Ruixuan Yang
- Jun Ye
- Boran Zhao
- Xingyu Chen
- Xuguang Lan
- Pengju Ren
topics:
- vision-language-action
- robot-foundation-model
- hierarchical-memory
- long-horizon-manipulation
- compositional-generalization
- hyperbolic-embeddings
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models

## Summary
## 概要
ECHO 为 Vision-Language-Action 策略加入连续层次记忆，让模型在长时程任务中复用过去的操作经验。与 π0 集成后，它在 LIBERO-Long 上取得了最大的提升。

## 问题
- 长时程机器人操作需要记住过去的子目标和动作片段，因为只看当前观测的策略会在多步执行中丢失任务进度。
- 扁平记忆库和线性历史缓冲区会在不保留任务-子目标-动作结构的情况下存储经验，数据增多后，检索会变慢，也更不稳定。
- 论文关注组合泛化：从相关源任务的记忆中复用经验，解决新的长时程任务序列。

## 方法
- ECHO 用超曲线自编码器把 π0 的隐藏状态映射到 Lorentz 双曲空间，然后将成功的子目标片段存为记忆条目。
- 全局任务嵌入作为父节点，子目标转换状态作为子节点；蕴含锥损失会把子记忆推到父任务区域内。
- 推理时，ECHO 通过双曲距离和锥约束在记忆树中做自顶向下的 beam search，然后用交叉注意力把检索到的记忆与当前状态对齐。
- 一个 VLM 引导的下采样器从连续控制流中提取子目标转换，并在写入记忆前过滤失败轨迹。
- 后台整合用 Lorentzian K-Means 切分较大的节点，也可以通过相关记忆之间的测地线插值合成临时虚拟记忆。

## 结果
- 在 LIBERO-Long 上，ECHO 达到 93.5% ± 2.6 的成功率，Vanilla π0 为 80.7% ± 2.0，绝对提升 12.8 个百分点。
- 在标准 LIBERO 套件上，ECHO 在 Spatial、Object 和 Goal 上分别为 98.3% ± 1.0、98.8% ± 0.5 和 98.6% ± 1.0；Vanilla π0 分别为 97.5% ± 1.7、97.0% ± 1.2 和 92.3% ± 2.5。
- 在论文的本地流程中，ECHO 在 LIBERO-Long 上略高于 MemoryVLA：93.5% ± 2.6 对 92.4% ± 1.1。
- 在 LIBERO-Plus 上，ECHO 由 Vanilla π0 的 54.2% ± 2.9 提升到 56.5% ± 2.0。
- 在跨套件泛化中，只使用来自 LIBERO-Spatial、LIBERO-Object 和 LIBERO-Goal 的记忆，且没有 LIBERO-Long 目标记忆时，ECHO 在 LIBERO-Long 上得分 89.31%，Vanilla π0 为 80.70%。
- LIBERO-Long 消融结果显示，Vanilla π0 为 80.70%，仅短期缓冲区为 88.81%，扁平欧几里得记忆为 83.25%，双曲记忆为 91.11%，锥树检索为 92.04%，完整 ECHO 为 93.48%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10993v1](https://arxiv.org/abs/2605.10993v1)
