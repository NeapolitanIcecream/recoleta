---
source: arxiv
url: http://arxiv.org/abs/2603.28955v1
published_at: '2026-03-30T19:56:05'
authors:
- Yuci Han
- Alper Yilmaz
topics:
- world-model
- robot-policy-learning
- inverse-dynamics
- calvin-benchmark
- diffusion-policy
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Enhancing Policy Learning with World-Action Model

## Summary
## 摘要
WAM 在 DreamerV2 世界模型中加入动作预测，让其潜在状态保留对控制有用的信息，而不只是用于图像重建的信息。在 CALVIN 操作任务上，这一改动同时提升了模仿学习表现，以及在学习到的模型内部进行 PPO 微调的效果。

## 问题
- 机器人领域的标准世界模型通常只训练来预测未来观测，因此它们的潜在状态可能缺少策略所需的动作相关细节。
- 在 DiWA 这类流程中，策略直接从这些潜在状态学习。如果表征更适合像素预测而不适合控制，下游策略学习就会受影响。
- 这一点很重要，因为更好的潜在动力学可以提高机器人操作中的策略成功率，并减少真实环境或模拟环境中的训练成本。

## 方法
- 论文在 DreamerV2 的 RSSM 世界模型基础上构建 WAM，并加入一个逆动力学头，用于根据两个连续编码器嵌入之间的变化预测动作。
- 训练使用联合损失：用于潜在动力学的 KL 正则项、用于未来观测预测的图像重建损失，以及用于逆动力学头的 L1 动作预测损失。
- 动作头作用于编码器嵌入而不是 RSSM 特征，这样动作预测就不会因为潜在动力学已经包含动作条件而变得过于简单。
- 世界模型训练完成后，模型被冻结，用来提取潜在特征，供一个扩散策略在每个任务 50 条专家轨迹上通过行为克隆训练。
- 随后，BC 策略在冻结的世界模型内部用基于模型的 PPO 继续微调，使用想象出来的潜在轨迹 rollout，并重新训练一个基于 WAM 特征的奖励分类器。

## 结果
- 在 CALVIN 世界模型评估中，WAM 在 23 万训练步后超过 DreamerV2 在所有报告的视频预测指标上的表现，而 DreamerV2 用了 200 万步：PSNR 22.10 对 21.66，SSIM 0.814 对 0.807，LPIPS 0.144 对 0.149，FVD 10.82 对 12.13。
- 在 8 个 CALVIN 任务的行为克隆结果上，Table III 显示 WAM 的平均成功率为 61.7%，DiWA 为 45.8%。摘要中则写为 71.2% 对 59.4%，因此摘录里出现了两组不同的平均值。
- 在 Table III 的 8 个 BC 任务中，WAM 在其中 7 个任务上超过 DiWA，包括 close_drawer 89.7% 对 58.6%、open_drawer 73.3% 对 53.3%、move_slider_right 82.8% 对 51.7%。
- 经过 800 次基于模型的 PPO 微调后，WAM 的平均成功率达到 92.8%，DiWA 为 79.8%，提高了 13.0 个百分点。
- 有两个经过 PPO 微调的任务在 WAM 上达到 100.0% 成功率：turn_on_lightbulb 和 turn_off_led。其他报告的提升包括 open_drawer 96.7% 对 74.4%，以及 turn_on_led 96.6% 对 86.2%。
- 论文称，在这些提升的同时，WAM 的世界模型训练步数比 DreamerV2 基线少 8.7 倍；此外，基于 WAM 特征训练的奖励分类器在训练数据上达到至少 0.97 的精确率和 1.00 的召回率。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28955v1](http://arxiv.org/abs/2603.28955v1)
