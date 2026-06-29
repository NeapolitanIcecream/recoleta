---
source: arxiv
url: https://arxiv.org/abs/2606.12105v1
published_at: '2026-06-10T13:59:07'
authors:
- Pankhuri Vanjani
- Zhuoyue Li
- Jakub Suliga
- Moritz Reuss
- Gianluca Geraci
- Xinkai Jiang
- Rudolf Lioutikov
topics:
- vision-language-action
- robot-foundation-model
- asynchronous-control
- multimodal-sensing
- force-torque
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model

## Summary
## 摘要
DAM-VLA 认为，当视觉、语言、力觉和本体感觉按各自速率更新时，VLA 策略表现更好。它在 7 个真实机器人操作任务上报告了 95.2% 的平均成功率，同时保持平滑的 100 Hz 控制。

## 问题
- 标准 VLA 模型用同一个时钟处理所有输入，这会把算力浪费在语言和视觉这类慢信号上，也会错过力和扭矩这类快接触信号。
- 这对接触丰富的操作任务很重要，因为力峰值可能出现在 100 到 500 Hz，而 RGB 帧中的有效变化更接近 3 到 10 Hz。
- 同步动作生成要等一整包观测输入，带来延迟，并限制反应式控制。

## 方法
- DAM-VLA 为每个模态保留一个潜在缓冲区。语言只编码一次，视觉稀疏更新，力觉和本体感觉按控制频率更新。
- 动作头在每个控制步读取所有缓冲区，因此即使慢模态没有新输入，动作输出也能继续。
- 视觉使用短期记忆缓冲区：25 Hz 下的 16 帧视觉帧，约 0.64 秒的上下文。
- 力觉和本体感觉使用密集历史：100 Hz 下的 96 个样本，约 0.96 秒的接触和状态上下文。
- 新的模态信息通过门控交叉注意力模块进入 X-VLA 动作专家，这些模块保持预训练的自注意力权重不变。

## 结果
- 在 7 个真实 Franka 操作任务上，每个任务 15 次试验，DAM-VLA 的平均成功率达到 95.2%，而最强同步基线 X-VLA_25 为 40.95%。这相当于提升了 54.25 个百分点，成功率约为 2.32 倍。
- 朴素的高频同步 X-VLA_100 的平均成功率降到 21.9%，低于 X-VLA_25 的 40.95%，说明在这个设置里把视觉帧上采样到 100 Hz 会损害表现。
- DAM-VLA 在 X-VLA_25 失败或接近失败的任务上也能成功：Handwash 100.0% 对 0.0%，Lego 93.3% 对 0.0%，Socket 80.0% 对 6.7%，Button 93.3% 对 13.3%。
- 最强的拼接基线 X-VLA_AFM 使用了力觉和记忆，但平均成功率只有 54.3%，远低于 DAM-VLA 的 95.2%。
- 消融结果显示了累加收益：仅异步 40.0%，异步加视觉记忆 58.1%，异步加力觉 66.7%，完整 DAM-VLA 95.2%。
- 报告中的控制器运行在 100 Hz。重规划频率大约为：X-VLA_25 为 1 Hz，X-VLA_100 为 3.5 Hz，s=22 的 DAM-VLA 为 5.5 Hz；200 Hz 控制器测试报告显示，根据 s 的不同，重规划频率约为 8 到 17 Hz。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12105v1](https://arxiv.org/abs/2606.12105v1)
