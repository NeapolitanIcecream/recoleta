---
source: arxiv
url: https://arxiv.org/abs/2606.02577v1
published_at: '2026-06-01T17:59:38'
authors:
- Junjie Ye
- Rong Xue
- Basile Van Hoorick
- Runhao Li
- Harshitha Rajaprakash
- Pavel Tokmakov
- Muhammad Zubair Irshad
- Vitor Guizilini
- Yue Wang
topics:
- robot-world-model
- synthetic-robot-data
- video-diffusion
- sim2real
- robot-data-scaling
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# RoboDream: Compositional World Models for Scalable Robot Data Synthesis

## Summary
## 总结
RoboDream 先固定机器人动作，再用视频扩散模型加入目标物体和场景，从而生成机器人训练视频。论文声称，这些合成数据能提高真实机器人策略的成功率，同时减少遥操作时间。

## 问题
- 机器人模仿学习需要大量示范，而真实遥操作速度慢，因为每次试验都要摆放物体、重置环境并由人操作。
- 现有视频生成方法可以改变外观，但完整生成的机器人视频可能出现错误的机器人形状或不可行的动作，这会损害硬件上的策略表现。
- 先前的运动锚定生成方法，如 AnchorDream，仍需要针对任务或环境进行微调，这限制了它们在新物体、新场景和新相机视角上的使用。

## 方法
- RoboDream 以渲染出的仅机器人轨迹、场景先验图像、物体先验图像、语言指令和全局机器人轨迹作为视频扩散 Transformer 的条件。
- 渲染的机器人视频提供像素级运动锚点，因此生成的示范会把机器人的运动学与可行轨迹绑定在一起。
- 场景先验通过视频潜变量输入进行编码，而物体先验 token 进入自注意力层，这样模型就能把任务物体放入生成视频中。
- 训练先验由 DROID 轨迹自动构建：视觉语言模型识别任务物体，Grounded-SAM 对其分割，OmniPaint 将其移除以生成干净的场景背景。
- 部署有两种模式：检索与重生会把相似的 DROID 轨迹复用到新上下文中；无道具遥操作会在没有实体物体的情况下记录动作，然后再把物体补上。

## 结果
- 该模型从 Cosmos-Predict2 2B 微调而来，使用约 4 万个带相机标定的 DROID 轨迹，在 8 块 NVIDIA A100 GPU 的 2 个节点上训练了 1 周。
- 在 4 个真实世界操作任务上进行评估，每个策略执行 20 次 rollout，Gen-Mix 的平均成功率为 62.5%，高于 Real-50 的 36.3%、Orig-Mix 的 45.0%、Gen-100 的 15.0% 和 Orig-100 的 0%。
- 各任务的 Gen-Mix 成功率分别为：把积木放入杯中 65%，把记号笔放入碗中 55%，从碗中移除记号笔 35%，用毛巾擦桌子 95%。
- 无道具采集 50 条轨迹花了 55 分钟，而 50 个真实遥操作 episode 约需 2 小时，速度约快 2.2 倍；其策略平均成功率为 32.5%，而 Real-50 为 36.3%。
- 将生成数据与 Real-50 混合后，平均成功率从 36.3% 提升到 Mix-100 的 62.5%、Mix-200 的 72.5%、Mix-300 和 Mix-400 的 73.75%。
- 论文报告了零样本生成能力，可通过改变物体先验、场景先验和渲染出的相机视角来控制未见物体、未见场景和新视角的生成。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.02577v1](https://arxiv.org/abs/2606.02577v1)
