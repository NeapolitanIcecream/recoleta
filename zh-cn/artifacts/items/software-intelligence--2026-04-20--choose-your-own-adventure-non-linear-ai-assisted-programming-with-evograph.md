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
## 总结
EvoGraph 是一个面向 AI 辅助编程的 VS Code 插件，它把编码历史当作分支图，而不是单一聊天线程。论文认为，这种方式更贴近开发者探索备选方案、回看先前状态和检查 AI 生成改动的实际工作方式。

## 问题
- 现有的 AI 编码工具大多是线性的聊天界面，但编程工作往往会分叉、回退，并比较不同方案。
- 作者的初步研究中，开发者反映了三个反复出现的问题：不便探索多个解法路径、难以跟踪较长的提示序列、以及看不清哪些代码来自哪次 AI 交互。
- 这会让开发者丢失有用的中间结果，难以在长会话中恢复上下文，也更难审查或信任 AI 生成的修改。

## 方法
- 作者构建了 **EvoGraph**，这是一个 VS Code 扩展，会把 AI 交互和代码变更记录为带检查点的开发图。
- 该图保存三类检查点：手动检查点、AI 提示检查点，以及 AI 代码应用检查点。
- 用户可以回到更早的节点，从过去的状态分支出去，对比备选方案，合并路径，并把代码改动和生成这些改动的提示一起查看。
- 系统提供溯源支持，开发者可以把代码编辑追溯到对应的提示上下文；它也可以把现有图历史作为未来 AI 交互的上下文。
- 这个设计基于对 **8 名开发者** 的访谈，并在一项被试内研究中用 **20 名参与者** 与一个基线 AI 辅助编程界面进行了评估。

## 结果
- 论文报告了一项涉及 **8 名开发者** 的初步访谈研究，识别出 EvoGraph 要解决的主要工作流问题：探索历史、长交互管理，以及作者归属和溯源跟踪。
- 在一项包含 **20 名参与者** 的用户研究中，EvoGraph 据称比基线界面更能帮助开发者探索备选方案、管理提示交互和跟踪 AI 生成的改动。
- 参与者也报告说，使用 EvoGraph 时的认知负荷低于基线，但摘录中**没有提供具体的认知负荷分数、p 值或效应量**。
- 摘录中最明确的结论是定性的：参与者说，这种图形表示支持更安全的探索、更快的迭代，以及对 AI 生成代码更好的反思。
- 摘录中**没有给出任务完成时间、准确率、采纳率或其他定量性能指标**来比较 EvoGraph 和基线。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18883v1](http://arxiv.org/abs/2604.18883v1)
