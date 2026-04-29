---
source: arxiv
url: http://arxiv.org/abs/2604.18394v1
published_at: '2026-04-20T15:17:03'
authors:
- Yilei Jiang
- Jinyuan Hu
- Qianyin Xiao
- Yaozhi Zheng
- Ruize Ma
- Kaituo Feng
- Jiaming Han
- Tianshuo Peng
- Kaixuan Fan
- Manyuan Zhang
- Xiangyu Yue
topics:
- agentic-coding
- game-generation
- code-intelligence
- software-engineering-agents
- benchmarking
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# OpenGame: Open Agentic Coding for Games

## Summary
## 摘要
OpenGame 是一个开源智能体系统，可将自然语言的游戏想法转成可玩的 2D 网页游戏。它结合了面向游戏的专用代码模型、可复用的项目模板和持续积累的调试协议，并用一个为交互式游戏生成设计的基准来评估输出结果。

## 问题
- 现有 LLM 和代码智能体在编写独立代码方面表现不错，但在构建一个逻辑一致、场景连接正确、资源完整、跨文件状态一致的可玩游戏时，经常失败。
- 游戏生成比标准代码生成更难，因为正确性取决于运行时行为、视觉交互和引擎特定的结构，而不只是代码能否编译。
- 这很重要，因为游戏开发是自动化软件生产中的高难度场景：如果智能体无法管理长链路、跨文件、交互式系统，那么在许多具有类似集成要求的真实软件任务中也会持续失败。

## 方法
- OpenGame 使用 **Game Skill**，其中包含两部分：**Template Skill** 和 **Debug Skill**。Template Skill 会扩展可复用的游戏骨架库，Debug Skill 会保存经过验证的失败特征、原因和修复方法，以便智能体复用过去的修复经验。
- 该智能体遵循六阶段工作流：分类游戏类型、搭建项目骨架、生成游戏设计文档、创建资源、结合模板扩展点实现代码，然后执行构建/测试/修复循环。
- 它的基础模型 **GameCoder-27B** 构建于 Qwen3.5-27B 之上，训练分为三个阶段：在 Phaser 和网页游戏代码上持续预训练、在合成的游戏设计任务上做监督微调、以及在经过测试的游戏玩法模块上进行基于执行结果的强化学习。
- 为了保持生成稳定，系统使用按原型划分的专用模板、三层文件读取策略、数据驱动的配置更新，以及重复的无头验证，而不是一次性输出代码。
- 论文还提出了 **OpenGame-Bench**，通过无头浏览器执行和基于 VLM 的评判，从 **Build Health**、**Visual Usability** 和 **Intent Alignment** 三个维度给生成的游戏打分。

## 结果
- 在使用 **150 个游戏提示** 的 **OpenGame-Bench** 上，搭配 **Claude Sonnet 4.6** 的 OpenGame 达到 **Build Health 72.4**、**Visual Usability 67.2** 和 **Intent Alignment 65.1**。
- 与列出的最强基线 **Cursor with Claude Sonnet 4.6** 相比，OpenGame 分别提升 **+5.6 BH**（72.4 vs 66.8）、**+5.8 VU**（67.2 vs 61.4）和 **+6.2 IA**（65.1 vs 58.9）。
- 搭配 **GameCoder-27B** 的 OpenGame 得分为 **63.9 BH**、**57.0 VU** 和 **54.1 IA**，高于搭配 **Qwen-3.5-27B** 的 OpenGame，后者得分为 **62.8 BH**、**53.8 VU** 和 **49.8 IA**。这意味着专用模型带来了 **+1.1 BH**、**+3.2 VU** 和 **+4.3 IA** 的提升。
- 在直接对比的闭源 LLM 基线中，**GPT-5.1** 得分为 **57.4 BH / 52.9 VU / 49.4 IA**，**Claude Sonnet 4.6** 为 **58.5 / 50.8 / 50.3**，**Gemini 3.1 Pro** 为 **53.6 / 60.2 / 42.1**。OpenGame 在三项指标上都超过了它们，不过 Gemini 在视觉质量上更接近。
- 该基准对每个任务使用 **三个不同随机种子的运行结果**，并报告平均分，这比单次通过/失败结果更稳定。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18394v1](http://arxiv.org/abs/2604.18394v1)
