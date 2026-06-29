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
## 总结
AffordVLA 通过让 VLA 策略的内部视觉特征与冻结教师提供的 affordance 特征对齐，训练它关注与任务相关的接触区域。教师只在训练时使用，因此推理时保持同一路径，没有文中提到的运行时开销。

## 问题
- VLA 策略常常能认出正确的物体，却会对错误的部位采取动作，比如抓平底锅的锅身，而不是手柄。
- 现有的 affordance 方法常在推理时把掩码、热力图或检测器输出送入策略，这需要额外的 affordance 标注，会增加延迟；检测器失效时也会失败。
- 这个问题很重要，因为在杂乱环境、干扰物和复杂纹理下，如果策略关注的是整体外观，而不是功能性交互区域，操作成功率就会下降。

## 方法
- 一个 zero-shot affordance 教师接收 RGB 图像和语言指令，用 Qwen3-VL 把任务转换成部件级 affordance 提示，再用基于 SAM3 的开放词表感知模块生成任务条件化的 affordance 特征。
- VLA 骨干基于 π0.5，语言骨干是 Gemma-2B，视觉编码器是 SigLIP-So400m；动作 Transformer 用 conditional flow matching 预测连续动作块。
- 训练时，AffordVLA 在缩放、归一化和两层 MLP 投影之后，用余弦相似度对齐 VLA 的中间视觉 token 和教师的 affordance 特征 token。
- 对齐应用在一个 18 层理解模型的第 12 层，教师特征维度为 256，VLA 视觉特征维度为 2048。
- 最终损失把动作预测损失和 affordance 对齐损失结合起来，λ = 0.5；推理时移除冻结教师。

## 结果
- 在 RoboTwin 上，论文声称达到当前最优，分别比之前最好的基线在 Easy 设置上高 20.5%，在 Hard 设置上高 12.8%。
- affordance 教师大约有 0.8B 参数，处理 1008 × 1008 图像；它只在训练时使用。
- 理解专家大约有 3.0B 参数，包含 18 层；动作专家大约有 0.3B 参数，包含 18 层 Transformer。
- 推理使用 10 步 flow-matching 去噪，动作块时域为 H = 30。
- 摘录声称它在非结构化环境中的真实世界操作更好，数据效率更高，并且没有额外的推理开销，但提供的文本里没有真实世界成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17517v1](https://arxiv.org/abs/2605.17517v1)
