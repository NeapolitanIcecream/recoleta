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
## 总结
HepScript 是一种嵌入 Ruby 的 DSL，允许物理学家和 LLM 代理为 BESIII 高能物理分析流程编写规格，然后生成 BOSS 和 ROOT 代码。它的核心主张是，受约束的 DSL 能让代理生成代码更可靠，也能减少人工编码工作量。

## 问题
- HEP 分析使用海量数据和实验专用软件，所以直接让 LLM 生成代码时，可能会在领域规则、长流程和底层 API 上出错。
- BESIII 流程需要一座桥，把物理意图，包括粒子重建和选择切分，转换成可生产的 BOSS/ROOT 代码。
- 这个问题很重要，因为分析代码重复、容易出错，而且如果没有足够窄的动作空间，代理很难安全生成代码。

## 方法
- HepScript 用受约束的 Ruby 语法表达数据集准备、基础选择、高级选择、可视化和统计分析。
- 处理器把 HepScript 转成目标代码，输出可以是 BOSS、ROOT、shell 脚本、Python 或 C++ 片段。
- 处理器用模板生成稳定代码，用 Ruby 转换器处理复杂语法，并用 LLM 处理依赖分析的任务，包括级联衰变逻辑和 ROOT 脚本。
- LLM 通过一个长提示词从论文中生成 HepScript，提示词里包含一个完整工作流示例和 YARD API 文档；重试循环会把处理器错误反馈给模型。

## 结果
- 对 45 篇 BESIII 论文手写的 HepScript 生成了 63 个 BOSS 算法包；在关闭 LLM 辅助组件后，这 63 个包全部无错误编译通过。
- 在两个完整案例中，HepScript 通过去掉 BOSS 样板代码和重复的 ROOT 绘图代码，将人工编写的分析代码减少了 93%。
- 对 72 个 BOSS 包进行 LLM 生成 HepScript 时，DeepSeek-R1 的初始成功率为 47.3%，一次重试后为 87.8%，三次重试后为 94.6%。
- 在同样的 72 包任务上，GLM-4.7 的初始成功率为 43.2%，一次重试后为 90.5%，三次重试后为 95.9%。
- 在手写规格的变量存储子任务中，DeepSeek-V3、GPT-4o、GLM-4.7 和 Qwen3-Max 的起始成功率为 93.8% 到 96.9%；所有测试模型在一次重试后都达到 98.5%。
- 两个 ROOT 案例研究完成了端到端执行，并复现了原始 BESIII 论文中的图；作者说明这些是流程检查，不是官方物理结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01423v1](https://arxiv.org/abs/2605.01423v1)
