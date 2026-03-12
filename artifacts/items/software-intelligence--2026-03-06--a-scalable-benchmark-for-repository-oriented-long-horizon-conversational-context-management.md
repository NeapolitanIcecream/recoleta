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
- context-management
- benchmark
- code-assistant
- repository-level
- long-horizon-dialogue
- memory-system
relevance_score: 0.93
run_id: materialize-outputs
---

# A Scalable Benchmark for Repository-Oriented Long-Horizon Conversational Context Management

## Summary
本文提出 **LoCoEval**，这是首个面向代码仓库开发场景的长程多轮对话上下文管理基准，用来评测代码助手在超长会话中是否还能记住并正确利用关键信息。作者还提出了一个仓库感知的记忆方法 **Mem0^R**，用于把对话信息和仓库信息统一管理。

## Problem
- 代码仓库开发中的对话往往跨越几十到上百轮，且需求会迭代、并行推进并夹杂噪声，导致 LLM 容易丢失早期关键信息。
- 现有上下文管理方法大多面向通用聊天，不擅长处理“对话上下文 + 仓库代码/文本”强耦合的场景，因此代码助手在真实仓库开发里效果受限。
- 该方向缺少可靠基准，导致研究者无法系统评测：模型到底能否在 64K~256K token 的仓库级长对话中正确回忆、检索并回答问题。

## Approach
- 作者构建了 **LoCoEval**：一个面向 repository-oriented long-horizon conversation 的自动化基准，基于现有仓库级函数生成数据集 DevEval 构造。
- 基准通过 LLM 驱动流水线生成真实感对话：先从目标函数参考实现中提取“关键信息项”，再故意制造部分“干扰信息”，并把这些信息分散到多轮用户查询中，模拟迭代需求、噪声输入和追溯式提问。
- 为保证评测真正依赖对话而不是仅靠仓库检索，作者先过滤掉那些“仅用仓库 RAG 就能解出”的样本；共从 1,825 个 DevEval 样本中剔除了 788 个。
- LoCoEval 含 **128** 个样本、**2** 个子集（single-hop / multi-hop）、**3** 类任务（topic awareness、information item extraction、function generation）；每个样本平均 **2.5** 个需求、约 **50** 轮对话、总上下文约 **64K~256K** tokens。
- 在方法上，作者提出 **Mem0^R**：在 Mem0 基础上做仓库场景扩展，把对话历史与仓库信息写入统一记忆，并支持上下文感知的仓库检索。

## Results
- 基准规模与设置上，LoCoEval 共包含 **128 samples / 768 tasks / 37 repos**，每个样本 **30~70 turns**、**1~4 requirements**、**64K~256K tokens**。
- 实验覆盖 **7** 个基线方法（其中含 **4** 类代表性上下文管理方法）和 **3** 个先进 backbone LLM，说明评测具有较全面的比较范围。
- 作者明确声称：即便加入初步 RAG 适配，**standalone LLMs** 和现有通用上下文管理方法在仓库导向长程对话上仍面临“显著挑战”，尤其是 **memory systems** 对仓库信息利用不足。
- 作者进一步声称：**Mem0^R** 在整体表现上优于所有非 Oracle 基线，并且表现更稳健；文段未给出具体分数、Pass@k 数值或相对提升百分比，因此无法精确列出 benchmark 数字对比。
- 额外的最强具体结论是：仓库开发场景中的上下文管理不能只记会话，还必须把仓库代码/文本与会话共同建模；这是作者解释现有方法失效、以及 Mem0^R 优势的核心原因。

## Link
- [http://arxiv.org/abs/2603.06358v1](http://arxiv.org/abs/2603.06358v1)
