---
source: hn
url: https://keanw.com/2026/03/a-diary-of-an-agentic-retro-gamer-part-1.html
published_at: '2026-06-05T23:43:13'
authors:
- throwaway_2494
topics:
- coding-agents
- test-oracles
- emulation
- code-intelligence
- human-ai-collaboration
- automated-software-production
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Using an AI coding agent with oracle-based testing to build a game emulator

## Summary
## 摘要
一个受引导的 AI 编码代理在配合一个基于 jzintv 的测试预言机后，用 36 小时做出了一个可工作的 Intellivision 模拟器。这个案例对代码智能很重要，因为它展示了参考测试如何约束代理在硬件精度要求很高的编程任务中的输出。

## 问题
- 现有的 Intellivision 模拟器在操作系统更新后失效，所以作者想做一个他能维护的新模拟器。
- 构建模拟器需要精确的 CPU、内存、时序、视频、声音和控制器行为，微小错误就可能让游戏无法启动或正常运行。
- 一个没有引导的编码代理生成了一个解析器，里面有两个重大缺陷，这说明代理需要人工指导和强测试。

## 方法
- 作者先手工写了大部分 CP-1610 CPU 核心。
- 他从 jzintv 提取了 CPU 实现，并把它当作测试预言机。
- 单元测试把每条新指令与 jzintv 在寄存器、标志位、RAM 和周期数上逐项对比。
- 在预言机就位后，作者引导编码代理完成了总线、视频、声音、ROM 加载、控制和运行时功能。
- 一个调试器端口让 AI 能查看模拟器状态，并在实时游玩时控制正在运行的游戏。

## 结果
- 在使用代理之前，作者一直做到 3 月中旬，已经有了一个大体可用的 CP-1610 CPU 核心，但还没有总线、视频或声音。
- 在受引导的代理加入后第 5 小时，模拟器显示出了第一批像素和颜色测试条。
- 到第 10 小时，渲染管线就位；到第 21 小时，第一张卡带 ROM 启动了。
- 到第 28 小时，作者收藏中的全部 204 个 ROM 都能启动。
- 到第 32 小时，游戏已经能在屏幕上移动；到第 36 小时，完整的 Intellivision 系统已经能运行，带有控制器输入和声音。
- 在接下来的几天里，作者又加入了调试器端口、由 AI 驱动的游戏控制、用于碰撞或死亡事件的代码位置支持，以及玩家死亡时控制器震动。

## Problem

## Approach

## Results

## Link
- [https://keanw.com/2026/03/a-diary-of-an-agentic-retro-gamer-part-1.html](https://keanw.com/2026/03/a-diary-of-an-agentic-retro-gamer-part-1.html)
