---
source: arxiv
url: http://arxiv.org/abs/2604.14004v1
published_at: '2026-04-15T15:50:29'
authors:
- Kangsan Kim
- Minki Kang
- Taeil Kim
- Yanlai Yang
- Mengye Ren
- Sung Ju Hwang
topics:
- coding-agents
- memory-transfer-learning
- cross-domain-generalization
- self-evolving-agents
- code-benchmarking
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Memory Transfer Learning: How Memories are Transferred Across Domains in Coding Agents

## Summary
## 摘要
这篇论文研究编码代理能否复用来自不同编码领域的记忆，而不只是在同一基准内复用。结果显示，跨领域记忆有帮助，而且抽象记忆，比如通用洞见，比原始轨迹更容易迁移。

## 问题
- 现有基于记忆的编码代理通常只在同一任务领域或同一基准内复用过去经验。
- 真实编码工作在不同领域之间共享很多结构，包括 shell、语言、测试、调试和接口约束，所以只用单领域记忆会让很多有用经验闲置。
- 论文要回答的是：异构记忆是否有帮助，哪类知识能迁移，以及哪种记忆形式能让迁移生效。

## 方法
- 作者提出 **Memory Transfer Learning (MTL)**：针对目标基准，代理从其他编码基准离线收集记忆，在推理时把这些记忆插入提示词中。
- 他们测试了四种抽象层级不同的记忆格式：**Trajectory**（原始动作/观察轨迹）、**Workflow**（筛选后的可复用动作）、**Summary**（任务和复盘摘要）、**Insight**（写成通用经验、避免任务特定细节的洞见）。
- 检索使用文本嵌入和余弦相似度；系统会从不包含目标基准的异构记忆池中，为每个查询选取前 3 条记忆。
- 评估覆盖 6 个编码基准：LiveCodeBench v6、Aider-Polyglot、SWE-Bench Verified、TerminalBench2、ReplicationBench 和 MLGym-Bench，指标是 Pass@3。
- 分析比较了零样本代理、MTL 各变体，以及 ReasoningBank 和 AgentKB 等此前的自进化方法，同时检查了不同基础模型之间的迁移。

## 结果
- 在 **GPT-5-mini** 上，零样本平均 **Pass@3 = 0.523**。表现最好的 MTL 变体 **Insight** 达到 **0.560**，在 6 个基准上的平均提升为 **+3.7%**。
- GPT-5-mini 在 **Insight** 下的基准提升分别是：**LiveCodeBench 0.910 -> 0.930（+2.0%）**、**SWE-Bench Verified 0.730 -> 0.770（+4.0%）**、**TerminalBench2 0.315 -> 0.360（+4.5%）**、**ReplicationBench 0.111 -> 0.189（+7.8%）**、**MLGym-Bench 0.667 -> 0.750（+8.3%）**，以及 **Aider-Polyglot 0.470 -> 0.470（0.0%）**。
- 跨模型迁移也有效：**DeepSeek V3.2** 在 Insight 下平均从 **0.542 -> 0.568（+2.6%）**；**Qwen3-Coder-480B-A35B-Instruct** 从 **0.483 -> 0.501（+1.8%）**。
- 在三个基准上与此前自进化基线比较时，**MTL = 0.630** 的平均 Pass@3，而 **ReasoningBank = 0.601**、**AgentKB = 0.613**。文中报告的差距是相对 ReasoningBank **+2.9%**，相对 AgentKB **+1.7%**。
- MTL 只用了 **431** 条记忆，而这组比较里 **AgentKB** 用了 **5,899** 条记忆，但 MTL 的得分更高。
- 论文声称的迁移机制主要是 **元知识**，比如 inspect-edit-verify 流程、验证习惯、小范围安全修补，以及能感知环境的调试。摘录指出，**算法策略迁移只解释了 5.5% 的收益**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14004v1](http://arxiv.org/abs/2604.14004v1)
