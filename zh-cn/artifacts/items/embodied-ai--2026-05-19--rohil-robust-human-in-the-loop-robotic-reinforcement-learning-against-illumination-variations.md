---
source: arxiv
url: https://arxiv.org/abs/2605.19924v1
published_at: '2026-05-19T14:47:38'
authors:
- Shuoqin Zhang
- Yixin Xiong
- Xiru Gao
- Kai Liu
- Ke Wang
- Xichuan Zhou
- Zhe Hu
topics:
- robot-rl
- human-in-the-loop
- illumination-robustness
- world-model-relighting
- offline-fine-tuning
- real-robot-manipulation
relevance_score: 0.58
run_id: materialize-outputs
language_code: zh-CN
---

# RoHIL: Robust Human-in-the-Loop Robotic Reinforcement Learning Against Illumination Variations

## Summary
## 总结
RoHIL 只用已有机器人数据，把已经学会的人机协同机器人强化学习策略适配到新的光照条件。它先重照录制轨迹，再在离线微调时混合重照数据和原始数据，并把策略锚定到原始模型上，以减少遗忘。

## 问题
- HIL-SERL 在训练时所在的工作站上几乎能做到满成功率，但当灯的位置、日光、阴影或高光在几米外的另一个工作站发生变化时就会失败。
- 为每个工作站重新收集演示并运行人机协同强化学习，会让部署成本随着工作站数量增加而上升。
- 直接对光照偏移的数据做离线微调，可能通过灾难性遗忘损坏原工作站策略。

## 方法
- RoHIL 以一次源工作站上的 HIL-SERL 训练为起点，全部适配都在离线完成，不增加真实机器人交互。
- 它使用 Cosmos-Transfer1-DiffusionRenderer，在保留真实动作、奖励和 done 标签不变的前提下，把录制的 RGB 流重照到 4 种 HDRI 目标光照条件下。
- Illumination-Retention Replay 将原始光照的策略数据与重照后的策略数据和演示数据混合；报告中的最佳保留设置是 alpha = 0.75。
- 评论器加入相对冻结源模型的特征锚点，演员加入相对冻结源策略的平均动作锚点。
- 微调使用 L_Critic = L_Bellman + L_feat 和 L_Actor = L_SAC + L_mse，锚点权重分别为 lambda_feat = 0.2 和 beta_mse = 0.1。

## 结果
- 论文评估了 4 个真实机器人 Franka Panda 任务：ram_insertion、usb_insertion、circuit_breaker 和 table_wiping。
- 评估覆盖 10 种光照条件，包括 5 张 HDRI 地图、3 组任务灯聚光配置和 2 组自然窗光偏移。
- RoHIL 在源 HIL-SERL 训练预算后再做 15,000 步离线微调；各任务预算分别为 RAM 60k 步、USB 30k 步、断路器 35k 步、擦桌 95k 步。
- 在 USB 插入任务上，alpha = 0.75 时，带锚定的目标在约 15,000 步时达到 1.00 的源成功率和 1.00 的偏移光照成功率；标准 SAC 微调在报告的训练扫描中最终低得多，为 0.57 的源成功率和 0.73 的偏移光照成功率。
- 在 USB 锚点消融实验中，基于 30 条轨迹，不加锚点时源成功率为 0.77、偏移光照成功率为 0.67；只加特征锚点时为 0.57 和 0.97；只加动作均值锚点时为 1.00 和 0.80；两个锚点都加时为 1.00 和 1.00，平均成功回合时间为源光照 2.75 秒、偏移光照 2.48 秒。
- DiffusionRenderer 在 6.82 小时内、峰值 VRAM 26.80 GB 的条件下重照了 8,000 个转移；同一相机流下，UniRelight 需要 48.63 小时和 39.88 GB。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19924v1](https://arxiv.org/abs/2605.19924v1)
