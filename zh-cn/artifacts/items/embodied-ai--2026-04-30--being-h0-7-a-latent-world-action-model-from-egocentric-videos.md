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
## 摘要
Being-H0.7 训练机器人策略在训练时使用未来视频信息，并在测试时仅根据当前观测执行动作。它通过把未来推理移入潜在 token，处理直接 VLA 策略与视频 rollout 世界-动作模型之间的差距。

## 问题
- 直接 VLA 策略可能学习从观测到动作的捷径映射，因为与视觉输入相比，动作标签较稀疏。
- 基于视频的世界-动作模型加入未来预测，但像素 rollout 会增加训练和推理计算量，也可能建模不影响控制的视觉细节。
- 对长时程和动态操作来说，这个问题会影响性能，因为接触、物体运动和任务进展会影响下一步动作。

## 方法
- 模型在多模态上下文和动作块之间插入 K=16 个可学习潜在 query，使 Transformer 在预测动作前构建紧凑的、面向动作的状态。
- 训练使用两个匹配分支：prior 分支看到当前指令、H=4 帧观测、状态和潜在 query；posterior 分支用来自未来观测的嵌入替换这些 query。
- 未来帧通过冻结的 ViT 和 Perceiver resampler 编码为 K 个嵌入，然后在最后 L=9 个 Transformer 层与 prior 潜在状态对齐。
- 两个分支都使用覆盖 T=20 个动作块的流匹配动作目标进行训练，并加入潜在对齐以及范数/秩正则项，以减少潜在表示坍缩。
- 推理时移除 posterior 分支，因此策略无需生成未来图像即可预测动作。

## 结果
- 摘录称该模型在 6 个仿真基准上达到当前最佳或相当的性能，但所给文本未包含表格数值、指标或成功率。
- 真实世界评估覆盖 3 个机器人平台和 12 个任务，任务涉及动态场景、物理推理、运动推理、长时程执行和泛化。
- 论文称 Being-H0.7 在全部 5 个按能力划分的真实世界套件中领先，示例包括接住快速滚动的球、向移动容器倒入物体、折叠衣物、传送带包裹分拣和钉钉子。
- 采用感知延迟的通用异步分块部署时，Being-H 系列报告的延迟为 3-4 ms/step，且测试时不生成未来帧。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00078v1](https://arxiv.org/abs/2605.00078v1)
