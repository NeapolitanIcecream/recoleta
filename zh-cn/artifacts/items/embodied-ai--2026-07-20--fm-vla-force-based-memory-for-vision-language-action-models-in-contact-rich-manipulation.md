---
source: arxiv
url: https://arxiv.org/abs/2607.18231v1
published_at: '2026-07-20T17:58:31'
authors:
- Ruicheng Li
- Qixiu Li
- Ruichun Ma
- Yu Deng
- Lin Luo
- Zhiying Du
- Jianfeng Xiang
- Huizhi Liang
- Ruicheng Wang
- Jiaolong Yang
- Baining Guo
topics:
- robot-foundation-model
- vision-language-action
- force-sensing
- contact-rich-manipulation
- robot-memory
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# FM-VLA: Force-based Memory for Vision-Language-Action Models in Contact-Rich Manipulation

## Summary
## 总结
FM-VLA 为视觉-语言-动作策略加入紧凑的力历史记忆，用于处理进展难以通过视觉观察的接触丰富型任务。在三个双臂操作任务上，它的平均成功率达到 83.3%，相较基础策略仅增加 3.3 ms 的推理延迟。

## 问题
- 无记忆 VLA 无法可靠地统计重复接触次数、跟踪隐藏的交互进度，或在当前图像看起来没有变化时恢复回合历史。
- 视觉记忆方法需要额外的图像 token，并且可能遗漏按钮重复按压等视觉运动极小的事件。
- 论文使用 AgiBot G1 双臂机器人在三个任务上评估这一问题：寻找杯子下方的方块、按指定次数按压按钮，以及按指定次数擦拭盘子。

## 方法
- 力历史 VAE 通过与任务无关的时间序列重构预训练，将带噪声的 6 轴腕部力/力矩序列压缩为八个潜在记忆 token。
- 潜在力 token 与当前图像和语言指令一同作为流匹配动作专家的条件，使策略能够在整个回合中保留接触事件。
- 经过投影的一秒关节位置和夹爪状态窗口提供短期运动上下文，并减少接触前的重复行为。
- 指数移动平均平滑和随机噪声预填充可降低传感器噪声，并防止模型利用历史长度这一捷径。

## 结果
- FM-VLA 在杯子任务上的成功率为 100.0%，在按钮任务上为 72.2%，在擦拭任务上为 77.8%；每个任务进行 18 次试验，三个任务的平均成功率为 83.3%。
- 它优于无记忆 pi_0.5 基线（平均成功率 27.8%）、TA-VLA（22.2%）和视觉记忆 pi-MEM 基线（53.7%）。
- 在按钮按压任务上，FM-VLA 的成功率为 72.2%，而 pi-MEM 为 33.3%；在擦拭任务上，FM-VLA 为 77.8%，而 pi-MEM 为 50.0%，表明在接触事件视觉上难以区分时，力历史具有优势。
- 移除任一记忆流后，平均成功率分别降至 25.9%（仅使用力历史）和 40.7%（仅使用状态历史）；基于 VAE 的组合设计超过了 GRU 和 Q-Former 变体，后两者的成功率分别为 33.3% 和 57.4%。
- 在 RTX 4090 上，推理延迟为 64.0 ms，仅比基础策略的 60.7 ms 高 3.3 ms；使用五帧视觉记忆的 pi-MEM 延迟为 99.8 ms，高于 FM-VLA。
- 证据仅限于三个任务、一个双臂机器人以及每个任务 18 次评估试验；作者还指出，固定的八 token 瓶颈可能限制对包含数百个接触事件的更长历史进行建模。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18231v1](https://arxiv.org/abs/2607.18231v1)
