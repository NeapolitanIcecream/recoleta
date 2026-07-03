---
source: arxiv
url: https://arxiv.org/abs/2607.01060v1
published_at: '2026-07-01T15:22:41'
authors:
- Byeongguk Jeon
- Seonghyeon Ye
- JaeHyeok Doo
- Sungdong Kim
- Minjoon Seo
- Hyungmok Son
- Kimin Lee
topics:
- robot-policy-evaluation
- video-world-models
- vision-language-action
- generalist-robot-policy
- neural-simulation
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation

## Summary
## 摘要
RoboWorld 通过在一个快速的动作条件视频世界模型中运行通用机器人策略，并用任务进度 VLM 评分标准评估生成的 rollout，来评估通用机器人策略。它报告称，在不进行实体 rollout 的情况下，评估结果与真实 RoboArena 策略排名高度一致。

## 问题
- 通用机器人策略需要在不同任务、物体和环境中进行大量试验，这使真实机器人评估变慢且成本高。
- 手工构建的模拟器需要资产和环境工程，其 sim-to-real 差距可能改变策略排名。
- 视频世界模型可以生成策略 rollout，但长时域伪影、缓慢的去噪过程和二元 VLM 评分可能把模型错误变成错误的策略失败判断。

## 方法
- 该系统在 DROID 上训练一个自回归视频世界模型，初始化自 Wan2.1-T2V-1.3B，并使用因果注意力、动作交叉注意力和逐帧噪声调度。
- Step Forcing 使用与推理阶段相同的少步去噪调度来训练模型，因此 4 步 rollout 条件与训练条件更接近。
- Step Forcing 创建一步自前推先验，让模型在训练中接触自身不完美的上下文，同时不需要运行完整的顺序 rollout。
- 锚定步骤混入带噪声的真实上下文，使动作-观测动态保持与数据相连，而不是由模型诱导状态主导。
- RoboWorld 以闭环方式运行策略：策略动作、生成的下一步多视角观测、再次生成策略动作。VLM 裁判默认使用 GPT-4o，给出 0-5 的任务进度分数，并使用腕部视角检测世界模型伪影。

## 结果
- 在 RoboArena 上，RoboWorld 用 4,186 个生成的 rollout 评估了 8 个开源策略，并与真实世界排行榜匹配，Pearson r=0.989，Spearman rho=0.970。
- 完整的 RoboArena 风格神经评估耗时 100 个 H100 GPU 小时，包括策略动作生成和世界模型 rollout。
- 任务进度 VLM 评分标准相对于 RoboArena 排名达到 Spearman rho=0.970；改用二元成功评分后，rho 降至 0.922。
- 在 BAIR Robot Pushing 上，使用 4 个去噪步骤的 Step Forcing 达到 SSIM 0.8063 ID 和 0.7374 OOD，LPIPS 0.0525 ID 和 0.0768 OOD。使用 8 个步骤的 Teacher Forcing 达到 SSIM 0.7942 ID 和 0.7118 OOD，LPIPS 0.0554 ID 和 0.1058 OOD。
- 在 300 帧、20 秒的 RoboArena 视频生成中，自回归 Step Forcing 运行速度为 15.31 FPS；4 步双向基线为 5.70 FPS。论文报告称，该方法取得总体最佳 LPIPS，并在 4 步方法中取得最佳 SSIM 和 FVD。
- 在 DROID 腕部视角消融中，完整方法的 FVD 为 231.0。移除自前推先验后，FVD 升至 258.5；移除锚定步骤后，FVD 升至 294.0。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01060v1](https://arxiv.org/abs/2607.01060v1)
