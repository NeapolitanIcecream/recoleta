---
source: arxiv
url: https://arxiv.org/abs/2605.17517v1
published_at: '2026-05-17T16:02:05'
authors:
- Weijie Kong
- Zhian Su
- Wei Yu
- Huixu Dong
topics:
- vision-language-action
- robot-foundation-model
- affordance-learning
- generalist-robot-policy
- robot-manipulation
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment

## Summary
## 摘要
AffordVLA 通过将内部视觉特征与冻结教师模型的可供性特征对齐，训练 VLA 策略关注与任务相关的接触区域。教师模型只在训练时使用，因此推理保持同一条策略路径，论文未说明会增加运行时成本。

## 问题
- VLA 策略常能识别正确物体，却在错误部位执行动作，例如抓平底锅锅身而不是锅柄。
- 现有可供性方法常在推理时向策略输入掩码、热图或检测器输出，这需要额外的可供性标签，会增加延迟，并且可能在检测器失败时失效。
- 这个问题很重要，因为杂乱场景、干扰物和复杂纹理会让策略关注全局外观而非功能性交互区域，从而降低操作成功率。

## 方法
- 零样本可供性教师模型接收 RGB 图像和语言指令，使用 Qwen3-VL 将任务转换为部件级可供性提示，再使用基于 SAM3 的开放词汇感知模块生成任务条件化的可供性特征。
- VLA 骨干基于 π0.5，使用 Gemma-2B 语言骨干和 SigLIP-So400m 视觉编码器；动作 Transformer 通过条件流匹配预测连续动作块。
- 训练期间，AffordVLA 在调整尺寸、归一化和两层 MLP 投影之后，使用余弦相似度将 VLA 的中间视觉 token 与教师模型的可供性特征 token 对齐。
- 对齐应用在 18 层理解模型的第 12 层，教师特征维度为 256，VLA 视觉特征维度为 2048。
- 最终损失结合动作预测损失和可供性对齐损失，λ = 0.5；冻结的教师模型在推理时移除。

## 结果
- 在 RoboTwin 上，论文声称达到最先进性能，在 Easy 设置中比此前最佳基线高 20.5%，在 Hard 设置中高 12.8%。
- 可供性教师模型约有 0.8B 参数，处理 1008 × 1008 图像；它只在训练期间使用。
- 理解专家约有 3.0B 参数、18 层；动作专家约有 0.3B 参数、18 个 Transformer 层。
- 推理使用 10 个流匹配去噪步骤，动作块时域为 H = 30。
- 摘录称该方法提升了非结构化环境中的真实世界操作效果，提高了数据效率，并且不增加推理开销，但所提供文本没有给出真实世界成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17517v1](https://arxiv.org/abs/2605.17517v1)
