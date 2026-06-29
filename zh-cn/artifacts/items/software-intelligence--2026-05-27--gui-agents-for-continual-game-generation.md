---
source: arxiv
url: https://arxiv.org/abs/2605.28258v1
published_at: '2026-05-27T10:08:48'
authors:
- Yixu Huang
- Bo Li
- Na Li
- Zhe Wang
- Kaijie Chen
- Haonan Ge
- Qingyi Si
- Yuanzhe Shen
- Ruihan Yang
- Guangjing Wang
- Hongcheng Guo
topics:
- gui-agents
- code-generation
- game-generation
- software-agents
- playtesting
- multi-agent-systems
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# GUI Agents for Continual Game Generation

## Summary
## 总结
Play2Code 使用一个 GUI agent 来玩生成的浏览器游戏，并把具体的游玩失败反馈给负责生成代码的 agent。在 PlaytestArena 上，它把 3 个模型骨干的平均量表通过率提高到 66.8%。

## 问题
- 一次性游戏代码生成可能产出能编译、能运行的产物，但在实际游玩时会因为控制无响应、状态变化缺失或胜利条件损坏而失败。
- 代码层面的检查会漏掉视觉和交互故障，所以生成的游戏需要通过真实游玩来评估。
- 人工测试速度太慢，跟不上模型快速生成的构建结果，因此自动化测试对游戏生成工作流很有用。

## 方法
- PlaytestArena 包含 200 个独立的 HTML/CSS/JS 浏览器游戏任务，覆盖 8 个类型，并配有 1,548 条人工编写的量表标准。
- GUI agent 在浏览器中加载每个生成的游戏，通过点击和按键进行游玩，并根据观察到的游戏过程判断每一条量表项。
- Play2Code 在 Game Agent 和 GUI Agent 之间运行一个循环：Game Agent 编写或修补游戏，GUI Agent 游玩，然后返回游玩摘要和修复列表。
- 系统把经验存入当前任务的 episode memory、每个 agent 的 skill memory，以及用于共享游戏规则和设计模式的 world memory。

## 结果
- 在一个 20 个游戏、约 120 个关卡的测试中，GUI agent 通过了大多数关卡：GPT-5.4 的 pass@20 达到 0.82，Claude Sonnet 4.6 达到 0.79，Kimi K2.5 达到 0.72，人工参考值达到 0.92。
- 在一个 32 个游戏的样本上，GUI 评估器与不看答案的人工标注者在 84.2% 的单项判断上一致，Cohen’s κ=0.64，而人工-人工 κ=0.66。
- 在同一个 32 个游戏样本上，GUI 生成的分数和人工生成的分数在游戏层面非常接近：Spearman’s ρ=0.87，Pearson’s r=0.88。
- Play2Code 在 3 个骨干上实现了 66.8% 的平均量表通过率，较 Direct LLM 提高 37.1 个百分点，较 OpenGame 提高 14.6 个百分点。
- 按骨干划分，Play2Code 的平均量表通过率分别为：GPT-5.4 72.3%，Claude Sonnet 4.6 71.1%，Kimi K2.5 56.9%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28258v1](https://arxiv.org/abs/2605.28258v1)
