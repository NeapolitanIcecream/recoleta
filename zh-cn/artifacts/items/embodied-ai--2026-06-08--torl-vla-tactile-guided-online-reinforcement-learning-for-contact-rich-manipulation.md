---
source: arxiv
url: https://arxiv.org/abs/2606.09337v1
published_at: '2026-06-08T11:05:05'
authors:
- Huaihang Zheng
- Yi Yang
- Kai Ma
- Shenglin Xu
- Tian Xie
- Guozheng Li
- Xiangyu Wang
- Yiren Ma
- Si Liu
- Yinian Mao
- Baoxu Liu
topics:
- vision-language-action
- tactile-feedback
- online-rl
- contact-rich-manipulation
- robot-policy
- human-intervention
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# TORL-VLA: Tactile Guided Online Reinforcement Learning for Contact-Rich Manipulation

## Summary
## 总结
TORL-VLA 在视觉-语言-动作机器人策略中加入了触觉引导的在线强化学习，让系统在执行过程中修正接触丰富操作中的错误。

## 问题
- 离线训练的 VLA 策略在接触条件偏离训练分布时会失效，即使 RGB 观察看起来已经接近成功也会这样。
- 紧配合的杯子放置、锁扣闭合和鸡蛋搬运这类接触丰富任务需要力和力矩反馈，才能避免不当接触力、反复重试或物体损坏。
- 在线学习中的人工干预会让价值估计产生偏差，因为失败的策略动作后面可能接上人工接管，再得到成功结果。

## 方法
- 机器人把两个 6x8 指尖触觉阵列映射成一个 12D wrench 信号，每个手指对应 6D 力-力矩。
- 一个感知 wrench 的 VLA 用注意力、MoE 路由和零初始化的触觉旁路，把最近的 wrench 历史与视觉-语言 token 融合。
- 参考模型同时预测动作块和未来的 wrench 序列，并用联合动作-wrench flow matching 损失进行训练。
- 一个轻量的、按阶段划分的 actor-critic 只在在线阶段细化可执行的动作块，条件包括 VLA token、本体感觉、当前 wrench、wrench 历史、预测 wrench 和 VLA 动作参考。
- 一个干预遮蔽 critic 会去掉人类纠正边界之间的 bootstrapping，并加入干预成本，这样后续因人工接管后的成功不会记到前面的策略动作上。

## 结果
- 在每个任务 30 次真实机器人试验中，TORL-VLA 在杯子任务上达到 30/30，在锁扣任务上达到 29/30，在鸡蛋任务上达到 30/30；对比 pi_0.5 分别是 18/30、15/30 和 20/30。
- 全任务成功率提升到 28/30；对比 pi_0.5 的 12/30、ForceVLA 的 15/30、去掉 RL 的 TORL-VLA 的 21/30，以及 RLT 的 23/30。
- 只统计成功运行时，全任务平均耗时 TORL-VLA 为 165.45 s；对比 RLT 的 175.23 s、去掉 RL 的 TORL-VLA 的 191.91 s、ForceVLA 的 195.34 s，以及 pi_0.5 的 199.65 s。
- 在参考模型消融中，去掉 MoE 的下降最大：杯子 18/30、锁扣 17/30、鸡蛋 19/30；完整但不含 RL 的参考模型分别是 25/30、23/30 和 25/30。
- 在在线自适应消融中，完整模型得到 30/30、29/30 和 30/30；去掉 wrench 上下文后是 27/30、27/30 和 26/30；去掉干预遮蔽 critic 后是 27/30、26/30 和 28/30。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09337v1](https://arxiv.org/abs/2606.09337v1)
