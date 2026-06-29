---
source: arxiv
url: https://arxiv.org/abs/2606.05015v1
published_at: '2026-06-03T15:38:36'
authors:
- Luca Zanatta
- Grzegorz Malczyk
- Kostas Alexis
topics:
- world-model
- quadrotor-navigation
- sim2real
- model-based-rl
- vision-based-navigation
- robot-generalization
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Generalization of World Models under Environmental Variability for Vision-based Quadrotor Navigation

## Summary
## 总结
这篇论文测试了在仿真中训练的 DreamerV3 世界模型，什么时候能泛化到真实的视觉四旋翼导航。核心结论是，跨环境的自监督重建质量，比仿真中的策略胜率更能预测真实世界迁移。

## 问题
- 研究对象是使用机载深度图像和状态估计进行的无碰撞三维四旋翼导航。
- 主要问题是域偏移：障碍物布局、起始点、目标点、纹理、光照和视角变化，都可能让学到的预测模型失效。
- 这很重要，因为世界模型策略在仿真里看起来很强，但如果学到的动力学和视觉预测不能迁移到真实无人机上，就会在实机上失败。

## 方法
- 作者训练了 DreamerV3 风格的递归状态空间模型世界模型，使用四个仿真随机性等级：固定障碍物（L1）、五种固定布局（L2）、Sobol 采样的障碍物放置（L3）以及完全均匀随机放置（L4）。
- 每个模型通过自监督重建、奖励预测和 KL 正则化，从深度图像、机器人状态和动作中学习。
- 他们用重建 MSE 和 SSIM 对每个训练好的世界模型在所有环境等级上做交叉评估，分成一个使用真实观测的上下文阶段和一个使用开放环模型滚动的想象阶段。
- 他们在学到的潜空间模型内微调 actor-critic 策略，并随机化底层控制器参数来测试动力学不匹配。
- 他们把训练好的系统部署到真实四旋翼上，在未见过的室内布局中测试，包括闭环飞行，以及在只获得 2.5 秒真实传感器上下文后切断传感器、改用想象观测飞行的一次开放环运行。

## 结果
- 超参数搜索发现，表现最好的模型在 RSSM 的确定性和隐藏层大小上都用了 1024，批次序列长度为 64，离散潜变量大小在 L1/L2 中为 64，在 L3/L4 中为 32。
- 离散潜变量大小和批次长度对重建损失影响最大：批次长度带来约 35% 的相对损失差距，离散潜变量大小带来约 35% 到 50%，RSSM 大小约 20%，随机种子低于 5%。
- 在仿真策略评估中，WM3 的跨环境表现最好：L1 的胜率为 97.0%，L2 为 96.5%，L3 为 92.5%，L4 为 89.5%，在 10 个立方体的 OOD 布局上为 72.0%。
- WM1 过拟合了固定布局：它在 L1 上达到 99.5% 的胜率，但在 OOD 上降到 54.5%，OOD 崩溃率升到 44.5%。
- 真实闭环测试使用了一个 13 米长的走廊，里面有七个平面板，缝隙窄到 0.67 米和 0.85 米；WM1、WM2 和 WM4 到达了目标，WM3 作为仿真中最强的策略却失败了。
- 论文还报告了一次真实世界开放环运行：无人机先接收了 2.5 秒的真实输入，然后在传感器被切断后，依靠想象观测完成了 12 米的穿越。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05015v1](https://arxiv.org/abs/2606.05015v1)
