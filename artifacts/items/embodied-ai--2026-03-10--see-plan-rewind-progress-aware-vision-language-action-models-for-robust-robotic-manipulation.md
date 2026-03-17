---
source: arxiv
url: http://arxiv.org/abs/2603.09292v1
published_at: '2026-03-10T07:22:51'
authors:
- Tingjun Dai
- Mingfei Han
- Tingwen Du
- Zhiheng Liu
- Zhihui Li
- Salman Khan
- Jun Yu
- Xiaojun Chang
topics:
- vision-language-action
- robot-manipulation
- progress-monitoring
- failure-recovery
- ood-robustness
relevance_score: 0.95
run_id: materialize-outputs
---

# See, Plan, Rewind: Progress-Aware Vision-Language-Action Models for Robust Robotic Manipulation

## Summary
SPR 是一种面向机器人操作的进度感知视觉-语言-动作框架，把语言任务分解为可验证的2D空间子目标，并在进度异常时触发“回退”恢复。它旨在在不增加失败数据或辅助模型的前提下，提高操作成功率、OOD鲁棒性和真实机器人恢复能力。

## Problem
- 现有 VLA 机器人策略通常能“看和做”，但缺少对**任务进度**的显式、可执行表征，导致长时序操作中错误累积、卡住后难以恢复。
- 许多进度监控方法只给出抽象文本推理或二值信号，缺乏对机器人动作直接有用的**空间落地**中间目标。
- 现有失败恢复方案常依赖额外失败数据、人工规则或辅助模型，代价高且在未见场景中适应性有限。

## Approach
- SPR 将任务执行组织为闭环 **See-Plan-Rewind**：先预测当前剩余子任务及其2D坐标，再规划到下一个子目标的2D轨迹，最后在检测到异常时执行回退。
- 它把示范数据自动分解为一串**空间子目标**：抓取类任务用夹爪开合变化找子任务边界；其他任务用 Gemini-3 标注片段与语义描述。
- 为了获得子目标与轨迹监督，方法用 **DINOv3 + SAM** 自动定位夹爪，从示范中提取离散化的2D waypoint 和 1–5 个中间轨迹点。
- 模型自回归生成：深度 token、剩余子任务数、每个子任务的语义+2D坐标、到下一个子目标的2D轨迹、以及最终动作 token。
- 回退机制不需要额外恢复数据：作者把成功示范反向构造成“return to initial position”数据，并用状态记录器监控最近 4 步子任务计数与 8 步轨迹；若计数持续上升或轨迹长期不变，则触发固定时长回退（实证设为 **N=3**）。

## Results
- 在 **LIBERO** 上，SPR 平均成功率达到 **90.6%**，相比 **MolmoAct 86.8%** 提升 **3.8 个百分点**；分项上为 Spatial **92.4%**, Object **93.0%**, Goal **94.2%**, Long **82.8%**。
- 在联合训练的 one-policy-for-all 设置下，SPR（Ours*）达到 **91.8%**，相比单独训练版 **90.6%** 再提升 **1.2 个百分点**；其中 Long 达到 **85.4%**。
- 在 **LIBERO-Plus** OOD 基准上，SPR 取得 **71.8%** 平均成功率，且平均性能下降仅 **18.8%**，优于 **OpenVLA-OFT 70.6% / ↓27.0%** 和 **UniVLA 57.7% / ↓37.5%**，文中据此声称达到新的 SOTA 鲁棒性。
- 按扰动类型，SPR 在 LIBERO-Plus 上分别达到：Background **86.0% (↓4.6%)**、Robot **47.7% (↓42.9%)**、Language **78.5% (↓12.1%)**、Layout **69.6% (↓21.0%)**、Light **85.0% (↓5.6%)**。
- 在真实机器人 3 个任务上，SPR 相比 MolmoAct 从 **50%→70%**（Pick up）、**0%→30%**（Tidy up）、**0%→40%**（Push-T），说明其恢复机制对长时序和连续接触任务更有效。
- 论文还声称该方法实现了**无需额外训练数据或辅助模型**的闭环纠错与更强泛化，但摘录中未给出更细的消融数值。

## Link
- [http://arxiv.org/abs/2603.09292v1](http://arxiv.org/abs/2603.09292v1)
