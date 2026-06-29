---
source: arxiv
url: https://arxiv.org/abs/2606.13355v1
published_at: '2026-06-11T13:43:01'
authors:
- Sangkyu Lee
- Seohyeon Park
- Tackgeun You
- Avi Caciularu
- Idan Szpektor
- Hwasup Lim
- Youngjae Yu
topics:
- vision-language-action
- autoregressive-policy
- real-time-control
- constrained-decoding
- robot-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Real-Time Execution with Autoregressive Policies

## Summary
## 摘要
本文研究如何让自回归 Vision-Language-Action 策略在机器人上实时运行，并且不在动作块之间停顿。结果显示，只需调整分词方式并加入受限解码，就能把延迟控制在范围内，同时保持较强的任务表现。

## 问题
- 自回归机器人策略按顺序解码动作，所以在同步推理时会比扩散式策略停顿更久。
- 这种停顿会降低 rollout 速度，也会让机器人在部署时反应更慢。
- 以往关于实时执行的工作主要面向扩散策略，自回归策略研究较少。

## 方法
- 将动作时域设为不可修改前缀长度的两倍，然后在部署时只解码该块的后半部分。
- 将每个 m 步动作块单独分词，这样模型可以基于前一个动作块进行条件化，而不需要重新解码它。
- 使用受限解码来保证解码能在实时执行所需的延迟上限内完成，并且 token 序列可以反分词为有效的动作块。
- 基于部分 token 序列在剩余预算内是否还能组成有效动作块，使用动态规划在解码时屏蔽无效 token。
- 加入多轨迹解码，在多个选择都符合延迟上限时挑选最优的有效轨迹。

## 结果
- 在 LIBERO 上，\u0003c0_0-REALFAST 的平均任务成功率为 95.7%，高于 \u0003c0_0 + RTC 的 89.4% 和 \u0003c0_0.5 + RTC 的 94.7%。
- 在 LIBERO 上，\u0003c0_0-REALFAST 接近没有实时约束的 \u0003c0_0.5，后者报告的平均成功率为 96.9%。
- 论文还说，这种方法相比同步推理能提升 rollout 速度和任务完成速度，但摘要片段没有给出一个统一的整体速度数值，只给了延迟示例。
- 在延迟方面，对 LIBERO 解码 11 个 token 或对 DROID 解码 20 个 token，并结合多轨迹解码，会额外增加约 4、7、8 或 13 毫秒，具体取决于设置和 N。
- 论文还声称，同步推理中自回归策略的优势在实时执行下仍然成立，包括更快收敛和更好的指令跟随泛化，但摘要片段没有提供这些指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13355v1](https://arxiv.org/abs/2606.13355v1)
