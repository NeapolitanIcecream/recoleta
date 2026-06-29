---
source: arxiv
url: https://arxiv.org/abs/2605.17912v1
published_at: '2026-05-18T06:18:21'
authors:
- Yu Shang
- Yinzhou Tang
- Yiding Ma
- Zhuohang Li
- Lei Jin
- Weikang Su
- Xin Jin
- Zhaolu Wang
- Ziyou Wang
- Xin Zhang
- Haisheng Su
- Weizhen He
- Wei Wu
- Haoyi Duan
- Gordon Wetzstein
- Xihui Liu
- Dhruv Shah
- Zhaoxiang Zhang
- Zhibo Chen
- Jun Zhu
- Yonghong Tian
- Tat-Seng Chua
- Wenwu Zhu
- Chen Gao
- Yong Li
topics:
- embodied-world-models
- visuotactile-robotics
- robot-benchmarking
- rl-world-models
- sim2real
- dexterous-manipulation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# WorldArena 2.0: Extending Embodied World Model Benchmarking on Modality, Functionality and Platform

## Summary
## 总结
WorldArena 2.0 是一个面向具身世界模型的基准，增加了视触觉感知、在学习到的动态中进行 RL 训练，以及真实机器人评测。它检验模型是否能预测包含接触的交互，并帮助训练可跨机器人平台迁移的策略。

## 问题
- 现有的具身世界模型基准主要关注仅视觉的视频预测，因此遗漏了接触、打滑、摩擦和对力敏感的操作所需的触觉信号。
- 许多评估止步于固定策略打分或开放环规划，因此没有检验世界模型是否能通过多次想象滚动支持策略改进。
- 只看模拟器分数无法说明学习到的动态是否能帮助真实机器人，尤其是在具身形态、传感器和物理接触发生变化时。

## 方法
- WorldArena 2.0 从三个维度扩展 WorldArena：模态、功能和平台。
- 在模态维度上，它把视频世界模型升级为触觉 VAE、双流视触觉去噪模型和动作扩散头；UniVTAC 用来评估触觉 PSNR、触觉 SSIM 和任务成功率。
- 在功能维度上，它把学习到的转移模型当作 RL 环境：策略作用于预测观测，奖励模型给转移打分，优化器根据想象滚动更新策略。
- 在平台覆盖上，它评估 RoboTwin 2.0、LIBERO，以及一台真实的 AgileX Split-Type ALOHA 机器人，并在六个任务上使用 data-engine 和 action-planner 协议。

## 结果
- 论文报告了 12 个具身世界模型在模拟和真实机器人设置下的实验，摘录中给出了 UniVTAC 和 RoboTwin 2.0 的详细数值。
- 在 UniVTAC 的 Insert HDMI 和 Lift Bottle 上，Wan2.2 的触觉预测质量最好：21.26 PSNR 和 0.746 SSIM。它在 Insert HDMI 上的任务成功率是 100%，在 Lift Bottle 上是 0%，平均 50%。
- 在同样的 UniVTAC 任务上，ACT 在 Insert HDMI 上达到 20%，在 Lift Bottle 上达到 80%，平均 50%；Vidar 的结果是 13.97 PSNR、0.278 SSIM、Insert HDMI 70%、Lift Bottle 0%、平均 35%。
- Genie Envisioner 的触觉预测达到 13.36 PSNR 和 0.456 SSIM，但在两个 UniVTAC 任务上都没有成功。
- 在 RoboTwin 2.0 的 RL 环境评估中，基于模拟器的 RL 仍然最高：Click Bell 为 87.30-87.45%，Adjust Bottle 为 78.90%。在世界模型中，WoVR 在 Click Bell 上用 proxy rewards 达到 75.00%，用 VLM rewards 达到 69.38%；Ctrl-World 在 Adjust Bottle 上用 proxy rewards 达到 70.70%，用 similarity rewards 达到 66.02%。
- 摘录提到真实世界的 AgileX ALOHA 任务，包括倒水和擦桌子，并声称存在 sim-to-real 可用性差距，但没有给出真实机器人成功率表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17912v1](https://arxiv.org/abs/2605.17912v1)
