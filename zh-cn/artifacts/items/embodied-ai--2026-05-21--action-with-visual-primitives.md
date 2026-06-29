---
source: arxiv
url: https://arxiv.org/abs/2605.22183v1
published_at: '2026-05-21T08:52:47'
authors:
- Weilong Guo
- Yuchen Wang
- Renping Zhou
- Yunfeng Zhang
- Rui Fang
- Yue Meng
- Wenda Xu
- Yuan He
- Gao Huang
topics:
- vision-language-action
- robot-manipulation
- visual-primitives
- generalist-robot-policy
- spatial-grounding
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Action with Visual Primitives

## Summary
## 摘要
AVP 是一种 VLA 架构，它先让 VLM 输出视觉目标 token，再进行动作预测。在需要精确空间定位的抓取和放置任务上，它在真实机器人实验中相对 π₀.₅ 取得了很大的提升。

## 问题
- 现有 VLA 策略常常把图像和语言直接映射到机器人动作，所以动作头必须同时学习指令解析、空间定位和运动控制。
- 这会带来实际影响，因为当物体布局、目标位置或物体外观变化时，机器人策略容易失效，尤其是在像中国象棋棋盘这样密集的场景里。
- 以前的视觉提示方法依赖外部检测器或 VLM API，这会增加延迟，也可能把定位误差传给机器人策略。

## 方法
- AVP 把任务拆开：VLM 先判断什么目标重要以及目标在哪里，然后动作专家再预测机器人该怎么移动。
- VLM 以自回归方式预测下一执行阶段的视觉原语，例如点、框、掩码或记忆原语。
- 这些原语会投影到视觉 token 空间，并与观测 token 融合，然后由 flow-matching 动作专家预测未来的机器人动作。
- 原语标签来自通过相机标定得到的末端执行器运动学，因此这种方法不需要逐样本人工提示标签。
- 推理时，AVP 只使用观测、指令和机器人状态；它不会调用外部检测器、分割器或在线 VLM API。

## 结果
- 在中国象棋操作任务上，AVP 的平均成功率达到 90.28%，而 π₀.₅ 为 62.67%，提升了 27.61 个百分点。指标分解如下：指令遵循 98.61% 对 74.00%，抓取 90.28% 对 72.00%，放置 81.94% 对 42.00%。
- 在同一个中国象棋任务上，AVP 的运行时间为每条指令 0.27 秒。使用 Kimi 的 Point-VLA 在 20 条指令子集上的平均成功率为 48.15%，延迟为 37.32 秒。
- 在多米诺骨牌摆放任务上，AVP 的平均成功率达到 88.19%，而 π₀.₅ 为 81.94%。抓取从 87.50% 提升到 100.00%，朝向从 93.75% 提升到 100.00%，放置保持在 64.58%。
- 在通用物体抓取和放置任务上，AVP 的平均成功率达到 86.18%，而 π₀.₅ 为 64.96%。抓取从 71.79% 提升到 90.24%，放置从 23.08% 提升到 68.29%。
- 在未见过的直接中国象棋转移任务上，AVP 报告平均成功率为 83%，其中指令遵循 100%，抓取 90%，放置 60%；而 π₀.₅ 在四项指标上都为 0%。
- 在视觉原语消融实验中，平均成功率从没有原语时的 78% 上升到使用框时的 83%、框加掩码时的 85%，以及框加掩码加记忆时的 91%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22183v1](https://arxiv.org/abs/2605.22183v1)
