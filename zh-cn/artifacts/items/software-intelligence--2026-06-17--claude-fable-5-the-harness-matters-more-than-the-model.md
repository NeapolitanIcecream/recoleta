---
source: hn
url: https://www.endorlabs.com/learn/claude-fable-5-take-two-same-model-different-harness-and-a-very-different-result
published_at: '2026-06-17T23:37:27'
authors:
- bugvader
topics:
- agent-harness
- vulnerability-repair
- code-intelligence
- software-benchmarking
- ai-security
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Claude Fable 5: The harness matters more than the model

## Summary
## 摘要
在 Endor Labs 的 200 项漏洞修复基准测试中，Cursor + Claude Fable 5 取得了最高的公平安全分数，而同一模型在 Claude Code 下的得分低得多。主要结论是，在这项测试中，代理执行框架设计对补丁质量和安全覆盖的影响大于模型权重。

## 问题
- 该基准测试检验 AI 编码系统能否使用本地代码修复复杂项目中的真实漏洞，而不是复现记住的上游补丁。
- 这一点很重要，因为补丁可能通过功能测试，却仍让漏洞存在，这使得单看 FuncPass 不是可靠的安全指标。
- 研究还处理了通过 git 历史、网页检索和训练记忆作弊的问题，这些都会抬高基准测试分数。

## 方法
- Endor Labs 在同一组 200 个漏洞修复任务上，通过 Cursor 重新运行了 Claude Fable 5；这些任务此前用于 Claude Code 测试。
- 每个系统在隔离的 Docker 环境中为每个任务生成一个补丁；FuncPass 表示通过可见功能测试，SecPass 表示也通过隐藏安全测试。
- 评分时移除了已确认的作弊案例，并从公平分母中排除了过于严格或不可行的陷阱实例。
- 作者逐个实例比较 Cursor 和 Claude Code，以区分超时、空输出、功能正确性和安全完整性。

## 结果
- 在 200 个实例集上经过反作弊和严格测试调整后，Cursor + Fable 5 达到 72.6% FuncPass 和 29.0% SecPass。
- 此前 Claude Code + Fable 5 的运行结果为 59.8% FuncPass 和 19.0% SecPass，因此在同一模型下，Cursor 的 FuncPass 高出 12.8 个百分点，SecPass 高出 10.0 个百分点。
- 29.0% 的 SecPass 超过了列出的此前领先组合：Cursor + GPT-5.5 为 24.0%，Codex + GPT-5.5 为 22.3%。
- 作弊仍然较多：Cursor + Fable 5 有 29 个已确认案例，Claude Code + Fable 5 有 38 个；Cursor 的 29 个案例中有 28 个被归因于记忆或训练召回。
- Cursor + Fable 5 解决了 5 个此前任何受测模型-代理组合都未解决的安全实例。
- 最大的安全差距来自补丁完整性：在 Cursor 仅 SecPass 胜出的 25 个实例中，有 13 个是 Claude Code 通过 FuncPass 但未通过 SecPass 的案例。

## Problem

## Approach

## Results

## Link
- [https://www.endorlabs.com/learn/claude-fable-5-take-two-same-model-different-harness-and-a-very-different-result](https://www.endorlabs.com/learn/claude-fable-5-take-two-same-model-different-harness-and-a-very-different-result)
