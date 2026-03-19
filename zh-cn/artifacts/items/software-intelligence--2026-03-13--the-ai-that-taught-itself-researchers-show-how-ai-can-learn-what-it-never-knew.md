---
source: hn
url: https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/
published_at: '2026-03-13T23:16:41'
authors:
- hhs
topics:
- llm-code-generation
- compiler-feedback
- low-resource-learning
- iterative-refinement
- program-synthesis
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# The AI that taught itself: Researchers show how AI can learn what it never knew

## Summary
这项研究表明，AI 不必完全受限于见过多少训练数据；只要给它一个明确、可验证的外部反馈回路，它就能在极低资源领域显著提升表现。作者用一种冷门编程语言 Idris 证明了这一点，把 GPT-5 的解题成功率从很低的水平大幅推高。

## Problem
- 传统假设认为，AI 在某个领域的能力基本受训练数据覆盖度限制；对低资源语言或冷门任务尤其如此。
- 这很重要，因为许多真实世界任务都处在“数据稀缺但规则清晰”的场景，如小众编程语言、数学证明、法律逻辑和低资源自然语言。
- 论文要解决的是：**当模型几乎没见过某个领域时，能否仅靠结构化反馈而不是额外训练数据，把性能提升到远超初始水平？**

## Approach
- 研究者选择了极其冷门的编程语言 **Idris** 作为测试对象；其公开代码仓库约 **2,000** 个，而 Python 超过 **2,400 万**，数据量相差约 **10,000 倍**。
- 他们让 **GPT-5** 在 Exercism 上完成 **56** 道 Idris 编程练习，先测原始能力，再比较多种增强方式。
- 简单提供文档、错误手册和参考资料只能带来有限提升，说明“多给点说明材料”不是关键突破口。
- 核心机制是 **compiler feedback loop**：把编译器返回的精确报错信息直接喂回模型，让它针对错误修复后重新提交；每题最多迭代 **20** 次。
- 用最简单的话说，这个方法就是：**让 AI 先尝试，再把机器能客观指出的错误逐轮告诉它，直到它改对为止。**

## Results
- 在 **56** 道 Idris 题上，GPT-5 开箱即用只做对 **22/56**，成功率 **39%**。
- 作为对比，文中给出的同模型成功率为：**Python 90%**、**Erlang 74%**，说明 Idris 初始表现显著更差。
- 仅提供文档、错误手册和参考指南后，Idris 成功率只提升到 **60% 出头（low 60s）**，没有出现决定性跃升。
- 引入编译器反馈回路后，成功率从 **39%** 提升到 **96%**；相当于从 **22/56** 提高到大约 **54/56**。
- 论文的核心主张是：**在训练覆盖极弱的领域，只要存在清晰、正确、可程序化的反馈信号，模型能力可以被“解锁”并显著超出其初始零样本/少样本表现。**
- 文中还提出潜在外推方向，如 3D 结构设计、数学证明、法律逻辑、低资源人类语言翻译，但这些扩展应用在所给文本中**尚未提供定量实验结果**。

## Link
- [https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/](https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/)
