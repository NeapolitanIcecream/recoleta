---
source: arxiv
url: https://arxiv.org/abs/2605.00078v1
published_at: '2026-04-30T14:16:15'
authors:
- Hao Luo
- Wanpeng Zhang
- Yicheng Feng
- Sipeng Zheng
- Haiweng Xu
- Chaoyi Xu
- Ziheng Xi
- Yuhui Fu
- Zongqing Lu
topics:
- latent-world-model
- vision-language-action
- robot-foundation-model
- egocentric-video
- robot-data-scaling
- generalist-robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Being-H0.7: A Latent World-Action Model from Egocentric Videos

## Summary
## 总结
Being-H0.7 在训练时使用未来视频信息来训练机器人策略，在测试时只根据当前观测执行动作。它试图缩小直接 VLA 策略和基于视频滚动预测的 world-action 模型之间的差距，把未来推理放进潜变量 token 里。

## 问题
- 直接的 VLA 策略可能从观测到动作学到捷径映射，因为与视觉输入相比，动作标注很稀疏。
- 基于视频的 world-action 模型加入了未来预测，但像素级滚动预测会增加训练和推理算力，也可能建模了与控制无关的视觉细节。
- 这个问题在长时程和动态操作任务里更重要，因为接触、物体运动和任务进度都会影响下一步动作。

## 方法
- 模型在多模态上下文和动作块之间插入 K=16 个可学习的 latent queries，让 Transformer 在预测动作前先构建一个紧凑的、面向动作的状态。
- 训练时使用两个配对分支：prior 分支读取当前指令、H=4 帧观测、状态和 latent queries；posterior 分支用未来观测的嵌入替换这些 queries。
- 未来帧先用冻结的 ViT 和 Perceiver resampler 编码成 K 个嵌入，再在最后 L=9 层 Transformer 上与 prior latent states 对齐。
- 两个分支都用针对 T=20 个 action chunks 的 flow-matching 动作目标训练，并加入 latent 对齐、norm 和 rank 正则项，减少 latent collapse。
- 推理时移除 posterior 分支，因此策略可以在不生成未来图像的情况下预测动作。

## 结果
- 摘要称它在 6 个仿真基准上达到 state-of-the-art 或接近 state-of-the-art，但给出的文本没有包含表格数值、指标或成功率。
- 真实世界评估报告覆盖 3 个机器人平台和 12 个任务，涉及动态场景、物理推理、运动推理、长时程执行和泛化。
- 论文称 Being-H0.7 在 5 个能力导向的真实世界测试套件中都排在第一，例子包括接住快速滚动的球、向移动容器倒液体、折叠衣物、传送带包裹分拣和钉钉子。
- 带有延迟感知的通用异步分块部署报告为 Being-H 变体每步 3-4 ms，且测试时不生成未来帧。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00078v1](https://arxiv.org/abs/2605.00078v1)
