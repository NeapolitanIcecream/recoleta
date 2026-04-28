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
这篇论文研究编码代理能否复用来自不同编码领域的记忆，而不只复用同一基准中的记忆。结果表明，跨领域记忆有帮助，而且抽象记忆（如一般性洞见）比原始轨迹更容易迁移。

## 问题
- 现有基于记忆的编码代理通常只在同一任务领域或同一基准内复用过去的经验。
- 真实编码工作在不同领域之间共享很多共同结构，包括 shell、编程语言、测试、调试和接口约束，因此单一领域记忆会浪费有用经验。
- 论文提出的问题是：异构记忆是否有帮助、哪些知识能够迁移、以及哪种记忆形式最适合迁移。

## 方法
- 作者提出了 **Memory Transfer Learning (MTL)**：针对目标基准，代理从其他编码基准离线收集的记忆中进行检索，并在推理时将其插入提示中。
- 他们测试了四种抽象层次不同的记忆格式：**Trajectory**（原始动作/观测轨迹）、**Workflow**（筛选出的可复用动作）、**Summary**（任务与事后总结）、以及 **Insight**（刻意避免任务特定细节的一般性经验）。
- 检索使用文本嵌入和余弦相似度；系统针对每个查询从排除目标基准的异构记忆池中选择 top-3 记忆。
- 评估覆盖 6 个编码基准：LiveCodeBench v6、Aider-Polyglot、SWE-Bench Verified、TerminalBench2、ReplicationBench 和 MLGym-Bench，指标为 Pass@3。
- 分析比较了 zero-shot 代理、MTL 各变体，以及 ReasoningBank 和 AgentKB 等已有自演化方法，也检查了不同基础模型之间的迁移效果。

## 结果
- 在 **GPT-5-mini** 上，zero-shot 的平均 **Pass@3 = 0.523**。表现最好的 MTL 变体 **Insight** 达到 **0.560**，在 6 个基准上的平均提升为 **+3.7%**。
- 在 GPT-5-mini 上，**Insight** 在各基准的变化为：**LiveCodeBench 0.910 -> 0.930 (+2.0%)**、**SWE-Bench Verified 0.730 -> 0.770 (+4.0%)**、**TerminalBench2 0.315 -> 0.360 (+4.5%)**、**ReplicationBench 0.111 -> 0.189 (+7.8%)**、**MLGym-Bench 0.667 -> 0.750 (+8.3%)**，以及 **Aider-Polyglot 0.470 -> 0.470 (0.0%)**。
- 跨模型迁移也有帮助：**DeepSeek V3.2** 使用 Insight 后平均分从 **0.542 -> 0.568 (+2.6%)**；**Qwen3-Coder-480B-A35B-Instruct** 从 **0.483 -> 0.501 (+1.8%)**。
- 在三个基准上与已有自演化基线相比，**MTL = 0.630** 平均 Pass@3，而 **ReasoningBank = 0.601**、**AgentKB = 0.613**。论文报告相对 ReasoningBank 提升 **+2.9%**，相对 AgentKB 提升 **+1.7%**。
- 在这组比较中，MTL 使用了 **431 条记忆**，而 **AgentKB** 使用了 **5,899 条记忆**，但 MTL 的得分仍然更高。
- 论文声称，迁移机制主要是 **元知识**，例如检查-编辑-验证流程、验证习惯、小而安全的补丁，以及考虑环境的调试方式。摘要中写道，**算法策略迁移只占增益的 5.5%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14004v1](http://arxiv.org/abs/2604.14004v1)
