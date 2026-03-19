---
source: arxiv
url: http://arxiv.org/abs/2603.11103v1
published_at: '2026-03-11T09:23:20'
authors:
- Zhiyuan Zeng
- Yichi Zhang
- Yong Shan
- Kai Hua
- Siyuan Fang
- Zhaiyu Liu
- Jiaheng Liu
- Haozhe Wang
- Yining Zheng
- Ming Ding
- Ke Shen
- Ge Zhang
- Wenhao Huang
- Xipeng Qiu
topics:
- llm-pretraining
- code-generation
- synthetic-data
- agent-trajectories
- long-context
- software-engineering
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Understanding by Reconstruction: Reversing the Software Development Process for LLM Pretraining

## Summary
本文提出“通过重建来理解”的预训练范式：不是只看代码仓库的最终结果，而是反向合成其开发过程中的规划、读写、调试与推理轨迹，再用这些轨迹持续预训练LLM。实验表明，这种把静态仓库转成动态 agent 轨迹的数据，可提升长上下文理解、代码生成、部分推理与软件工程代理能力。

## Problem
- 现有代码预训练主要使用**静态仓库终态**，丢失了需求分析、架构规划、依赖处理、调试与迭代等中间过程。
- 因此模型更容易学到“代码长什么样”，却较难学到**复杂软件开发的长程因果推理**与 agentic 行为。
- 这很重要，因为真实软件工程依赖跨文件、长上下文、分步骤决策；只记住最终代码不足以支撑复杂工程任务。

## Approach
- 核心方法是把一个真实代码仓库当作“标准答案”，**反向重建**出一条开发它的 synthetic agent trajectory。
- 他们用**多智能体模拟**：Main Agent 先生成项目需求与文件级实施计划；Sub-Agent 按文件执行，进行思考、读取已有文件、再写出当前文件。
- 为避免纯 LLM 生成轨迹的幻觉，方法注入仓库的**真实结构信息**：文件树、跨文件依赖图、AST 结构；并用真实文件内容替换 Read/Write 的观测与最终代码结果。
- 他们再对轨迹中的 CoT 做**基于搜索的优化**：对每一步思考采样替代版本，只在其能降低目标真值代码 perplexity 时才替换，目标是让“思考更有利于生成正确代码”。
- 最后将多智能体层级轨迹展平成单序列文档，用于**持续预训练** Llama-3-8B，并对 observation token 做 loss masking，只训练 Think/Action 部分。

## Results
- 数据规模：约**300k GitHub 仓库**，合成约**4B tokens** 轨迹；持续预训练 **20B tokens**，上下文窗口 **64k**。CoT 搜索为每步生成 **2** 个候选，迭代 **3** 轮。
- 长上下文：**Ruler-65,536** 上 Repo2Agent-Search 达 **61.80**，高于 Prolong **57.10** 与 Raw-Repos **61.00**；**Helmet-32,768** 上达 **62.65**，高于 Raw-Repos **60.98** 与 Prolong **61.57**。
- 代码能力：**HumanEval** 上 Repo2Agent-Search **37.20**，高于 Raw-Repos **34.76**、Repo2Agent **36.59**、Prolong **16.46**；**LongCodeBench-32k** 上 **36.46**，高于 Raw-Repos **34.16** 和 Prolong **29.38**。
- 长代码任务并非全面领先：**LongCodeBench-64k** 上 Repo2Agent **31.05** 最好，优于 Repo2Agent-Search **30.26**、Prolong **30.52**、Raw-Repos **27.37**，说明搜索优化收益并不总是单调。
- 推理迁移：**BBH** 上 Repo2Agent-Search **67.03**，略高于 Prolong **66.69**；**MATH** 上 **3.76**，高于 Repo2Agent **3.72**、Raw-Repos **2.18**、Prolong **1.64**；但 **GSM-8k** 上 Raw/Reop2Agent **61.94** 反而高于 Search **60.96**。
- 软件工程 agent 基准 **APTBench**：总体平均 Repo2Agent **30.10**，高于 Repo2Agent-Search **29.65** 与 Raw-Repos **29.02**；表明未搜索版本在部分 agentic 软件工程能力上更稳。

## Link
- [http://arxiv.org/abs/2603.11103v1](http://arxiv.org/abs/2603.11103v1)
