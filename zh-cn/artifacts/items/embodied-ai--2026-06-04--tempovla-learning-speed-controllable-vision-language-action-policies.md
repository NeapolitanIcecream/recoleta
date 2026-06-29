---
source: arxiv
url: https://arxiv.org/abs/2606.06491v1
published_at: '2026-06-04T17:59:40'
authors:
- Dong Jing
- Jingchen Nie
- Tianqi Zhang
- Jiaqi Liu
- Huaxiu Yao
- Zhiwu Lu
- Mingyu Ding
topics:
- vision-language-action
- robot-manipulation
- speed-control
- trajectory-augmentation
- generalist-robot-policy
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# TempoVLA: Learning Speed-Controllable Vision-Language-Action Policies

## Summary
## 总结
TempoVLA 训练一个 Vision-Language-Action 策略，让机器人操作任务按指定速度执行，而不是固定为示教数据的速度。它通过重定时示教数据，并把一个标量速度值输入策略来实现这一点。

## 问题
- 现有 VLA 从遥操作示教中继承一种执行速度，所以同一个策略无法在安全的空移阶段加速，也无法在接触密集的步骤减速。
- 这很重要，因为单个任务里的不同阶段需要不同速度：快速的自由空间运动能省时间，而慢速的插入、抓取和交接能降低失败风险。
- 之前的加速工作只改变推理速度，或者生成一个更快的固定策略，但这篇论文关注的是对机器人运动速度进行显式的双向控制。

## 方法
- Variable-Speed Trajectory Augmentation（VSTA）会在线重定时示教数据。加速时，它把连续动作合并成更少、更大的动作；减速时，它把动作拆分成更多、更小的动作。
- VSTA 按运动模式、方向变化和夹爪状态变化来切分轨迹，这样重采样就不会把旋转、平移或夹爪切换弄模糊。
- 目标速度写成比例 s = q/p。VSTA 将 q 个源帧映射成 p 个输出帧，同时保留每个分块上的累计运动量。
- TempoVLA 用三种轻量机制之一把速度条件加入 VLA：文本前缀、速度调制的 RMSNorm，或与速度锚点绑定的软提示 token。
- 部署时，VLM 调度器可以选择速度，在高风险接触阶段发送低速，在自由空间阶段发送较高速。

## 结果
- 在 LIBERO 上，VSTA 重放重定时示教的速度接近目标值：在 0.5x、0.75x、1.25x、1.5x 和 2x 时，数据比例分别为 0.50、0.76、1.20、1.43 和 1.90。
- VSTA 保留了积分运动，误差很小：在 0.5x、0.75x、1.25x、1.5x 和 2x 时分别为 2.8E-10、4.4E-9、1.1E-8、2.2E-8 和 4.8E-8。
- 在 LIBERO 上，重定时示教重放成功率在 1x 时为 97.6%，在 0.75x 时为 92.9%，在 1.25x 时为 92.4%，在 0.5x 时为 83.0%，在 1.5x 时为 81.6%，在 2x 时为 67.5%。
- 三种速度条件化方法在 LIBERO 上表现接近：Text 在 0.75x、1x、1.25x 和 1.5x 上的平均成功率为 96.8%，Modulation 也是 96.8%，Soft Prompt-8 为 96.5%。
- 变量速度训练在默认 1x 的 LIBERO 成功率上优于或持平于单速基线 96.7%；七速策略在 1x 时达到 96.9%，在 1.25x 时达到 97.4%，在 1.5x 时达到 97.3%。
- 该策略能双向控制速度，但对大幅加速的达成低于目标：在七速设置下，命令 2x 时模型速度比达到 1.58x，而 VSTA 数据达到 1.90x。摘要提到在五个 Franka 任务上做了真实世界评估，每个任务 50 条示教、每个速度 10 次 rollout，但没有给出真实世界成功率表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06491v1](https://arxiv.org/abs/2606.06491v1)
