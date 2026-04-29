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
dWorldEval 是一个以离散扩散世界模型构建的机器人策略评估器。它将语言、图像和动作放入同一个 token 序列中，预测未来观测和任务进度 token，目标是在不必让机器人在每个环境中实际运行的情况下，对机器人策略进行排序。

## 问题
- 在大规模场景下评估机器人策略成本很高，尤其是在大量任务和环境中，真实 rollout 和依赖大量资产的模拟器都很昂贵。
- 以往基于世界模型的评估器常常难以充当可靠代理，因为在分布外行为或失败行为下，它们往往不能很好地跟随机器人动作，而且在长时域上会发生漂移。
- 这很重要，因为当模型误判成功、漏掉失败，或破坏空间与时间一致性时，策略排序就会变得不可靠。

## 方法
- 该模型将视觉、语言和机器人动作块映射到同一个离散 token 空间，并用一个 transformer 去噪器统一预测，因此动作是核心输入，而不是较弱的附加条件。
- 它使用掩码离散扩散来重建未来 token，并联合生成下一视觉状态和一个离散进度 token。
- 稀疏关键帧记忆会存储低分辨率历史帧，并加入显式帧索引 token，以减少长时域漂移并保持物体布局一致。
- 在训练时，任务进度会通过基于里程碑的打分转换为类似文本的离散 token；在推理时，当预测进度达到 1 就判定任务成功。
- 论文还引入了 **Δ-LPIPS**，这个指标用于衡量在给定动作序列下，预测的状态变化与真实状态变化的匹配程度。

## 结果
- 在 LIBERO 动作可控性评测上，dWorldEval 在 expert 和 failure 子集上的 **Δ-LPIPS** 都是最优，分别为 **0.315 / 0.352**；对比 **WorldEval 0.423 / 0.701**、**WorldGym 0.347 / 0.650**、**Ctrl-World 0.334 / 0.416**。标准 LPIPS 也略好：**0.215**，对比 **0.262 / 0.218 / 0.220**。
- 在长时域往返一致性上，完整模型在动作时域 **H=5,10,15,20** 上都优于去掉记忆模块的消融版本，LPIPS 分别为 **0.130, 0.145, 0.193, 0.243**，而后者为 **0.177, 0.186, 0.302, 0.411**。
- 在与以往方法的完整一致性比较中，dWorldEval 的往返 LPIPS 仍然最低：在 **H=20** 时，结果为 **0.243**，而 **WorldEval 0.531**、**WorldGym 0.482**、**Ctrl-World 0.370**。
- 作为策略评估代理，估计成功率与真实执行结果的相关性很强：在 LIBERO 多视角上 **r=0.910**，在 RoboTwin 上 **r=0.927**，在真实世界任务上 **r=0.918**。引言还提到整体 **Pearson r ≈ 0.9**。
- 在 LIBERO 单视角排序任务中，论文报告 dWorldEval 的排序违例最少，**MMRV = 0.013**，而基线方法最高达到 **0.039**。
- 实验使用了 **LIBERO**（5.5k 条 expert 演示和 **1k** 条失败 rollout）、**RoboTwin**（覆盖 **10** 个任务的 **5.5k** 条轨迹），以及一个真实双臂机器人数据集，其中有 **5.2k** 条轨迹，包含 **1k** 条失败样本，覆盖 **5** 个任务。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22152v1](http://arxiv.org/abs/2604.22152v1)
