---
source: arxiv
url: https://arxiv.org/abs/2605.09410v1
published_at: '2026-05-10T08:24:05'
authors:
- Weijia Liufu
- Xiaoyu Guo
- Ruiyi Chen
- Jingzhi Liu
- Kaidong Zhang
- Xiwen Liang
- Jianqi Lin
- Dawei Sun
- Yuze Wang
- Rongtao Xu
- Bingqian Lin
- Bowen Yang
- Tongtong Cao
- Bowen Peng
- Dongyu Zhang
- Guangrun Wang
- Min Wang
- Liang Lin
- Xiaodan Liang
topics:
- vision-language-action
- robot-recovery
- bimanual-manipulation
- robot-data-scaling
- generalist-robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models

## Summary
## 摘要
RePO-VLA 通过使用带不同标签的成功、失败和恢复轨迹，让 VLA 机器人策略在接触丰富的操作出现漂移后学会恢复。论文报告，对抗成功率平均从 20% 提升到 75%，在扩展的真实世界试验中最高达到 80%。

## 问题
- 长时程双臂任务在抓取、接触或时序上的微小错误后就会失败，即使机器人本来仍有机会恢复。
- 只用成功示范做模仿，对漂移的监督很弱，而且常常会丢掉那些包含有用早期行为的失败轨迹。
- 直接模仿恢复过程会把导致漂移的动作和修复漂移的动作混在一起。

## 方法
- Recovery-Aware Initialization 会从完整回合中切出恢复片段，并重置观测历史，让策略从当前的不利状态学习纠正动作。
- Progress-Aware Semantic Value Function 使用冻结的 V-JEPA 轨迹特征、语言嵌入和成功参考轨迹来分配稠密的进度标签。
- 失败轨迹通过可靠性衰减标签保留有用前缀，alpha = 3.0，而末端漂移得到低价值标签。
- Value-Conditioned Refinement 用 value token 训练一个 flow-matching pi_0.5 策略，把成功、原始恢复和失败数据一起使用。
- 部署时，策略使用正常的滚动历史和固定的价值条件 v = 1.0，不需要在线失败检测器或手写重试规则。

## 结果
- 论文声称，对抗成功率平均从 20% 提升到 75%，在扩展的真实世界试验中最高达到 80%。
- FRBench-Sim 包含 46 个任务中的 23,453 段模拟双臂回合：17,061 段正常成功回合和 6,392 段已验证的失败-恢复回合。
- FRBench 使用 4 种注入错误类型：过早闭合、抓取滑移、抓取位置偏移和抓取朝向不匹配。
- 在最终过滤前，错误注入覆盖了 8,022 个过早闭合案例、3,516 个抓取滑移案例、4,686 个位置偏移案例和 688 个朝向不匹配案例。
- 仿真协议对每个任务运行 50 次 rollout，并通过将夹爪保持打开 30 帧，约 1 秒，来注入抓取扰动。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09410v1](https://arxiv.org/abs/2605.09410v1)
