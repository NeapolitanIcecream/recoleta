---
source: arxiv
url: http://arxiv.org/abs/2604.15013v1
published_at: '2026-04-16T13:41:07'
authors:
- Joonho Koh
- Haechan Jung
- Nayoung Kim
- Wook Ko
- Changjoo Nam
topics:
- dexterous-manipulation
- teleoperation
- force-feedback
- robot-data-collection
- sim2real
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands

## Summary
## 摘要
DEX-Mouse 是一款低成本的手持接口，用于在真实硬件上采集灵巧机器人手的示范数据。它通过加入力反馈和一种贴附式、前臂安装的设置，力求让数据采集更便携、对不同操作者免校准，并且与目标机器人在物理上更一致。

## 问题
- 灵巧机器人学习需要大量真实示范数据，而且这些数据要符合机器人实际的运动学和接触动力学。
- 仿真和视频流程会因 sim-to-real 误差、遮挡，以及人到机器人的重定向不匹配而损失保真度。
- 现有遥操作设备，如 MoCap 手套和其他手持系统，往往需要按用户校准、定制硬件、固定实验室设置，或者对多个机器人手的支持不好。

## 方法
- 论文用现成部件搭建了一个便携式遥操作设备，成本低于 **USD 150**，不需要按操作者校准，也不需要为不同用户做结构修改。
- 该接口使用腱驱动手指、直接驱动拇指，以及基于电流的动觉力反馈，因此当机器人手因接触受阻时，用户会感到阻力。
- 它支持一种 **attached configuration**，把机器人手安装在操作者前臂上，也支持标准的空间分离遥操作模式。attached 模式用于采集与机器人坐标更对齐的数据，减少坐标不一致。
- 手部运动通过简单的比例重定向映射到机器人，而不是依赖复杂、与形态相关的重定向。固件以 **100 Hz** 运行；VIVE 追踪器提供全局位姿，机载摄像头以 **30 Hz** 记录对齐的 RGB 图像。

## 结果
- 在一项包含 **8 名参与者**、**3 种接口**和 **2 种采集配置**的用户研究中，DEX-Mouse 在 attached 设置下的总体成功率达到 **86.67%**，平均完成时间为 **10.05 s**。
- 在相同的 attached 设置下，DEX-Mouse 的总体平均成功率高于 DOGlove 和 Manus 手套：**86.67%** 对 **77.5%** 和 **62.5%**。它的 attached 完成时间也最快：**10.05 s** 对 **11.67 s** 和 **11.93 s**。
- DEX-Mouse attached 的任务分解结果为：抓取放置 **95.0%** 成功率 / **5.57 s**，插销入孔 **72.5%** / **14.29 s**，锤击 **92.5%** / **10.29 s**。
- DEX-Mouse 的遥操作模式弱于 attached 模式：总体成功率 **52.5%**，平均时间 **18.77 s**；而 attached 模式分别为 **86.67%** 和 **10.05 s**。
- 在所有接口中，attached 采集在总体平均成功率和速度上都优于远程遥操作：**75.56%** 和 **11.22 s**，对比 **46.39%** 和 **19.42 s**。
- 论文还称，attached 配置降低了参与者的主观工作负荷，但摘录中没有给出完整的工作负荷表或精确问卷数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15013v1](http://arxiv.org/abs/2604.15013v1)
