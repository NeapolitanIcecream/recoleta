---
source: arxiv
url: http://arxiv.org/abs/2603.04639v1
published_at: '2026-03-04T21:59:32'
authors:
- Yinpei Dai
- Hongze Fu
- Jayjun Lee
- Yuejiang Liu
- Haoran Zhang
- Jianing Yang
- Chelsea Finn
- Nima Fazeli
- Joyce Chai
topics:
- robotic-manipulation
- memory-augmented-policy
- vision-language-action
- benchmarking
- long-horizon-control
relevance_score: 0.52
run_id: materialize-outputs
---

# RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies

## Summary
本文提出 RoboMME，一个面向机器人通用策略记忆能力的大规模标准化基准，并在统一的 \(\pi_{0.5}\) VLA 骨干上系统比较 14 种记忆增强变体。核心结论是：机器人记忆设计没有“一招通吃”，不同任务偏好不同记忆表示，但感知记忆配合调制式集成整体最均衡。

## Problem
- 机器人长时程操作常依赖历史信息，例如计数、遮挡下追踪、跨时间指代和模仿演示；仅靠当前观测往往无法决定正确动作。
- 现有记忆型机器人方法使用不同骨干、不同任务和不同评测协议，导致难以公平比较，也难以知道哪类记忆机制真正有效。
- 现有基准要么任务太少、接近被解完，要么时程短、示范不足，无法系统覆盖时间、空间、对象和程序性记忆需求。

## Approach
- 构建 RoboMME：16 个非马尔可夫、长时程操作任务，分为 4 个套件，分别测试 temporal、spatial、object、procedural memory；共 1,600 条示范、770k 训练时间步，平均每任务约 481 步。
- 任务覆盖计数、遮挡与交换下位置追踪、短暂高亮/视频/语言指代下对象识别，以及复现演示轨迹和操作方式等真实记忆需求。
- 在统一 \(\pi_{0.5}\) 骨干上构建 14 个记忆增强 VLA：三类记忆表示包括 symbolic（语言子目标）、perceptual（历史视觉 token）、recurrent（TTT/RMT 压缩状态）。
- 进一步比较三种集成方式：memory-as-context（把记忆拼到输入里）、memory-as-modulator（用记忆调制动作专家）、memory-as-expert（增加专门记忆专家）。
- 为公平评测，作者固定 memory budget 为 512 tokens，在 16 个任务上做多任务训练，并与 \(\pi_{0.5}\)、past-actions、SAM2Act+、MemER 等基线比较。

## Results
- 基准规模上，RoboMME 覆盖 **4 类记忆**、**16 个任务**、**1,600 demonstrations**、**770k timesteps**；对比 MemoryBench 的 **3 个任务/300 demos**，以及 MIKASA-robo(VLA) 的 **12 个任务/1,250 demos**，其覆盖面和训练规模更完整。
- 任务时长显著更长：RoboMME 平均 **481 steps/episode**；单任务平均步数从 **208**（PatternLock）到 **1,134**（VideoPlaceOrder），强调真实长时程历史依赖。
- 作者评测了 **14 个**自建 MME-VLA 变体和 **4 个**已有方法；在统一设置下发现**没有任何单一记忆表示或集成策略能在全部任务上持续最优**，说明以往从单一任务得出的结论不具普适性。
- 定性结论上，**symbolic memory** 更擅长 counting 和短时程推理；**perceptual memory** 对时间敏感和运动中心任务更关键；综合性能与计算效率的最佳折中是 **perceptual memory + memory-as-modulator**。
- 文本摘录未完整给出主结果表中的各方法**平均成功率/逐任务数值**，因此无法可靠列出完整定量 SOTA 指标；能明确提取的最强定量信息主要是基准规模、任务步长和比较设置。

## Link
- [http://arxiv.org/abs/2603.04639v1](http://arxiv.org/abs/2603.04639v1)
