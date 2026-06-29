---
source: arxiv
url: http://arxiv.org/abs/2604.22152v1
published_at: '2026-04-24T01:50:53'
authors:
- Yaxuan Li
- Zhongyi Zhou
- Yefei Chen
- Yaokai Xue
- Yichen Zhu
topics:
- robot-policy-evaluation
- world-model
- discrete-diffusion
- vision-language-action
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model

## Summary
## 摘要
dWorldEval 是一个基于离散扩散世界模型的机器人策略评估器。它把语言、图像和动作放进同一个 token 序列里，预测未来观测和任务进度 token，目标是在不把每个策略都跑遍所有环境的情况下，对机器人策略进行排序。

## 问题
- 在真实 rollout 和资源密集型模拟器里，大规模评估机器人策略成本很高，尤其是在很多任务和环境上。
- 之前的世界模型评估器常常不能稳定充当代理，因为它们在分布外行为或失败行为下跟不住机器人动作，长时序下也容易漂移。
- 这会让策略排序变得不可靠，因为模型可能把失败判成成功、漏掉失败，或者破坏空间和时间一致性。

## 方法
- 该模型把视觉、语言和机器人动作片段映射到一个离散 token 空间里，用单个 transformer 去做去噪，因此动作是一级输入，而不是弱条件。
- 它使用掩码离散扩散来重建未来 token，联合生成下一时刻的视觉状态和离散进度 token。
- 稀疏关键帧记忆保存低分辨率历史帧，并加入显式帧索引 token，以减少长时序漂移并保持物体布局一致。
- 训练时，任务进度会通过基于里程碑的评分转换成离散的类文本 token；推理时，当预测进度达到 1 就判定成功。
- 论文还引入了 **Δ-LPIPS**，这个指标衡量在给定动作序列下，预测的状态变化与真实状态变化有多一致。

## 结果
- 在 LIBERO 的动作可控性评估中，dWorldEval 的 **Δ-LPIPS** 在 expert 和 failure 子集上都是最优：**0.315 / 0.352**，对比 **WorldEval 0.423 / 0.701**、**WorldGym 0.347 / 0.650**、**Ctrl-World 0.334 / 0.416**。标准 LPIPS 也略好：**0.215**，对比 **0.262 / 0.218 / 0.220**。
- 在长时序往返一致性上，完整模型在动作跨度 **H=5,10,15,20** 下都优于去掉记忆的消融版本，LPIPS 分别为 **0.130、0.145、0.193、0.243**，而消融版本为 **0.177、0.186、0.302、0.411**。
- 在与先前方法的完整一致性对比中，dWorldEval 的往返 LPIPS 仍然最低：在 **H=20** 时为 **0.243**，对比 **WorldEval 0.531**、**WorldGym 0.482**、**Ctrl-World 0.370**。
- 作为策略评估代理，估计成功率与真实执行结果高度相关：LIBERO 多视角上 **r=0.910**，RoboTwin 上 **r=0.927**，真实世界任务上 **r=0.918**。引言里还写到整体 **Pearson r ≈ 0.9**。
- 在 LIBERO 单视角排序上，论文报告 dWorldEval 的排序违规最小，**MMRV = 0.013**，而基线最高到 **0.039**。
- 实验使用了 **LIBERO**（**5.5k** 个专家示范和 **1k** 个失败 rollout）、**RoboTwin**（覆盖 **10** 个任务的 **5.5k** 条轨迹），以及一个真实双臂机器人数据集（覆盖 **5** 个任务的 **5.2k** 条轨迹，其中包括 **1k** 个失败样本）。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22152v1](http://arxiv.org/abs/2604.22152v1)
