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
## 摘要
ECHO 为视觉-语言-动作策略加入连续层次化记忆，使其能在长程任务中复用过去的操作经验。它与 π0 集成后，在 LIBERO-Long 上报告了最大增益。

## 问题
- 长程机器人操作需要记住过去的子目标和动作片段，因为只依赖当前观测的策略可能在多步执行中丢失任务进度。
- 扁平记忆库和线性历史缓冲区在存储经验时缺少任务-子目标-动作结构，数据增长后可能让检索变慢且可靠性下降。
- 论文关注组合泛化：通过复用相关源任务的记忆，解决新的长程任务序列。

## 方法
- ECHO 使用双曲自编码器将 π0 隐状态映射到 Lorentz 双曲空间，然后把成功的子目标片段存为记忆条目。
- 全局任务嵌入作为父节点，子目标转移状态作为子节点；蕴含锥损失把子记忆推入父任务区域内。
- 推理时，ECHO 使用双曲距离和锥约束在记忆树中执行自顶向下的束搜索，然后通过交叉注意力将检索到的记忆与当前状态对齐。
- VLM 引导的下采样器从连续控制流中提取子目标转移，并在记忆插入前过滤失败轨迹。
- 后台整合使用 Lorentzian K-Means 拆分范围较宽的节点，并可通过相关记忆之间的测地线插值合成临时虚拟记忆。

## 结果
- 在 LIBERO-Long 上，ECHO 达到 93.5% ± 2.6 的成功率，Vanilla π0 为 80.7% ± 2.0，绝对提升 12.8 个百分点。
- 在标准 LIBERO 套件上，ECHO 在 Spatial、Object 和 Goal 上分别报告 98.3% ± 1.0、98.8% ± 0.5 和 98.6% ± 1.0；Vanilla π0 分别为 97.5% ± 1.7、97.0% ± 1.2 和 92.3% ± 2.5。
- ECHO 在 LIBERO-Long 上略高于 MemoryVLA：在论文的本地流水线中为 93.5% ± 2.6，对比 92.4% ± 1.1。
- 在 LIBERO-Plus 上，ECHO 将 Vanilla π0 的结果从 54.2% ± 2.9 提高到 56.5% ± 2.0。
- 在跨套件泛化中，ECHO 只使用 LIBERO-Spatial、LIBERO-Object 和 LIBERO-Goal 的记忆，在 LIBERO-Long 上得到 89.31%，Vanilla π0 为 80.70%，没有使用 LIBERO-Long 目标记忆。
- LIBERO-Long 消融结果显示：Vanilla π0 为 80.70%，仅使用短期缓冲区为 88.81%，使用扁平欧氏记忆为 83.25%，使用双曲记忆为 91.11%，使用锥树检索为 92.04%，完整 ECHO 为 93.48%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10993v1](https://arxiv.org/abs/2605.10993v1)
