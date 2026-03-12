---
source: arxiv
url: http://arxiv.org/abs/2603.03194v1
published_at: '2026-03-03T12:52:01'
authors:
- Guoxin Chen
- Fanzhe Meng
- Jiale Zhao
- Minghao Li
- Daixuan Cheng
- Huatong Song
- Jie Chen
- Yuzhi Lin
- Hui Chen
- Xin Zhao
- Ruihua Song
- Chang Liu
- Cheng Chen
- Kai Jia
- Ji-Rong Wen
topics:
- code-agents
- software-engineering-benchmark
- swe-bench
- web-search-augmentation
- repository-generation
relevance_score: 0.02
run_id: materialize-outputs
---

# BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing?

## Summary
本文提出 **BeyondSWE**，用于评测代码智能体是否能超越“单仓库局部修 bug”的传统 SWE-bench 设定，并给出带搜索能力的基线框架 **SearchSWE**。结果显示，当前前沿代码智能体在更贴近真实软件工程的任务上整体成功率仍明显不足。

## Problem
- 现有 SWE 基准大多局限于**单仓库、局部函数级修复**，无法覆盖现实开发中常见的跨仓库检索、领域知识推理、依赖迁移和从文档生成系统等场景。
- 这很重要，因为真实软件工程经常需要**利用外部知识**、进行**代码库级改造**，而不是只在给定仓库内做小修补；若评测不覆盖这些能力，就会高估代码智能体的真实可用性。
- 论文要回答的问题是：**当前代码 agent 离开 single-repo bug fixing 后还能否有效工作？**

## Approach
- 构建了 **BeyondSWE** 基准，从两个维度扩展评测：**resolution scope**（从局部修复到全仓库迁移/整仓生成）和 **knowledge scope**（是否需要仓库外知识）。
- 基准包含 4 类任务：**CrossRepo**（借助外部仓库解决问题）、**DomainFix**（需要生物信息/量子等专业知识）、**DepMigrate**（因上游依赖破坏性更新而做全库迁移）、**Doc2Repo**（从自然语言规格文档生成完整仓库）。
- 总计 **500 个实例，来自 246 个真实 GitHub 仓库**；每个实例提供问题描述、Docker 环境和测试套件，并通过多轮自动化与人工质检保证环境可复现、无泄漏、不可通过修改测试作弊。
- 提出 **SearchSWE**：在常规代码 agent 的本地容器操作之外，增加 **search tool** 和 **browser tool**，让 agent 能交替进行仓库探索、代码修改与网页检索，同时用 blocklist 阻止直接访问目标仓库答案。

## Results
- BeyondSWE 的规模与复杂度明显高于现有 SWE 基准：平均每题涉及 **5.6 个文件、209.9 行代码、246 个仓库来源**；对比 SWE-bench-Verified 仅 **1.3 文件、11.6 行**，说明任务更接近真实工程复杂度。
- 在 **OpenHands** 下，最佳平均表现仅约 **41.82%**（Gemini 3 Pro），而论文总结当前代码 agent 在 BeyondSWE 上整体成功率**只有约 45%**，远低于文中引用的 **SWE-bench Verified 上 80%+** 水平，显示明显能力落差。
- 分任务看：OpenHands 下 **CrossRepo** 最好为 **44.72%**（Seed-Coder），**DomainFix** 最好为 **36.11%**（GLM-4.7），**DepMigrate** 最好为 **41.81%**（Gemini 3 Pro），**Doc2Repo Pass Rate** 最好为 **54.99%**（DeepSeek-V3.2）；但 **Doc2Repo 完全正确** 的仓库最多只有 **2 个**，说明从规格构建完整系统仍很困难。
- SearchSWE 带来的收益**不稳定**：例如 **Gemini 3 Pro** 在 SearchSWE 下平均分从 **41.82% 提升到 43.84%**，其中 **DomainFix +7.5**、**DepMigrate +2.3**；但 **Seed-Coder** 在 CrossRepo 上从 **44.72% 降到 38.89%（-5.8）**，表明“会搜索”与“会编码”并未被当前模型有效统一。
- CrossRepo 通常更能从搜索中受益，而 **Doc2Repo** 往往受搜索干扰更大；论文据此声称一个核心发现：**当前 LLM 的搜索能力与代码能力是各自成熟但尚未真正融合的两套能力。**

## Link
- [http://arxiv.org/abs/2603.03194v1](http://arxiv.org/abs/2603.03194v1)
