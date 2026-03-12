---
source: hn
url: https://news.ycombinator.com/item?id=47225418
published_at: '2026-03-02T22:56:56'
authors:
- genesalvatore
topics:
- ai-governance
- autonomous-agents
- deterministic-policy
- llm-safety
- audit-trail
relevance_score: 0.78
run_id: materialize-outputs
---

# Show HN: We filed 99 patents for deterministic AI governance(Prior Art vs. RLHF)

## Summary
这篇内容提出一种用于自治智能体治理的**确定性**架构，目标是替代依赖 RLHF 和提示词的概率式安全方案。核心主张是把 LLM 从“可执行主体”降级为只能产生意图，再由外部确定性策略执行层进行强约束与审计。

## Problem
- 现有自治代理安全主要依赖 **RLHF、system prompt、constitutional training** 等概率式对齐方法，作者认为这类方法在越狱或上下文溢出时会失效。
- 作者强调“统计倾向不是安全边界”：如果模型本身仍握有执行能力，就无法提供可验证、可强制的治理机制。
- 这对自动化代理尤其重要，因为一旦代理能真实调用工具、执行动作或持续运行，失控风险会放大到安全、合规和伦理层面。

## Approach
- 提出 **Deterministic Policy Gates**：LLM 不直接执行任何动作，只能输出一个 **intent payload**（意图载荷）。
- 该 payload 被送入一个 **进程隔离的确定性执行环境**，由外部规则系统而不是模型概率分布来决定是否允许执行。
- 执行环境会将请求与一个 **加密哈希的约束矩阵**（作者称为 constitution）做匹配；若违反约束则直接阻断。
- 每个决策都会记录到 **Merkle-tree substrate（GitTruth）**，形成不可篡改的审计轨迹。
- 作者还声称把**人道主义使用限制**直接写进专利权利要求中，试图从 IP 层面限制其用于自主武器、大规模监控或剥削。

## Results
- 文本**没有提供实验数据、基准测试或量化评测结果**，因此无法验证其在具体数据集、任务成功率、越狱拦截率或性能开销上的效果。
- 最强的具体主张是：作者自 **2026-01-10** 起围绕该架构提交了 **99 项 provisional patents**。
- 论文/帖子声称其方案相较 **RLHF / system prompts / constitutional training** 更接近“真正的安全边界”，因为模型被剥夺执行权，违规意图会被确定性策略层拦截。
- 还声称通过 **Merkle-tree** 日志实现“immutable audit trail”，但未给出吞吐量、存储成本、审计延迟等数字。
- 声称在专利中加入 **Peace Machine Mandate** 以限制特定滥用场景，但未提供法律可执行性或实际约束效果的数据。

## Link
- [https://news.ycombinator.com/item?id=47225418](https://news.ycombinator.com/item?id=47225418)
