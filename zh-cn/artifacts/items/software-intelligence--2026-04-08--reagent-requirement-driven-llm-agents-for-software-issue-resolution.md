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
REAgent 通过在生成补丁前把含糊的 issue 报告转成结构化需求，来改进软件 issue 修复。它在 LLM agent 工作流之上加入了需求生成、需求质量评分和迭代式需求细化。

## 问题
- 仓库级 issue 修复对 LLM 很难，因为 issue 报告常常缺少关键上下文，或者语言含糊，这会导致补丁错误。
- 论文认为，以前大多数系统虽然改进了工具和工作流，但仍把原始 issue 描述当作任务规格。
- 这很重要，因为仓库级性能仍然偏低；论文引用 DeepSeek-V3.2 在 LiveCodeBench 上为 83.30%，但在 SWE-bench Pro 上只有 15.56%，还引用了先前证据，指出超过 70% 的 issue 缺少复现步骤或验证标准等要素。

## 方法
- REAgent 先构建一个 **issue-oriented requirement**：从 issue 和仓库上下文中提取出的结构化规格。该需求模式包含 9 个一级属性和 17 个二级属性，包括背景、复现步骤、预期行为、根因、修改位置和成功标准。
- 需求生成 agent 在 Docker 环境中使用文件检索、浏览和代码分析等工具探索仓库，然后用收集到的上下文填充需求模式。
- 需求评估 agent 生成补丁和 10 个测试脚本，然后用 **Requirement Assessment Score (RAS)** 给需求打分，定义为补丁通过的生成测试占比。只有当 RAS = 1.0 时，补丁才会被接受。
- 如果 RAS 低于 1.0，需求细化 agent 会把需求缺陷分成三类：冲突、遗漏和歧义。然后它会修改需求并重复这个循环。

## 结果
- 在 3 个基准和 2 个基础 LLM、共 6 种设置下，REAgent 在每一种设置中都优于 5 个代表性或最先进的基线。
- 论文报告，和基线相比，**% Resolved** 提高了 **9.17% 到 24.83%**，平均提升 **17.40%**。
- 它还报告，和基线相比，**% Applied** 提高了 **22.17% 到 49.50%**。
- 基准包括：**SWE-bench Lite**、**SWE-bench Verified** 和 **SWE-bench Pro**。基础模型包括：**DeepSeek-V3.2** 和 **Qwen-Plus**。
- 论文还说明，随着迭代次数 **N** 增加，REAgent 仍然优于迭代式基线；包含 4 个变体的消融实验也支持各个主要组件的贡献。
- 这段摘要没有给出每个基准的原始分数、每个表格对应的具体基线名称，或完整的消融实验数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06861v1](http://arxiv.org/abs/2604.06861v1)
