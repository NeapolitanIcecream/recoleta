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
RePO-VLA 使用带有不同标签的成功、失败和恢复 rollout，训练 VLA 机器人策略在接触密集操作发生漂移后恢复。论文报告称，平均对抗成功率从 20% 提高到 75%，在扩展的真实世界试验中最高达到 80%。

## 问题
- 长时程双臂任务可能因轻微的抓取、接触或时序错误而失败，即使机器人仍有恢复机会。
- 只用成功样本做模仿学习，对漂移提供的监督很弱，并且常常丢弃包含有用早期行为的失败 rollout。
- 直接模仿恢复片段可能把导致漂移的动作和修复漂移的动作混在一起。

## 方法
- Recovery-Aware Initialization 从完整 episode 中切出恢复片段，并重置观测历史，使策略从当前不利状态学习纠正动作。
- Progress-Aware Semantic Value Function 使用冻结的 V-JEPA 轨迹特征、语言嵌入和成功参考轨迹来分配稠密进度标签。
- 失败轨迹通过可靠性衰减标签保留有用前缀，其中 alpha = 3.0；终端漂移被赋予低价值。
- Value-Conditioned Refinement 使用成功、原始恢复和失败数据一起训练带价值 token 的 flow-matching pi_0.5 策略。
- 部署时，策略使用正常的滚动历史和固定价值条件 v = 1.0，不需要在线失败检测器或手写重试规则。

## 结果
- 论文称平均对抗成功率从 20% 提高到 75%，在扩展的真实世界试验中成功率最高达到 80%。
- FRBench-Sim 包含 46 个任务上的 23,453 个模拟双臂 episode：17,061 个标称成功 episode 和 6,392 个经验证的失败-恢复 episode。
- FRBench 使用 4 类注入错误：过早闭合、抓取滑移、抓取位置偏移和抓取朝向不匹配。
- 最终过滤前，错误注入覆盖包括 8,022 个过早闭合案例、3,516 个抓取滑移案例、4,686 个位置偏移案例和 688 个朝向不匹配案例。
- 仿真协议对每个任务运行 50 个 rollout，并通过让夹爪保持打开 30 帧来注入抓取扰动，约 1 秒。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09410v1](https://arxiv.org/abs/2605.09410v1)
