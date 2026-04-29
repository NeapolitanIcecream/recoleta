---
source: arxiv
url: http://arxiv.org/abs/2604.18883v1
published_at: '2026-04-20T22:05:09'
authors:
- Vassilios Exarhakos
- Jinghui Cheng
- Jin L. C. Guo
topics:
- ai-assisted-programming
- code-intelligence
- ide-plugin
- human-ai-interaction
- provenance-tracking
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Choose Your Own Adventure: Non-Linear AI-Assisted Programming with EvoGraph

## Summary
## 概要
EvoGraph 是一个用于 AI 辅助编程的 VS Code 插件。它把编码历史视为分支图，而不是单一的聊天线程。论文认为，这种方式更符合开发者实际的工作过程，因为他们经常要探索不同方案、回到先前状态，并检查 AI 生成的修改。

## 问题
- 目前的 AI 编码工具大多采用线性的聊天界面，但编程工作本身常常需要分叉、回退和比较不同方案。
- 作者在前期研究中发现，开发者反复提到三个问题：缺少对多条解决路径探索的支持、难以跟踪很长的提示词交互序列，以及难以看清哪些代码对应哪些 AI 交互。
- 这很重要，因为开发者可能会丢失有价值的中间成果，在长时间会话中难以找回上下文，也更难审查或信任 AI 生成的编辑内容。

## 方法
- 作者构建了 **EvoGraph**，这是一个 VS Code 扩展，用检查点将 AI 交互和代码变更记录为开发图。
- 该图保存三类检查点：手动检查点、AI 提示词检查点和 AI 代码应用检查点。
- 用户可以回到更早的节点、从过去的状态分支、比较不同方案、合并路径，并把代码变更和生成这些变更的提示词放在一起查看。
- 系统支持溯源，开发者可以把代码编辑追溯到对应的提示词上下文；它还可以把现有的图历史作为后续 AI 交互的上下文。
- 该设计基于对 **8 名开发者** 的访谈，并在一项被试内研究中与一个基线 AI 辅助编程界面进行了比较评估，研究共有 **20 名参与者**。

## 结果
- 论文报告了一项针对 **8 名开发者** 的前期访谈研究，确定了 EvoGraph 试图解决的主要工作流问题：探索历史、长交互管理，以及作者归属/溯源跟踪。
- 在一项包含 **20 名参与者** 的用户研究中，据称 EvoGraph 在帮助开发者探索不同方案、管理提示词交互和跟踪 AI 生成的修改方面优于基线界面。
- 参与者还表示，使用 EvoGraph 时的**认知负荷更低**，但摘录中**没有给出认知负荷的具体分数、p 值或效应量**。
- 摘录中最明确、最具体的结论是定性的：参与者表示，这种图结构支持更安全的探索、更快的迭代，以及对 AI 生成代码更好的回顾。
- 摘录中**没有提供 EvoGraph 与基线相比的任务完成时间、准确率、接受率或其他量化性能指标**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18883v1](http://arxiv.org/abs/2604.18883v1)
