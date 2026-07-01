---
source: arxiv
url: https://arxiv.org/abs/2606.31329v1
published_at: '2026-06-30T08:31:35'
authors:
- Dongyoon Hwang
- Byungkun Lee
- Dongjin Kim
- Hyojin Jang
- Hoiyeong Jin
- Jueun Mun
- Minho Park
- Hojoon Lee
- Hyunseung Kim
- Jaegul Choo
topics:
- vision-language-action
- hierarchical-vla
- 3d-trajectory-guidance
- point-cloud-policy
- robot-manipulation
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# 3D HAMSTER: Bridging Planning and Control in Hierarchical Vision Language Action Models through 3D Trajectory Guidance

## Summary
## 摘要
3D HAMSTER 训练一个分层 VLA，让它把机器人末端执行器路径规划为 3D 路径点，再把这些路径点输入点云控制策略。主要主张是：让规划器和控制器都在 3D 度量空间中工作，可以在视觉、语言和空间变化下提高轨迹准确性和操作效果。

## 问题
- 当前分层 VLA 系统通常预测 2D 图像轨迹，而低层机器人策略通常在 3D 点云上执行动作。
- 通过读取每个像素的深度把 2D 路径点提升到 3D，可能会让路径贴在场景表面上，给控制器提供失真的引导。
- 这会影响结果，因为精细操作依赖深度、间隙和接触位置，尤其是在视角、纹理、光照和物体发生变化时。

## 方法
- 规划器基于 Qwen3-VL-8B-Instruct，预测 `(u, v, d)` 形式的路径点序列，其中 `d` 是度量深度。
- 单独的深度编码器处理深度图，把深度 token 投影到语言模型空间，并与 RGB token 融合。
- 密集深度重建损失训练深度通路保留完整场景几何，语言模型损失训练文本形式的轨迹输出；损失使用 `L = L_LM + 0.1 L_depth`。
- 训练混合使用 3D 机器人与空间数据，以及用于保持能力的仅 RGB 数据：RLBench 606K、DROID 123K、InternData-M1 1.5M、RefSpatial 2.2M、RoboPoint 666K、PixMo 171K、LVIS 138K 和 Honey-1M 749K 个样本。
- 低层策略使用 3DFA：它把 `(u, v, d)` 路径点反投影到世界坐标，把它们连同轨迹和场景嵌入一起附加到场景点云，并用整流流匹配预测动作块。

## 结果
- 在由 148 个留出的 DROID 抓取-放置 episode 构建的 DroidSpatial-Bench 上，完整 3D HAMSTER 在 10 cm 阈值下达到 65.5% Both 准确率，相比之下 RoboBrain-2.5-8B 为 60.1%，Gemini-3.0-Pro 为 29.7%，GPT-5.2 为 16.2%，Sonnet-4.6 为 2.0%。
- 在 5 cm 阈值下，完整 3D HAMSTER 在 DroidSpatial-Bench 上得到 63.5% Start、66.2% End 和 41.9% Both 准确率；RoboBrain-2.5-8B 分别得到 61.5%、58.1% 和 39.2%。
- 消融实验显示，基础 Qwen3-VL-8B 在这项任务上接近零：5 cm 和 10 cm 下的 Both 都是 0.7%。加入 3D 轨迹数据后，Both 在 5 cm 下提高到 27.7%，在 10 cm 下提高到 50.0%。
- 加入深度编码器后，Both 准确率在 5 cm 下提高到 42.6%，在 10 cm 下提高到 62.8%；加入密集深度重建后，5 cm 下为 41.9%，10 cm 下为 65.5%。
- 论文还报告了在 11 个 Colosseum 任务、14 个扰动轴上的仿真测试，以及在 Franka Panda 上覆盖 3 个任务家族和 4 个泛化轴的真实世界测试。摘录没有给出对应的成功率或得分表，因此这里可用的具体结论是：3D 引导优于 2D HAMSTER 引导和无引导的 3DFA，并且在外观变化以及未见过的语言、空间和视觉条件下提升最大。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31329v1](https://arxiv.org/abs/2606.31329v1)
