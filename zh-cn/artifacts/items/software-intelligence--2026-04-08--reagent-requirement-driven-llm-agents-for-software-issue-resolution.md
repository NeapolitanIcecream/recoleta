---
source: arxiv
url: http://arxiv.org/abs/2604.06861v1
published_at: '2026-04-08T09:22:30'
authors:
- Shiqi Kuang
- Zhao Tian
- Kaiwei Lin
- Chaofan Tao
- Shaowei Wang
- Haoli Bai
- Lifeng Shang
- Junjie Chen
topics:
- software-engineering
- llm-agents
- issue-resolution
- requirements-engineering
- code-generation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# REAgent: Requirement-Driven LLM Agents for Software Issue Resolution

## Summary
## 摘要
REAgent 在生成补丁前，先把含糊的问题报告整理成结构化需求，从而提升软件问题解析效果。它在 LLM agent 工作流之上加入了需求生成、需求质量评分和迭代式需求细化。

## 问题
- 对 LLM 来说，仓库级问题解析很难，因为问题报告常常缺少关键上下文，或使用含糊的表述，进而导致错误补丁。
- 论文认为，之前大多数系统改进了工具和工作流，但仍然把原始问题描述直接当作任务规格。
- 这一点很重要，因为仓库级表现仍然较低；论文引用的数据是，DeepSeek-V3.2 在 LiveCodeBench 上达到 83.30%，但在 SWE-bench Pro 上只有 15.56%；还引用了先前证据，说明超过 70% 的问题缺少复现步骤或验证标准等要素。

## 方法
- REAgent 首先构建一个**面向问题的需求**：这是从 issue 和仓库上下文中提取出的结构化规格。该需求模式包含 9 个一级属性和 17 个二级属性，包括背景、复现步骤、预期行为、根因、修改位置和成功标准。
- 需求生成 agent 使用文件检索、浏览和代码分析等工具，在 Docker 环境中探索仓库，然后用收集到的上下文填充需求模式。
- 需求评估 agent 生成一个补丁和 10 个测试脚本，然后用 **Requirement Assessment Score (RAS)** 对需求打分，其定义是补丁通过的生成测试所占比例。只有当 RAS = 1.0 时，补丁才会被接受。
- 如果 RAS 低于 1.0，需求细化 agent 会从三类问题中诊断需求缺陷：冲突、遗漏和歧义。随后它会修订需求并重复这一循环。

## 结果
- 在 3 个基准和 2 个基础 LLM 上，共 6 种设置中，REAgent 在每一种设置下都优于 5 个有代表性或当前最先进的基线方法。
- 论文报告，REAgent 相比基线在 **% Resolved** 上提升了 **9.17% 到 24.83%**，平均提升 **17.40%**。
- 论文还报告，REAgent 相比基线在 **% Applied** 上提升了 **22.17% 到 49.50%**。
- 基准包括：**SWE-bench Lite**、**SWE-bench Verified** 和 **SWE-bench Pro**。基础模型包括：**DeepSeek-V3.2** 和 **Qwen-Plus**。
- 论文还指出，随着迭代次数 **N** 增加，REAgent 仍然持续优于迭代式基线；包含 4 个变体的消融实验也支持各个主要组件的贡献。
- 这段摘录没有给出各基准的原始分数、每张表对应的确切基线名称，或完整的消融实验数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06861v1](http://arxiv.org/abs/2604.06861v1)
