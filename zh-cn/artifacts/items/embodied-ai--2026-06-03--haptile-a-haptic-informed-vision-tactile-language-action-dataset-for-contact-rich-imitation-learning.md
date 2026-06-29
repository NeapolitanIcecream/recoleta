---
source: arxiv
url: https://arxiv.org/abs/2606.04825v1
published_at: '2026-06-03T12:48:17'
authors:
- Amirhosein Alian
- Yongqiang Zhao
- Shiyi Gu
- Xuyang Zhang
- Zhuo Chen
- Christopher E. Mower
- Haitham Bou-Ammar
- Shan Luo
topics:
- vision-language-action
- tactile-sensing
- haptic-teleoperation
- robot-manipulation-dataset
- imitation-learning
- contact-rich-manipulation
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning

## Summary
HapTile 是一个包含 1,726 次示范的机器人操作数据集，配对了语言、RGB 视频、指尖触觉图像、机器人状态、动作和操作者的触觉反馈。它面向接触丰富的任务，在这类任务中，只用视觉的策略会漏掉滑移、力和接触几何。

## 问题
- VLA 数据集常存储 RGB、语言和动作，但接触丰富的操作还需要触觉信号来感知滑移、受力和被遮挡的接触。
- 现有触觉数据集往往缺少任务多样性、作为策略输入的语言、动作轨迹，或者在遥操作过程中提供的触觉反馈。
- 这对擦拭、折叠、倒液、插销和转瓶这类日常机器人任务很重要，因为很小的接触误差就可能让任务失败。

## 方法
- 作者在一台配备 Robotiq 2F-85 夹爪的 UR5e 上收集了 1,726 次示范，覆盖 38 个任务、9 种技能和 9 名人工操作者。
- 每个 episode 都保存语言指令、第三视角 RGB、腕部 RGB、左右指尖触觉图像、机器人本体感知、7D 末端执行器增量动作、时间戳，以及 15 Hz 的触觉反馈状态。
- 指尖传感器用内部 RGB 摄像头观察硅胶层的形变。Lucas-Kanade 光流跟踪标记点位移，系统再把标记运动转换为接触-运动评分。
- 遥操作控制器根据触觉标记运动向操作者发送离散振动反馈，这样示范者在采集数据时就能感到接触。
- 基准测试用 Diffusion Policy 和 π0 训练了三种输入设置：仅视觉、视觉加原始触觉图像、视觉加触觉标记特征。

## 结果
- 数据集规模：1,726 次示范、38 个任务、9 种技能、750.33 分钟交互、15 Hz 采样。
- 任务时长示例：插销平均 54.21 秒，移动高尔夫球平均 12.42 秒。
- 在 π0 的插销任务上，成功率从仅视觉的 0% 提高到视觉加原始触觉图像的 90%，基于 10 次试验测得。
- 在 π0 的白板擦拭任务上，成功率从仅视觉的 50% 提高到视觉加触觉标记特征的 100%。
- 在 Diffusion Policy 的把瓶子转正任务上，最佳结果是视觉加触觉标记特征的 90%，高于仅视觉的 80%。
- 触觉输入并不总是有帮助：Diffusion Policy 在倒液任务上从仅视觉的 50% 降到触觉标记特征的 20%，π0 也从仅视觉的 30% 降到触觉标记特征的 0%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04825v1](https://arxiv.org/abs/2606.04825v1)
