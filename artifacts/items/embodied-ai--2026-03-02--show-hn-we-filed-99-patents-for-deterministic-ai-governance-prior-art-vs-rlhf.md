---
source: hn
url: https://news.ycombinator.com/item?id=47225418
published_at: '2026-03-02T22:56:56'
authors:
- genesalvatore
topics:
- ai-governance
- agent-safety
- deterministic-policy
- llm-security
- auditability
relevance_score: 0.05
run_id: materialize-outputs
---

# Show HN: We filed 99 patents for deterministic AI governance(Prior Art vs. RLHF)

## Summary
这篇文章提出一种用于自治代理治理的“确定性策略门”架构，主张用可验证、可审计的硬性约束替代 RLHF 等概率式对齐。核心卖点是把 LLM 与真实执行权限彻底分离，并通过确定性规则与不可篡改日志实现治理边界。

## Problem
- 文章认为当前主流 AI 治理主要依赖 **概率式对齐**（如 RLHF、system prompts、constitutional training），在被越狱或上下文溢出时会失效。
- 作者强调“统计倾向不是安全边界”：如果模型仍保有执行能力，仅靠训练出来的行为偏好不足以提供强安全保证。
- 这之所以重要，是因为自治代理一旦具备行动能力，治理失败可能带来高风险后果，如武器化、监控滥用或剥削。

## Approach
- 提出 **Deterministic Policy Gates**：LLM 不再直接执行动作，只能生成一个“intent payload（意图载荷）”。
- 该意图会被送入 **进程隔离的确定性执行环境**，在其中根据一个经 **密码学哈希** 的约束矩阵（相当于 constitution）进行检查。
- 如果意图违反约束矩阵，就会被 **直接阻断**；也就是说，治理逻辑不依赖模型是否“愿意服从”，而依赖外部硬约束是否放行。
- 每一次决策都会记录到一个 **Merkle-tree substrate（GitTruth）** 中，以提供不可篡改的审计轨迹。
- 文章还声称将“人道主义使用限制”直接写入专利权利要求，以在法律/IP 层面对自主武器、大规模监控和剥削用途施加限制。

## Results
- 文中**没有提供标准学术实验、基准数据集或定量指标**，因此无法验证其相对 RLHF 或其他安全框架的性能提升幅度。
- 最明确的量化声明是：作者自 **2026-01-10** 起已提交 **99 项临时专利（provisional patents）**，覆盖该确定性治理架构。
- 文章的核心结果性主张是：与概率式对齐相比，该架构把 LLM 从“可直接执行”降级为“只能提出意图”，从而建立更强的执行安全边界。
- 另一个具体主张是：系统提供基于 **Merkle tree** 的不可变审计日志，用于追踪每次治理决策。
- 还宣称通过将伦理限制写入专利，可在法律层面限制该技术被用于 **autonomous weapons、mass surveillance、exploitation**，但文中未给出执法效果或案例数据。

## Link
- [https://news.ycombinator.com/item?id=47225418](https://news.ycombinator.com/item?id=47225418)
