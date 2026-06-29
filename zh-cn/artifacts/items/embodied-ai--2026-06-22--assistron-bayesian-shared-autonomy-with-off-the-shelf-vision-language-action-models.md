---
source: arxiv
url: https://arxiv.org/abs/2606.23147v1
published_at: '2026-06-22T10:47:12'
authors:
- Pinhao Song
- Ze Fu
- Yutong Hu
- Renaud Detry
topics:
- vision-language-action
- shared-autonomy
- assistive-robotics
- flow-matching
- human-in-the-loop
- manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Assistron: Bayesian Shared Autonomy with Off-the-shelf Vision-Language-Action Models

## Summary
## 摘要
Assistron 是一个共享自主系统，它冻结 VLA 策略，并在接触密集步骤附近请求用户用摇杆协助。在长时程辅助操作基准中，它提高了任务成功率；与直接遥操作相比，它减少了用户主动控制时间。

## 问题
- 辅助机器人需要处理多种家庭任务，但面向特定任务的控制器只覆盖抓取、插入、倒水等狭窄技能。
- 冻结的 VLA 可以理解语言并处理宏观到达动作，但在抓取、插入和释放时常因空间精度和接触精度错误而失败。摘录引用的 RoboArena 成功率为 pi_0.5 的 46.95% 和 pi_0 的 35.25%。
- 重新训练或微调 VLA 可能需要大量机器人数据集，并可能使策略变窄，因此论文的目标是在不改变 VLA 权重的情况下实现辅助控制。

## 方法
- Assistron 使用 pi_0.5 作为冻结的流匹配 VLA。Whisper 将用户语音转写为给 VLA 的自然语言提示。
- 系统通过二值干预信号在自主 VLA 控制和共享控制之间切换。
- ResNet-18 检测器读取 224x224 的腕部相机图像并预测交互置信度。只有当置信度超过阈值且 VLA 预测夹爪状态变化时，它才触发干预；用户也可以通过摇杆输入触发干预。
- 在干预期间，摇杆命令被视为高斯测量。系统在 VLA 的流匹配去噪过程中加入引导项，使采样动作跟随用户命令，同时保持接近 VLA 动作分布。
- 用户处理抓取或释放等精细接触步骤，随后控制权返回给 VLA 执行宏观运动。

## 结果
- 在包含 17 名新手用户、5 个子任务和 7 分钟超时限制的场景恢复基准中，Assistron 达到 91.3% 的部分成功率。Direct joystick 达到 96.3%，自主 VLA 达到 13.7% 且一直超时。
- Assistron 的完成时间为 324.5 秒，Direct joystick 为 305.9 秒。Assistron 需要用户主动输入的时间占运行时长的 56.5%，其中 41.7% 为摇杆、14.8% 为语音，并有 43.5% 的时间自主运行。
- 用户评分显示，在 Quick、Easy to Use、Low Workload 和 Reuse 上，Assistron 优于 Direct joystick（p<0.05）；Direct joystick 在 Wanted 和 Trust 上得分更高（p<0.05）。Assistron 的 NASA-TLX 心理负荷和体力负荷低于 Direct joystick（p<0.001）。
- 摇杆熟练度较低的用户获益更大：完成时间改进与基线 Direct joystick 表现相关，r=0.762，p=0.001。挫败感降低也与较弱的基线表现相关，r=-0.564，p=0.023。
- 在葡萄放入抽屉的消融实验中，后验混合相对 Direct teleoperation 缩短了完成时间（p<0.05），并相对 Direct 和 Linear blending 缩短了轨迹长度（p<0.05）。摘录未给出具体时间或长度数值。
- 交互检测器使用超过 12,000 帧腕部相机图像训练，测试准确率达到 81.2%，平均精度达到 84.5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23147v1](https://arxiv.org/abs/2606.23147v1)
