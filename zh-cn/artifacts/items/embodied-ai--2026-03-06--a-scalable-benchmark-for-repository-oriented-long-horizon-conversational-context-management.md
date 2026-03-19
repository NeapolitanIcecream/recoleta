---
source: arxiv
url: http://arxiv.org/abs/2603.06358v1
published_at: '2026-03-06T15:09:40'
authors:
- Yang Liu
- Li Zhang
- Fang Liu
- Ping Lin
- Xinyi Li
topics:
- long-context-benchmark
- repository-oriented-llm
- context-management
- code-assistant-evaluation
- memory-system
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# A Scalable Benchmark for Repository-Oriented Long-Horizon Conversational Context Management

## Summary
本文提出 **LoCoEval**，这是首个面向代码仓库开发场景的长程对话上下文管理基准，用于评测代码助手在超长、多轮、含噪声对话中是否还能正确记住并利用关键信息。作者还提出了一个简单改进方法 **Mem0^R**，将对话记忆与仓库信息统一建模，在该基准上优于现有通用方法。

## Problem
- 代码仓库开发中的真实对话往往跨越 **数十到数百轮**，并伴随需求迭代、并行任务、追问与噪声，LLM 很容易因上下文过长而丢失关键信息。
- 现有上下文管理方法大多面向**通用聊天**，没有专门处理“对话信息 + 仓库代码信息”紧密交织的 repository-oriented 场景。
- 缺少可靠基准，导致研究者无法系统回答：模型到底能否在长程仓库对话中正确保留、检索并使用历史信息；这直接影响代码助手在真实开发流程中的可用性与一致性。

## Approach
- 作者构建了 **LoCoEval**：基于现有仓库级代码生成数据集，先抽取完成目标函数所必需的“信息项”，再把这些信息打散进长程多轮对话中，反向合成长对话评测样本。
- 为了模拟真实复杂开发过程，基准显式加入了**迭代需求、噪声信息、回溯性问题、并行主题**等模式，并让 mock 用户查询与 agent 响应在评测时**动态生成**。
- 数据规模上，LoCoEval 含 **128 个样本**、分为 **single-hop / multi-hop** 两个子集；每个样本平均 **2.5 个需求**、约 **50 轮对话**，总上下文长度可达 **64K–256K tokens**。
- 基准覆盖 **3 类任务**：topic awareness、information item extraction、function generation，用来测“记住了什么”“能否抽取关键信息”“最终能否正确完成代码任务”。
- 针对通用记忆系统不适配仓库场景的问题，作者提出 **Mem0^R**：把**对话历史与仓库信息写入统一记忆**，并结合与当前上下文相关的仓库检索，以更好地恢复完成任务所需的信息。

## Results
- LoCoEval 是一个明确可量化的基准：共 **2 个子集、128 个样本、768 个任务、37 个仓库**；每样本 **30–70 轮**、**64K–256K tokens**。
- 构建时从 DevEval 的 **1,825** 个样本中筛选，并剔除了 **788** 个可仅靠仓库检索解决的样本，以确保评测真正依赖长程对话中的上下文管理能力。
- 作者使用 **7 个基线**（其中含 **4 类代表性上下文管理方法**）和 **3 个先进 backbone LLMs** 进行评测；结论是**独立 LLM** 与现有**通用上下文管理方法**在仓库长对话中都面临显著困难，尤其是**memory systems** 表现不足。
- 论文声称 **Mem0^R 超过了所有基线方法（不含 Oracle）**，并表现出更好的鲁棒性；但给定摘录**没有提供具体分数、Pass@k 数值、数据集分项结果或相对提升百分比**。
- 最强的实证结论不是绝对数值突破，而是：**仓库场景的上下文管理不能只做通用对话记忆，必须联合建模对话内容与仓库代码信息**。

## Link
- [http://arxiv.org/abs/2603.06358v1](http://arxiv.org/abs/2603.06358v1)
