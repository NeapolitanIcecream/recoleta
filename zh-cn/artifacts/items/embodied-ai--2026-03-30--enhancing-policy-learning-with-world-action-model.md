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
WAM 在 DreamerV2 世界模型中加入动作预测，让潜变量保留与控制相关的信息，而不只是图像重建信息。在 CALVIN 操作任务上，这个改动同时提升了模仿学习和在学到的模型内进行的 PPO 微调。

## 问题
- 机器人中的标准世界模型通常只训练去预测未来观测，因此它们的潜变量可能缺少策略所需的动作相关细节。
- 在 DiWA 这类流程中，策略直接从这些潜变量学习。如果表示对像素预测有效，但对控制不够好，下游策略学习就会受影响。
- 这很重要，因为更好的潜在动力学可以提高策略成功率，并减少机器人操作所需的真实或模拟训练量。

## 方法
- 论文在 DreamerV2 的 RSSM 世界模型上构建 WAM，并加入一个逆动力学头，用来预测两个连续编码器嵌入之间的动作。
- 训练使用联合损失：潜在动力学的 KL 正则项、未来观测预测的图像重建损失，以及逆动力学头的 L1 动作预测损失。
- 动作头作用在编码器嵌入上，而不是 RSSM 特征上，这样动作预测不会从已经条件化的潜在动力学中变得过于简单。
- 世界模型训练完成后，模型被冻结，用来提取潜在特征；随后在每个任务的 50 个专家回合上，用这些特征训练一个扩散策略进行行为克隆。
- 之后，这个 BC 策略在冻结的世界模型内用基于模型的 PPO 继续微调，使用想象中的潜在轨迹，以及一个用 WAM 特征重新训练的奖励分类器。

## 结果
- 在 CALVIN 的世界模型评估中，WAM 在 230K 训练步后优于 DreamerV2 的所有已报告视频预测指标，而 DreamerV2 需要 2M 步：PSNR 为 22.10 对 21.66，SSIM 为 0.814 对 0.807，LPIPS 为 0.144 对 0.149，FVD 为 10.82 对 12.13。
- 在 8 个 CALVIN 任务上的行为克隆结果中，表 III 显示 WAM 的平均成功率为 61.7%，而 DiWA 为 45.8%。摘要还报告了 71.2% 对 59.4%，所以这段摘录里有两个不同的平均值。
- 在表 III 中，WAM 在 8 个 BC 任务中的 7 个上优于 DiWA，包括 close_drawer 89.7% 对 58.6%、open_drawer 73.3% 对 53.3%，以及 move_slider_right 82.8% 对 51.7%。
- 经过 800 次基于模型的 PPO 微调迭代后，WAM 的平均成功率达到 92.8%，DiWA 为 79.8%，提升了 13.0 个百分点。
- 经过 PPO 调优后，WAM 在两个任务上达到 100.0% 成功率：turn_on_lightbulb 和 turn_off_led。其他已报告的提升包括 open_drawer 96.7% 对 74.4%，以及 turn_on_led 96.6% 对 86.2%。
- 论文称，这些提升是在比 DreamerV2 基线少 8.7 倍的世界模型训练步数下得到的；用 WAM 特征训练的奖励分类器在训练数据上的精确率至少为 0.97，召回率为 1.00。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28955v1](http://arxiv.org/abs/2603.28955v1)
