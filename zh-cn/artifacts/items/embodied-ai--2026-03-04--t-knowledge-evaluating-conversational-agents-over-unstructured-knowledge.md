---
source: arxiv
url: http://arxiv.org/abs/2603.04370v1
published_at: '2026-03-04T18:34:47'
authors:
- Quan Shi
- Alexandra Zytek
- Pedram Razavi
- Karthik Narasimhan
- Victor Barres
topics:
- benchmarking
- conversational-agents
- retrieval-augmented-generation
- tool-use
- knowledge-grounding
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# $τ$-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge

## Summary
本文提出 **τ-Knowledge**，一个面向非结构化知识库上的对话式智能体评测基准，并新增金融客服场景 **τ-Banking**。它强调：智能体不仅要检索文档，还必须正确理解政策、发现可用工具，并在多轮对话中完成可验证的状态变更。

## Problem
- 现有基准通常把**检索**与**工具使用**分开评测，难以反映企业客服等真实部署中“边对话边查知识、再执行操作”的复杂流程。
- 在私有、非结构化、长文档知识库中，智能体需要处理**模糊用户意图、复杂内部政策、跨文档依赖、部分可观测状态**，这比普通QA或单步工具调用难得多。
- 这件事重要，因为现实中的知识密集型客服系统若做错，会导致**错误的账户状态修改、违规决策、低效率交互和用户信任下降**。

## Approach
- 构建新基准 **τ-Knowledge**，其中的 **τ-Banking** 域模拟真实金融客服：智能体需在多轮对话中查询约 **698 篇文档 / 194,562 tokens** 的知识库，并通过工具修改底层银行数据库状态。
- 核心机制很简单：**先从文档里找到规则和工具说明，再按规则调用工具，最终看数据库状态是否正确**。也就是说，评测的不只是“找得到”，而是“找得到 + 看得懂 + 做得对”。
- 引入 **discoverable tools**：部分工具起初对智能体不可见，只在文档里被提到；智能体必须先检索到相关说明，才能调用这些会改变环境状态的工具。
- 基准对检索方式保持开放，支持**稠密检索、BM25 稀疏检索、终端/文件系统搜索、gold 文档直给**等配置，从而比较“知识访问”与“知识利用”的不同瓶颈。
- 数据构建上，作者使用**结构化到非结构化**的生成流水线：先生成一致的产品/政策/工具结构化规格，再扩展成自然语言文档，并结合人工审校与任务验证保证一致性和可解性。

## Results
- **主结果很低**：所有测试系统中最佳仅达到 **25.52% pass^1**，对应 **GPT-5.2 (high reasoning) + Terminal**；说明当前前沿模型在这类真实知识驱动对话任务上仍明显不足。
- **可靠性快速下降**：作者指出最佳配置的 **pass^4 最高也只有 13.40%**，说明同一任务重复运行时成功率不稳定，鲁棒性较差。
- 即使移除检索瓶颈、直接提供任务所需文档（**Gold** 设置），最好结果也只有 **39.69% pass^1**（**Claude-4.5-Opus, high**），表明问题不只是检索，更在于**政策理解、跨文档推理和状态跟踪**。
- 按平均结果看，不同检索方式的 **pass^1** 分别为：**Gold 32.18%**、**Terminal 19.20%**、**Qwen3-emb-8b 17.11%**、**BM25 17.04%**、**text-embedding-3-large 16.88%**；Terminal 整体最好，但仍远低于 Gold。
- 代表性对比：**Claude-4.5-Opus (high)** 在 **Gold** 下为 **39.69%**，切换到 **Terminal** 降到 **24.74%**，到 **dense retrieval** 仅 **18.30% / 19.59%**；说明检索配置会带来 **约 15–21 个点** 的显著损失。
- 效率方面，论文声称 **GPT-5.2 (high) + Terminal** 与 **Claude-4.5-Opus (high)** 表现相近，但前者需要约 **1.7× tokens、2.3× shell commands、9× 更长耗时**，表明当前系统往往靠更多搜索和试错来弥补能力不足。

## Link
- [http://arxiv.org/abs/2603.04370v1](http://arxiv.org/abs/2603.04370v1)
