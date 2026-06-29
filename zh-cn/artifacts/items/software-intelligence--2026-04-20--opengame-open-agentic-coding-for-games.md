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
## 总结
OpenGame 是一个开源的 agentic 系统，用自然语言游戏想法生成可游玩的 2D 网页游戏。它把面向游戏的代码模型、可复用项目模板和累积的调试协议结合起来，再用一个专门为交互式游戏生成设计的基准来评估输出。

## 问题
- 现有的 LLM 和代码 agent 可以很好地写出局部代码，但它们常常无法做出一个完整、可游玩的游戏，难以保持逻辑一致、场景连线、资源和多文件状态。
- 游戏生成比常规代码生成更难，因为正确性依赖运行时行为、视觉交互和引擎特定结构，而不只是代码能否通过编译。
- 这之所以重要，是因为游戏开发是自动化软件生产中的难例：如果 agent 不能处理长时程、跨文件、交互式系统，它们在许多具有类似集成要求的真实软件任务上也会继续失败。

## 方法
- OpenGame 使用 **Game Skill**，它分成两部分：**Template Skill** 和 **Debug Skill**。Template Skill 会扩展一个可复用的游戏骨架库，Debug Skill 会保存已验证的失败特征、原因和修复方法，让 agent 可以复用过去的修补方式。
- 这个 agent 采用六阶段流程：识别游戏类型、搭建项目框架、生成游戏设计文档、创建资源、用模板扩展点实现代码，然后运行构建/测试/修复循环。
- 其基础模型 **GameCoder-27B** 建立在 Qwen3.5-27B 之上，训练分三阶段：在 Phaser 和网页游戏代码上继续预训练，在合成的游戏设计任务上做监督微调，以及在经过测试的玩法模块上做执行约束强化学习。
- 为了让生成更稳定，系统使用按原型分类的模板、三层文件读取策略、数据驱动的配置更新，以及反复的无头浏览器验证，而不是一次性输出代码。
- 论文还引入了 **OpenGame-Bench**，它通过无头浏览器执行和基于 VLM 的判定，从 **Build Health**、**Visual Usability** 和 **Intent Alignment** 三个维度给生成的游戏打分。

## 结果
- 在 **OpenGame-Bench** 的 **150 个游戏提示**上，使用 **Claude Sonnet 4.6** 的 OpenGame 达到 **Build Health 72.4**、**Visual Usability 67.2**、**Intent Alignment 65.1**。
- 和列出的最强基线 **Cursor with Claude Sonnet 4.6** 相比，OpenGame 提升了 **+5.6 BH**（72.4 对 66.8）、**+5.8 VU**（67.2 对 61.4）和 **+6.2 IA**（65.1 对 58.9）。
- 使用 **GameCoder-27B** 的 OpenGame 得到 **63.9 BH**、**57.0 VU** 和 **54.1 IA**，高于使用 **Qwen-3.5-27B** 的 OpenGame，后者分别是 **62.8 BH**、**53.8 VU** 和 **49.8 IA**。这说明专门模型带来 **+1.1 BH**、**+3.2 VU** 和 **+4.3 IA** 的提升。
- 在直接的闭源 LLM 基线中，**GPT-5.1** 得到 **57.4 BH / 52.9 VU / 49.4 IA**，**Claude Sonnet 4.6** 得到 **58.5 / 50.8 / 50.3**，**Gemini 3.1 Pro** 得到 **53.6 / 60.2 / 42.1**。OpenGame 在这三个指标上都超过了它们，只有 Gemini 的视觉质量更接近。
- 这个基准对每个任务用 **不同随机种子的三次运行**，并报告平均分，比单次通过/失败结果更稳定。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18394v1](http://arxiv.org/abs/2604.18394v1)
