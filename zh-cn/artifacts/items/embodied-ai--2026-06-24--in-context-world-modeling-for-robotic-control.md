---
source: arxiv
url: https://arxiv.org/abs/2606.26025v1
published_at: '2026-06-24T16:53:36'
authors:
- Siyin Wang
- Junhao Shi
- Senyu Fei
- Zhaoyang Fu
- Li Ji
- Jingjing Gong
- Xipeng Qiu
topics:
- vision-language-action
- world-modeling
- test-time-adaptation
- system-identification
- robot-control
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# In-Context World Modeling for Robotic Control

## Summary
## 摘要
ICWM 让 VLA 机器人策略先执行几次安全的随机动作，并把观察到的视觉变化作为上下文，从而适应新的相机视角或机体配置。论文称，这种方法在未见过的视角下提升了 LIBERO 和真实机器人控制表现，并且测试时不更新权重，也不需要任务演示。

## 问题
- 标准 VLA 策略只基于当前图像和语言指令进行决策，因此相机视角、安装偏移和机器人几何结构会被写入训练数据，而不是在部署时被推断出来。
- 部署配置变化后，同一套图像到动作的映射可能出错，导致末端执行器偏移、夹爪过早闭合和任务失败。
- 这一点很重要，因为真实机器人在训练后常会遇到相机移动、标定漂移，以及工具或夹爪变化。

## 方法
- 机器人在执行任务前先运行一段短暂的主动探测阶段：采样安全目标位姿，移动到这些位姿，并记录起始图像、动作和结束图像片段。
- 这些与任务无关的交互片段会作为上下文加到 VLA 输入前面，使 Transformer 能推断当前动作到观测的映射。
- 训练使用相同格式：来自不同配置的上下文片段放在任务查询之前，模型用标准策略损失学习下一步动作预测。
- 主设置使用 Qwen2.5-VL-3B、FAST 动作分词、长度为 5 的动作块，以及 5 个上下文片段。
- 推理时，由于系统配置在一次运行中保持不变，可以缓存上下文隐藏状态。

## 结果
- 在 LIBERO 跨视角评估中，训练使用 8 个方位角，测试包含 6 个未见过的 OOD 视角，规模为 500 × 15 × 4 个 episode；ICWM 的平均 OOD 成功率比 Multi-View BC 高 13.0 个百分点，比显式输入相机角度的基线高 9.5 个百分点。
- 在 LIBERO 已见视角上，ICWM 的平均成功率比 Multi-View BC 高 8.1 个百分点。
- 在 LIBERO-Long 上，ICWM 报告的增益最大：相较 Multi-View BC，已见视角提高 29.9 个百分点，未见视角提高 26.3 个百分点。
- 真实机器人测试使用 UR5e、12 个相机视角（6 个训练视角和 6 个保留视角）、4 个任务，共 600 次试验；摘录显示它相较 Multi-View BC 有明确提升，但所给图中文字无法读出准确的平均成功率。
- 上下文消融支持该机制：移除图像会使平均成功率下降 56.4 个百分点，错误上下文得分为 18.9，而无上下文为 22.0；未经过上下文监督训练的 BC 模型在输入前置交互 token 后成功率低于 1%。
- 额外压力测试显示，在语义变化下增益较小：干扰物体场景得分为 35.0，MV 为 27.5；新桌面纹理场景得分为 41.2，MV 为 37.5；在 RTX 4090 上，使用 3 个上下文片段时每步延迟为 0.165 秒，使用 5 个片段时为 0.185 秒。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26025v1](https://arxiv.org/abs/2606.26025v1)
