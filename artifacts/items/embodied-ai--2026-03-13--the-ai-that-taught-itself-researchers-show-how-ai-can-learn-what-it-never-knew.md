---
source: hn
url: https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/
published_at: '2026-03-13T23:16:41'
authors:
- hhs
topics:
- iterative-feedback
- low-resource-learning
- code-generation
- compiler-guidance
- self-correction
relevance_score: 0.14
run_id: materialize-outputs
---

# The AI that taught itself: Researchers show how AI can learn what it never knew

## Summary
这项研究表明，AI在极低资源领域并不完全受限于训练数据，只要加入正确的外部反馈回路，就能显著提升表现。作者用GPT-5在冷门编程语言Idris上的代码生成实验，展示了这种“自我纠错式”提升。

## Problem
- 传统假设认为，模型在某个领域的能力基本受其见过的数据量限制；低资源领域因此表现很差。
- 这在冷门编程语言、形式化推理、低资源人类语言等场景尤其重要，因为可用训练数据极少。
- 研究要回答的是：在几乎没有足够训练覆盖的情况下，AI能否借助外部反馈学会完成原本不擅长的任务？

## Approach
- 研究者选用极低资源语言 **Idris** 作为测试对象：公开仓库约 **2,000** 个，而 Python 超过 **2,400万** 个，数据规模相差约 **10,000 倍**。
- 让 **GPT-5** 解决 Exercism 上的 **56** 道 Idris 编程题，先测基础表现，再比较不同增强方式。
- 试过提供文档、错误手册、参考资料等静态辅助，这些方法只能把成功率提升到 **60%出头**。
- 核心方法是 **compiler feedback loop**：把编译器返回的具体报错直接喂回模型，让它针对错误修复并重试，每题最多 **20 次**。
- 这个机制本质上很简单：模型先写代码，编译器指出哪里错了，模型按错误信息改，再反复尝试，直到通过。

## Results
- 在 Idris 上，GPT-5 开箱即用只解出 **22/56** 题，成功率 **39%**。
- 作为对比，文中称 GPT-5 在 **Python** 上成功率约 **90%**，在 **Erlang** 上约 **74%**，说明 Idris 确实是明显的低资源难例。
- 提供文档和参考材料后，Idris 成功率仅提升到 **60%出头**，改进有限，未接近主流语言水平。
- 使用编译器反馈回路后，成功率从 **39% 提升到 96%**，约为 **54/56** 题，较初始提升 **57 个百分点**。
- 作者据此声称：只要任务存在清晰、正确、可自动生成的反馈信号，AI就可能在训练覆盖不足的领域显著超越“仅靠训练数据”所能达到的表现。
- 文中未提供更细的统计显著性、消融实验或跨模型/跨任务系统评测；对数学证明、法律逻辑、3D建模、低资源人类语言等应用目前主要是前瞻性推断。

## Link
- [https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/](https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/)
