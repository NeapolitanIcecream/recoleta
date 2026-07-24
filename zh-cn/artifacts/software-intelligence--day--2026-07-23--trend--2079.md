---
kind: trend
trend_doc_id: 2079
granularity: day
period_start: '2026-07-23T00:00:00'
period_end: '2026-07-24T00:00:00'
topics:
- "\u7F16\u7801\u667A\u80FD\u4F53"
- "\u667A\u80FD\u4F53\u8BC4\u6D4B"
- "\u53EF\u9760\u6027 harness"
- "\u4EBA\u5DE5\u76D1\u7763"
- "\u795E\u7ECF\u7B26\u53F7\u63A8\u7406"
run_id: materialize-outputs
aliases:
- recoleta-trend-2079
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u667A\u80FD\u4F53"
- "topic/\u667A\u80FD\u4F53\u8BC4\u6D4B"
- "topic/\u53EF\u9760\u6027-harness"
- "topic/\u4EBA\u5DE5\u76D1\u7763"
- "topic/\u795E\u7ECF\u7B26\u53F7\u63A8\u7406"
language_code: zh-CN
---

# 智能体评测触及模糊项目，可靠性机制转移到 harness

## 概览
在过去几天聚焦于编码循环中的可执行反馈之后，今天的证据拓宽了控制面。新的基准测试智能体处理不完整的产品意图和混合型办公任务；可靠性机制则在预先定义的检查点交付记忆、逻辑推理和审查。结果仍处于早期阶段：几项研究缺乏广泛的量化比较，其中一个工作流虽然提升了可审计性，但成本显著增加。

## 研究发现

### 更广泛的编码智能体评测
ICAE-Bench 测试智能体能否澄清不完整的需求并构建代码仓库，而不是解决一个规格完整的编辑任务。其 480 个任务覆盖 12 种语言；在两个 harness 中评测的六个模型仍难以处理隐藏约束、边界情况和长周期集成。

Tencent WorkBuddy Bench 将评测扩展到代码、网页、办公和安全工作。其 260 个任务经过逆向工程和重写，以减少通过网页搜索找回答案的可能性，随后随环境和验证器一同发布，以支持可审计性。由于每个领域采用不同的验证方法，该套件有意不提供单一的聚合分数。总体而言，这些基准表明，任务构造和评估器设计本身就是能力主张的一部分，而不是背景实现细节。

#### 资料来源
- [ICAE-Bench: Evaluating Coding Agents as Interactive Project Builders](../Inbox/2026-07-23--icae-bench-evaluating-coding-agents-as-interactive-project-builders.md): 报告了覆盖 12 种语言的 480 个任务基准，以及模型在隐藏约束、边界情况和长周期集成方面的失败。
- [Tencent WorkBuddy Bench: A Multi-Domain Coding-Agent Benchmark with Contamination-Resistant Task Construction](../Inbox/2026-07-23--tencent-workbuddy-bench-a-multi-domain-coding-agent-benchmark-with-contamination-resistant-task-construction.md): 描述了覆盖四个工作领域的重写任务、抗污染设计以及开放评测包。

### 作为强制基础设施的可靠性
三个系统将关键控制置于模型的自愿行为之外。以线索为锚点的工作记忆会在文件、符号或生命周期事件触发时注入限定范围的事实；在最强的自愿控制条件下，智能体在 114 个回合中没有发起任何记忆调用，而 harness 的交付机制经受住了反复的上下文压缩。Euclid-MCP 将规则推导委托给 Prolog 并返回证明轨迹，但其报告的性能优势缺乏数值基线结果支持。

对于经济理论，pAI-Econ-claude 在不存在自动判定器的环节使用可检查的中间记录、针对性检查门和人工检查点。盲评者在五个匹配任务中有四个更偏好该工作流，但其使用量是基线限额的 4.6 至 18 倍。共同结论是有限的：强制交付和显式检查门提升了可追溯性并有助于拦截错误，但尚不足以证明其能够以低成本实现普遍正确性。

#### 资料来源
- [Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents](../Inbox/2026-07-23--delivery-not-storage-cue-anchored-working-memory-as-a-harness-property-for-coding-agents.md): 报告了 114 个回合中零次自愿记忆操作、确定性交付，以及在 138 次强制压缩恢复中均成功交付。
- [Euclid-MCP: A Model Context Protocol Server for Deterministic Logical Reasoning via Prolog](../Inbox/2026-07-23--euclid-mcp-a-model-context-protocol-server-for-deterministic-logical-reasoning-via-prolog.md): 定义了一个将推导委托给 SWI-Prolog 并公开证明轨迹的 MCP 接口。
- [pAI-Econ-claude: A Gated Human-in-the-Loop Multi-Agent Architecture for AI-Assisted Economic Theory Development](../Inbox/2026-07-23--pai-econ-claude-a-gated-human-in-the-loop-multi-agent-architecture-for-ai-assisted-economic-theory-development.md): 报告了五次盲评比较中的四次胜出、更低的失败严重程度、更高的有用性，以及有限的可审计性结论。
