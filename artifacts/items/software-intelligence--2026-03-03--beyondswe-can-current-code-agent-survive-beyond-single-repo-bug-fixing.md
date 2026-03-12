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
- search-augmented-agents
- cross-repository-reasoning
- repository-generation
relevance_score: 0.97
run_id: materialize-outputs
---

# BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing?

## Summary
BeyondSWE提出了一个超越单仓库局部修Bug的新型代码智能体评测基准，并用它检验当前前沿代码模型在跨仓库、领域知识、依赖迁移和从文档生成仓库等更真实的软件工程任务上的能力。论文同时提出SearchSWE，用统一的“编码+检索”框架分析外部搜索是否真正提升代码智能体表现。

## Problem
- 现有SWE基准大多只评测**单仓库、局部、函数级**问题修复，和真实软件工程中常见的跨仓库依赖、领域知识、全库迁移、从规格生成系统等场景差距很大。
- 因此我们并不知道当前代码智能体离“真实可用的软件工程代理”还有多远；这很重要，因为产业中的开发任务往往需要**外部知识获取**和**大范围代码变更**。
- 论文要回答的核心问题是：**当前代码智能体能否在超越单Repo bug fixing的设定下生存下来？**

## Approach
- 构建了**BeyondSWE**基准，从两个维度扩展评测：**resolution scope**（从局部修复到全仓库改造/完整生成）和**knowledge scope**（是否需要代码库外知识）。
- 基准包含4类任务、共**500个实例**、来自**246个真实GitHub仓库**：**CrossRepo**（借助外部仓库解决问题）、**DomainFix**（需要专业领域知识）、**DepMigrate**（因上游依赖破坏性升级而进行全库迁移）、**Doc2Repo**（从自然语言规格直接生成完整仓库）。
- 为保证可复现性，作者使用LLM代理自动构建Docker环境，并通过严格检查保留稳定样本：补丁前要求**P2P通过、F2P失败**，补丁后要求两者都通过；评测时还把补丁应用到**全新容器**中，避免环境污染。
- 提出**SearchSWE**框架，在本地Docker编码环境之外增加**web search**和**browser**工具，使智能体能交替进行仓库探索、代码修改和外部资料检索；同时通过目标仓库访问屏蔽机制防止作弊。

## Results
- BeyondSWE整体显著更难：论文称当前代码智能体在该基准上的成功率只有约**45%**，远低于文中对比提到的SWE-bench Verified上常见的**80%+**水平，说明“超越单仓库修Bug”仍存在明显能力鸿沟。
- 在**OpenHands**框架下，最佳平均表现仅约**41.82%**（**Gemini 3 Pro**）；其他如**GLM-4.7 41.20%**、**DeepSeek-V3.2 40.01%**、**Kimi-K2 39.81%**，没有任何模型在所有任务上全面占优。
- 各任务中：**CrossRepo**最佳为**Seed-Coder 44.72%**；**DomainFix**最佳为**GLM-4.7 36.11%**；**DepMigrate**最佳为**Gemini 3 Pro 41.81%**；**Doc2Repo**最高测试通过率为**DeepSeek-V3.2 54.99%**，但“完全正确”仓库最多只有**2个**，表明从规格生成完整系统尤其困难。
- SearchSWE带来的提升是**不稳定**的。比如**Gemini 3 Pro**在SearchSWE下平均分从**41.82%**升到**43.84%**，其中**DomainFix +7.5%**（31.94%→39.44%）、**DepMigrate +2.3%**（41.81%→44.07%）；但**Doc2Repo -1.3**（52.03→50.73）。
- 一些模型从搜索中受益有限甚至退化，例如**Seed-Coder**在**CrossRepo**从**44.72%**降到**38.89%**（**-5.8%**），平均分从**36.90%**降到**34.01%**。这支持论文的核心结论：**搜索能力与编码能力尚未被有效统一**。
- 基准规模上，BeyondSWE相较已有SWE类基准覆盖更广：平均涉及**5.6个文件**、**209.9行**修改，显著高于SWE-bench Verified的**1.3个文件/11.6行**、SWE-bench Live的**2.7个文件/65.1行**以及SWE-bench Pro的**4.1个文件/107.4行**。

## Link
- [http://arxiv.org/abs/2603.03194v1](http://arxiv.org/abs/2603.03194v1)
