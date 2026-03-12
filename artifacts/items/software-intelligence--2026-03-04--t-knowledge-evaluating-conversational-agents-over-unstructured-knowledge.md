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
- agent-benchmark
- knowledge-grounding
- conversational-agents
- tool-use
- retrieval-augmented-generation
relevance_score: 0.78
run_id: materialize-outputs
---

# $τ$-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge

## Summary
本文提出 **τ-Knowledge**，一个面向非结构化知识库上的对话式智能体评测基准，并新增金融客服场景 **τ-Banking**。它重点测试智能体能否在长程对话中同时完成文档检索、政策推理、工具发现与状态修改，而不是只做单点检索或单点工具调用。

## Problem
- 现有基准通常把**检索**和**工具使用**分开评测，难以反映真实企业场景中“边对话边查私有知识库边执行操作”的综合难题。
- 在客服、金融等高风险应用里，智能体不仅要找到正确文档，还要理解复杂政策、发现可用工具，并做出**可验证且合规**的状态变更；这直接影响正确性、时延与用户信任。
- 真实环境常有目标不明确、用户意图变化、知识库私有且术语分布外等因素，使得仅靠传统RAG命中相关文档并不足以完成任务。

## Approach
- 作者扩展 τ-Bench，构建 **τ-Knowledge / τ-Banking**：一个模拟金融客服的部分可观测对话环境，任务成功由最终数据库状态是否正确决定。
- 知识库包含约 **698 篇文档 / 194,562 tokens / 21 类产品 / 51 个可发现工具**；智能体需要从自然语言文档中获取政策、流程、产品信息和工具说明。
- 设计了**discoverable tools**：某些工具初始对智能体不可见，只有先在知识库中找到文档说明，才能调用相应状态修改能力。
- 基准支持多种知识访问方式，保持检索机制无关：**稠密检索、BM25 稀疏检索、终端/文件系统搜索、gold 文档直给**，从而区分“找知识”和“用知识”的误差来源。
- 数据构建采用“**结构化规格 → 非结构化文档**”流水线，并结合人工审校，生成 **97 个任务**；平均每任务需 **18.6** 篇文档、**9.52** 次工具调用。

## Results
- 整体难度很高：跨所有模型与检索配置，最佳结果仅 **25.52% pass^1**，来自 **GPT-5.2 (high) + Terminal**。
- 可靠性随重复试验明显下降：论文指出最佳系统的 **pass^4 最高仅 13.40%**，说明同一任务多次运行稳定性不足。
- 即使移除检索瓶颈，表现仍然有限：**Gold** 条件下最强为 **Claude-4.5-Opus (high) = 39.69% pass^1**，表明问题不只是“找不到文档”，还包括政策推理、跨文档依赖和状态跟踪。
- 各检索方式平均表现（pass^1）分别为：**Gold 32.18%**，**Terminal 19.20%**，**Qwen3-emb-8b 17.11%**，**BM25 17.04%**，**text-embedding-3-large 16.88%**；Terminal 平均优于标准检索，但仍远低于 Gold。
- 代表性对比：**Claude-4.5-Opus (high)** 在 Gold 为 **39.69%**，用 Terminal 降至 **24.74%**，用 text-embedding-3-large 仅 **18.30%**；说明检索噪声会造成 **14.9–21.4 个百分点**的损失。
- 效率方面，**GPT-5.2 (high) + Terminal** 与 **Claude-4.5-Opus (high)** 表现相近，但前者约需 **1.7× tokens、2.3× shell commands、9× 更长完成时间**；论文据此强调应同时衡量成功率与求解效率。

## Link
- [http://arxiv.org/abs/2603.04370v1](http://arxiv.org/abs/2603.04370v1)
