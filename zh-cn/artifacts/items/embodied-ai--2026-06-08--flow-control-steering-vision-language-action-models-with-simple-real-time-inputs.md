---
source: arxiv
url: https://arxiv.org/abs/2606.10180v1
published_at: '2026-06-08T21:16:37'
authors:
- Jonathan C. Kao
- Jason Chan
- Andy Wang
topics:
- vision-language-action
- robot-policy-steering
- flow-matching
- shared-autonomy
- robot-data-scaling
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Flow Control: Steering Vision-Language-Action Models with Simple Real-Time Inputs

## Summary
## 摘要
Flow Control 通过把动作采样器的初始条件替换成简单的用户指令，比如键盘方向键，来控制一个冻结的 flow-matching VLA。论文称，这让用户可以实时引导 \(\pi_{0.5}\)-DROID，而模型仍会把粗糙的指令映射成符合其已学习动作分布的动作。

## 问题
- VLAs 可能在语言理解、新物体、新场景和分布外状态上失效，所以用户需要一种低延迟方式，在执行过程中纠正机器人的行为。
- 现有的控制方法使用 episode 中途的语言、草图、目标图像或额外训练的接口；这些信号可能过于粗糙、带宽过高，或者需要新数据和微调。
- 这个问题重要，因为一个很小的用户输入应该能帮助高自由度机器人安全、有效地行动，而不需要用户逐个关节遥操作。

## 方法
- 该方法面向带有 flow-matching 动作头的 VLA，重点是 \(\pi_{0.5}\)-DROID。它的动作 expert 会用 10 个 Euler 步长、\(\Delta t=0.1\) 的确定性 ODE 进行积分。
- 键盘指令对应六个笛卡尔方向之一：上、下、左、右、前、后。
- 系统把这个方向转换成末端执行器速度，用逆运动学计算关节速度，再对其归一化，并把结果写入 flow 模型前 \(\tau\) 个动作步的初始条件。
- 之后，flow head 会把用户提供的初始条件转换成一个动作块，动作分布来自 VLA 的已学习动作分布，并以相机、语言和机器人状态为条件。
- 论文的方法依赖 flow matching 的一个关键性质：确定性 ODE 会保留初始条件信息，而扩散采样会在每一步注入噪声。

## 结果
- 在 Two-Block 任务中，\(\pi_{0.5}\)-DROID 在含糊指令“put the block in the hole”下有 85% 的概率选对积木；当把 joint-1 的初始条件设为朝左块的方向时，\(\tau=6\) 或 \(\tau=8\) 时拿到左块的成功率接近 100%。
- 在同一个 Two-Block 设置里，积木宽 2 cm，离洞口 10 cm；论文报告称，即使在整个 episode 中持续施加 steering 输入，抓取和放置成功率仍接近 100%。
- VLA 的动作块有 16 个时间步，其中 8 个在环境中执行；每个动作是 8 维，覆盖 7 个 Franka Panda 关节角和夹爪宽度。
- 用户研究用了 16 名参与者。每人完成了 Marker-in-Bowl 的 10 次 Flow Control 试验、Cup-Stacking 的 10 次 Flow Control 试验，以及这两个任务各 10 次遥操作试验，另有最多 5 次练习试验。
- 摘要称 Flow Control 提高了用户引导下的任务成功率和完成速度，且在 Flow Control 轨迹上微调能提升自主策略表现，但这里没有给出这些结论对应的精确成功率或时间数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10180v1](https://arxiv.org/abs/2606.10180v1)
