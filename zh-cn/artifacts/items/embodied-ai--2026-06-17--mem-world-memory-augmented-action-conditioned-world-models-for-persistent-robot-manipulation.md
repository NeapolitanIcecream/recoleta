---
source: arxiv
url: https://arxiv.org/abs/2606.18960v1
published_at: '2026-06-17T11:42:00'
authors:
- Zirui Zheng
- Jiaqian Yu
- Xiongfeng Peng
- jun shi
- Mingyi Li
- Chao Zhang
- Weiming Li
- Dong Wang
- Huchuan Lu
- Xu Jia
topics:
- robot-world-model
- action-conditioned-video
- memory-retrieval
- persistent-manipulation
- sim2real
- policy-evaluation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Mem-World: Memory-Augmented Action-Conditioned World Models for Persistent Robot Manipulation

## Summary
## 摘要
Mem-World 是一个多视角、动作条件化的机器人世界模型，用几何记忆在长时程操作 rollout 中保持物体细节一致。它针对腕部相机遮挡和快速自我中心运动，这些因素会让以往模型忘记或幻觉生成场景内容。

## 问题
- 当腕部相机被夹爪遮挡，或移开后再返回时，机器人操作世界模型常会丢失物体身份和场景布局。
- Ctrl-World 使用的固定步长历史检索把关节位姿相似度当作间接信号，可能漏掉显示相关物体或表面的帧。
- 这会影响长时程策略评估和合成数据策略训练，因为二者都需要在 rollout 中保留任务物体、目标和与接触相关的细节。

## 方法
- Mem-World 基于 Ctrl-World，从当前观测、未来动作片段和检索到的历史帧预测未来多视角观测。
- 它的主要机制是 W-VMem，一种以腕部视角为中心的 surfel 记忆。surfel 是一个小的表面元素，与过去的视觉观测绑定，并连同时间、视角几何、深度和被操作物体标记一起存储。
- 模型先用前三个相机视角初始化记忆，然后在 rollout 期间用预测的腕部视角帧更新记忆，使时间戳记录移动中的腕部相机看到了什么。
- 对每个未来动作片段，它用正向运动学估计未来腕部相机位姿，从该位姿渲染历史 surfel，按可见性、任务相关性和近因性为过去时间步打分，然后检索 top-K 个非冗余历史帧。
- 检索到的帧为视频模型提供具体视觉证据，用于描述当前腕部帧中可能被遮挡或位于视野外的物体。

## 结果
- 在 34 条 memory-stress DROID 回放轨迹上，第三视角结果相比 Ctrl-World 提升：PSNR 25.30 vs 23.17，SSIM 0.878 vs 0.828，LPIPS 0.054 vs 0.076，物体一致性 0.619 vs 0.573。Cosmos Predict 2.5 的得分为 22.80 PSNR、0.819 SSIM、0.089 LPIPS 和 0.579 物体一致性。
- 在腕部视角预测上，Mem-World 优于 Ctrl-World：PSNR 19.21 vs 17.34，SSIM 0.691 vs 0.623，LPIPS 0.236 vs 0.281，物体一致性 0.524 vs 0.476。
- 在记忆消融实验中，W-VMem 优于短期检索和步长检索。第三视角 PSNR 分别为 W-VMem 24.78、步长检索 22.58、短期检索 21.25；腕部视角 PSNR 分别为 18.97、17.06 和 15.04。
- 在五个任务的策略评估中，Mem-World 的模拟成功率与真实世界成功率的相关性为 r=0.97，p<0.001。Ctrl-World 达到 r=0.85，p<0.01；论文报告 Pearson 相关性提升 14.5%。
- 在策略改进中，作者为每个任务生成 200 条合成轨迹，保留 20–30 条人工标注的成功轨迹，并微调 π0.5。三个长时程任务的平均真实世界成功率从 58% 升至 72%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18960v1](https://arxiv.org/abs/2606.18960v1)
