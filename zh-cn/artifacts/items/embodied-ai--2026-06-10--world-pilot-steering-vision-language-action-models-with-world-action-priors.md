---
source: arxiv
url: https://arxiv.org/abs/2606.12403v1
published_at: '2026-06-10T17:59:08'
authors:
- Zefu Lin
- Rongxu Cui
- Junjia Xu
- Xiaojuan Jin
- Wenling Li
- Lue Fan
- Zhaoxiang Zhang
topics:
- vision-language-action
- world-action-models
- generalist-robot-policy
- robot-manipulation
- ood-generalization
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# World Pilot: Steering Vision-Language-Action Models with World-Action Priors

## Summary
## 摘要
World Pilot 在 Vision-Language-Action 策略中加入了一个冻结的 World-Action Model，让策略同时接收语言对齐和预测到的场景动态。它面向 OOD 机器人操作任务，在这些任务中，静态图文预训练让 VLA 的动作头缺少接触和运动线索。

## 问题
- 现有 VLA 能很好地编码图像和指令，但它们的预训练来自静态图文对，因此动作生成器缺少对象如何在机器人动作下移动、碰撞、变形或变化的直接模型。
- 这很重要，因为当相机位姿、物体几何、光照、布局、可变形状态或接触容差偏离训练数据时，操作策略往往会失效。
- 论文要解决的问题是：如何把世界模型信号加入 VLA，同时不让策略依赖带噪的生成像素或不准确的逐步动作猜测。

## 方法
- World Pilot 保持 World-Action Model 冻结，并把它作为先验来源。在报告的设置中，ABot-M0 是 VLA 基座，Qwen3-VL 是 VLM 骨干，Cosmos Policy 是 WAM。
- Latent Steering 取出 WAM 的场景演化潜变量，将其投影到 VLA 隐状态空间，加入未来场景标记，并通过残差交叉注意力注入到 VLM 隐状态中。
- Action Steering 取出 WAM 预测的动作轨迹，将其重采样到 VLA 的时域长度，编码成一个前缀 token，再把这个 token 输入 flow-matching 动作生成器。
- WAM 输出可以在训练时缓存；推理时，WAM 在每个决策步在线运行。梯度更新的是 VLA、动作头和融合模块，不更新 WAM。

## 结果
- 在 LIBERO-Plus zero-shot OOD 上，World Pilot 的 Total success 达到 84.7%，高于 Being-H0.7 的 82.1%、ABot-M0 的 80.5% 和 Cosmos Policy 的 79.7%。
- 在 LIBERO-Plus 各轴上，它在 Camera 上以 82.8% 领先 Cosmos Policy 的 69.6%，在 Light 上以 98.6% 领先 Cosmos Policy 的 97.7%，在 Background 上以 96.4% 领先 ABot-M0 和 RIPT-VLA 的 91.6%，在 Noise 上以 93.6% 领先 Cosmos Policy 的 87.3%。
- 在 RoboCasa 上，World Pilot 的成功率是 65.5%。这低于 Cosmos Policy 的 67.1%，但高于 Being-H0.7 的 62.1% 和 ABot-M0 的 54.0%。
- 在 4 个任务、12 个设置、每个任务 100 次示范、每个设置 20 次试验的真实机器人测试中，World Pilot 在每个表格单元里都拿到了最高成功率。例子包括 Fold Towel ID 的 85%，而最佳基线是 55%；Fruit-to-Plate ID 的 90%，而基线是 70%；Container-Lid Alignment 的 lid-pose OOD 为 65%，而基线是 15%。
- World Pilot 在真实机器人 OOD 上的下降幅度都控制在与对应 ID 设置相差 20 个绝对百分点以内，而列出的基线下降了 25 到 50 个百分点。
- LIBERO-Plus 上的消融显示，单独使用 Latent Steering 为 83.7%，单独使用 Action Steering 为 83.1%，两者结合后为 84.7%，相比 ABot-M0 基线的 80.5% 更高。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12403v1](https://arxiv.org/abs/2606.12403v1)
