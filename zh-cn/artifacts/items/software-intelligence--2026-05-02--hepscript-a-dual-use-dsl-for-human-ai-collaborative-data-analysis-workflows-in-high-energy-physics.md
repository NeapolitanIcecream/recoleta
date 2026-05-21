---
source: arxiv
url: https://arxiv.org/abs/2605.01423v1
published_at: '2026-05-02T12:42:34'
authors:
- Junkun Jiao
- Tong Liu
- Ke Li
- Weimin Song
- Yipu Liao
- Bolun Zhang
- Beijiang Liu
- Chang-Zheng Yuan
- Yue Sun
topics:
- domain-specific-language
- code-generation
- llm-agents
- scientific-workflows
- human-ai-collaboration
- high-energy-physics
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# HepScript: A Dual-Use DSL for Human-AI Collaborative Data Analysis Workflows in High-Energy Physics

## Summary
## 摘要
HepScript 是一种嵌入 Ruby 的 DSL，可让物理学家和 LLM agent 指定 BESIII 高能物理分析工作流，并生成 BOSS 和 ROOT 代码。论文的主要主张是，受约束的 DSL 能提高 agent 生成代码的可靠性，并减少人工编码工作。

## 问题
- HEP 分析使用大规模数据集和实验专用软件，因此直接用 LLM 生成代码时，可能在领域规则、长工作流和底层 API 上失败。
- BESIII 工作流需要在物理意图与生产级 BOSS/ROOT 代码之间建立桥梁，物理意图包括粒子重建和选择截断。
- 这个问题很重要，因为分析代码重复多、容易出错；如果没有狭窄的动作空间，agent 很难安全地生成这些代码。

## 方法
- HepScript 用受约束的 Ruby 语法表达数据集准备、基础选择、高级选择、可视化和统计分析。
- 处理器将 HepScript 转换为面向 BOSS、ROOT、shell 脚本、Python 或 C++ 片段的目标代码。
- 处理器使用模板生成稳定代码，用 Ruby 转换器处理复杂语法，并调用 LLM 完成依赖具体分析的任务，包括级联衰变逻辑和 ROOT 脚本。
- LLM 根据论文生成 HepScript；提示词很长，包含一个完整工作流示例和 YARD API 文档；重试循环会把处理器错误反馈给模型。

## 结果
- 研究者为 45 篇 BESIII 论文人工编写 HepScript，并生成了 63 个 BOSS 算法包；在关闭 LLM 辅助组件后，全部 63 个包都无错误编译通过。
- 在两个完整案例研究中，HepScript 去除了 BOSS 样板代码和重复的 ROOT 绘图代码，使人工编写的分析代码减少了 93%。
- 在覆盖 72 个 BOSS 包的 LLM 生成 HepScript 任务中，DeepSeek-R1 的初始成功率为 47.3%，一次重试后为 87.8%，三次重试后为 94.6%。
- 在相同的 72 包任务中，GLM-4.7 的初始成功率为 43.2%，一次重试后为 90.5%，三次重试后为 95.9%。
- 在面向人工编写规格的变量存储子任务中，DeepSeek-V3、GPT-4o、GLM-4.7 和 Qwen3-Max 的初始成功率为 93.8-96.9%；所有受测模型在一次重试后都达到 98.5%。
- 两个 ROOT 案例研究完成了端到端执行，并复现了原始 BESIII 论文中的图；作者说明这些是流水线检查，并非官方物理结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01423v1](https://arxiv.org/abs/2605.01423v1)
