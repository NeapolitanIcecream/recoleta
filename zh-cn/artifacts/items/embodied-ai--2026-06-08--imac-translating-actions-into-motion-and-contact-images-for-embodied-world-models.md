---
source: arxiv
url: https://arxiv.org/abs/2606.09813v1
published_at: '2026-06-08T17:55:41'
authors:
- Zhenyu Wu
- Xiuwei Xu
- Yukun Zhou
- Yifan Li
- Qiuping Deng
- Xiaofeng Wang
- Zheng Zhu
- Bingyao Yu
- Ziwei Wang
- Jiwen Lu
- Haibin Yan
topics:
- embodied-world-model
- action-conditioned-video
- robot-policy-evaluation
- contact-aware-control
- long-horizon-rollout
- dexterous-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# iMaC: Translating Actions into Motion and Contact Images for Embodied World Models

## Summary
## 总结
iMaC 是一个面向长时程操作策略评估的动作条件机器人世界模型。它把未来机器人动作转换为渲染出的机器人运动视频和基于点云的接触热力图，再用这些控制信号引导多视角 RGB-D 视频滚动生成。

## 问题
- 机器人策略在真实硬件上的评估速度慢、成本高，而且很难在不同检查点之间重复对比。
- 现有动作条件视频模型通常把动作作为紧凑向量输入，容易漏掉决定接触、物体运动和任务成败的厘米级变化。
- 长时间闭环滚动会放大视觉和几何误差，因为每个生成块都会变成下一段输入。

## 方法
- iMaC 使用机器人 URDF 和正向运动学，把未来关节动作转换为运动图像，也就是从一个头部相机和两个腕部相机渲染未来机器人观测。
- 它预测六联图中的 RGB 和深度，再把预测的深度提升为点云，供后续块使用。
- 它构建两路接触图像流：机器人到场景的距离，以及场景到夹爪的距离，并把它们着色成密集热力图。
- 一个 WAN2.2 的图像到视频 DiT 接收参考帧、带噪的未来视频 token，以及这三路控制视频，并通过潜空间 token 加法进行条件控制。
- 训练时滚动会把分离出来的生成最终帧送入后续块，减少与闭环推理之间的不匹配。

## 结果
- 在 8 个真实机器人长时程操作任务上，iMaC 在列出的模型中取得了最好的平均 FID、PSNR、SSIM 和 FVD：FID 36.96 ± 9.16，PSNR 16.39 ± 1.41，SSIM 0.735 ± 0.037，FVD 489.51 ± 92.65。
- 与 Ctrl-World 相比，iMaC 将 FID 从 48.64 ± 10.68 降到 36.96 ± 9.16，将 FVD 从 591.47 ± 160.30 降到 489.51 ± 92.65，MSE 为 0.028 ± 0.010，对比值为 0.030 ± 0.012。
- 与 ABot-PhysWorld 相比，iMaC 将 MSE 从 0.041 ± 0.017 降到 0.028 ± 0.010，将 FID 从 74.23 ± 22.50 降到 36.96 ± 9.16，将 FVD 从 642.98 ± 105.27 降到 489.51 ± 92.65。
- 在闭环策略评估中，世界模型的成功估计与真实世界成功在 8 个任务中的 6 个任务上相关，r = 0.833 到 0.956。
- 另外两个较弱的任务报告 r = 0.678 和 r = 0.428；论文把这些失败归因于可用相机对高度关系观察不足。
- 评估覆盖 2 个 VLA 策略家族，π0.5 和 GigaBrain-0.5，每个家族各 3 个检查点，每个评估组 30 个回合。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09813v1](https://arxiv.org/abs/2606.09813v1)
