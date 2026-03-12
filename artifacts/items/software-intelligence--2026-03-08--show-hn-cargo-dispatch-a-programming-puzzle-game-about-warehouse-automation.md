---
source: hn
url: https://matthuggins.com/lab/cargo-dispatch
published_at: '2026-03-08T23:28:50'
authors:
- matthuggins
topics:
- programming-game
- warehouse-automation
- robot-scheduling
- typescript
- javascript
relevance_score: 0.39
run_id: materialize-outputs
---

# Show HN: Cargo Dispatch – a programming puzzle game about warehouse automation

## Summary
这是一款以仓库自动化为主题的编程解谜游戏，玩家用 TypeScript 或 JavaScript 控制机器人搬运包裹并按时送达卡车。它更像交互式编程练习与调度仿真，而不是传统研究论文。

## Problem
- 解决的问题是：如何通过编程控制一组仓库机器人，在限时条件下完成包裹拾取、路径移动与正确分拣。
- 这一问题重要，因为它把多机器人调度、任务分配和自动化物流等真实工程概念，转化为可操作的编程学习体验。
- 从研究相关性看，它涉及代码驱动自动化与简单代理控制，但未展示更广义的软件工程智能体能力。

## Approach
- 玩家直接编写 **TypeScript/JavaScript** 代码，作为控制逻辑来指挥仓库机器人行为。
- 游戏环境会生成包裹、设置多个 aisle 与 truck，并要求机器人在倒计时结束前完成取货与投递。
- 核心机制可以简单理解为：**用代码写一个调度器/控制器**，让机器人在地图中移动、拿起包裹、再送到正确卡车。
- 该系统通过关卡与时间压力，把路径规划、资源协调和事件响应封装成一个可玩的编程谜题。

## Results
- 提供的内容**没有给出正式量化实验结果**，没有论文式 benchmark、数据集或与基线方法的对比数字。
- 可见的界面信息显示存在关卡/进度与计时元素，例如 **Speed: 1 / 2 / 3**、计时约 **36s**、以及 **0 of 20** 之类的目标计数，但其具体评价含义未在摘录中说明。
- 最强的具体主张是：玩家能够用 **TypeScript 或 JavaScript** 控制一支仓库机器人队伍，处理生成于 aisle 的包裹并投递到正确 truck。
- 另一具体主张是：游戏聚焦“warehouse automation”主题，并以“survive the workweek”的形式提供限时挑战。

## Link
- [https://matthuggins.com/lab/cargo-dispatch](https://matthuggins.com/lab/cargo-dispatch)
