---
kind: trend
trend_doc_id: 1820
granularity: day
period_start: '2026-07-09T00:00:00'
period_end: '2026-07-10T00:00:00'
topics:
- agent harnesses
- test-time adaptation
- long-horizon evaluation
- repository verification
- small language models
run_id: materialize-outputs
aliases:
- recoleta-trend-1820
tags:
- recoleta/trend
- topic/agent-harnesses
- topic/test-time-adaptation
- topic/long-horizon-evaluation
- topic/repository-verification
- topic/small-language-models
language_code: zh-CN
---

# 可执行 harness 已开始决定 agent 的成本、可靠性和测试时增益

## Overview
Agent 的性能越来越取决于模型周围的可执行控制层。TTHE 通过根据无标签轨迹编辑 harness 来改进固定的大语言模型（LLM），Long-Horizon-Terminal-Bench 则显示了当前 agent 在持续终端工作中的性能会多快下降。仓库级检查补足了这一点：实用的 agent 需要自适应控制、密集评估和结构验证。

## Clusters

### 自适应 agent harness
Harness 正在成为优化目标。TTHE 使用运行时错误、工具输出、公开测试和其他无标签轨迹，对可执行控制程序进行分支和编辑。使用 DeepSeek-V4-Flash 时，BIRD 准确率从 12.0% 提升到 50.0%，SWE-bench Verified 从 20.0% 提升到 35.0%。这些增益具有传导性，不完善的代理信号仍可能导致选择错误。

自动化 harness 适配也改变了部署成本。在 21 个任务-模型组合中，优化后的 harness 改进了其中 16 个，并在其中 7 个组合中缩小了小语言模型（SLM）的差距。表现最好的 SLM agent 达到了前沿 LLM 性能的 89.7%，成本仅为其 4%。另一项企业研究将来源、路由、输出和轨迹要求编码为代码；270 次模型边界运行全部通过这些契约，而外接式护栏降低了测得的效用。

#### Evidence
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): 记录了 TTHE 基于轨迹的 harness 编辑、基准测试增益、传导式设置以及代理选择的局限性。
- [Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation](../Inbox/2026-07-09--better-harnesses-smaller-models-building-90-cheaper-agents-via-automated-harness-adaptation.md): 提供了自动化 harness 适配在业务任务中的结果，包括成本和性能数据。
- [From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents](../Inbox/2026-07-09--from-prompts-to-contracts-harness-engineering-for-auditable-enterprise-llm-agents.md): 支持由代码管理的契约、270 次运行的评估以及护栏效用对比。

### 长时程终端评估
Long-Horizon-Terminal-Bench 使用 46 个容器化任务和密集的子任务奖励来衡量持续执行能力。每次运行平均使用 990 万个 token，包含 231 个回合，耗时 85.3 分钟。测试中表现最强的模型在 0.95 奖励阈值下完成了 7 个任务。在所有模型中，平均通过率为 4.3%，超时导致了 79% 的未解决运行。

密集评分揭示了失败过程中的差异。690 次运行中有 433 次获得部分奖励，其中 180 次的奖励达到或超过 0.5。有 73 次运行接近完成，而完全通过的运行有 30 次。这些数据让开发者能够了解最终状态评分所掩盖的进展、停滞和验证失败。

#### Evidence
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): 包含基准测试范围、资源使用量、通过率、部分奖励分布和超时分析。

### 仓库上下文与结构一致性
仓库级编码需要与待实现过程相匹配的上下文。ProjAgent 会检索计算步骤相似的函数，即使它们的词汇和应用领域不同，然后使用编译器和静态分析反馈进行修复。该方法在 REPOCOD 上报告了 41.14% 的 Pass@1，但现有证据没有量化其相对于检索基线的优势。

代码生成完成后，还需要检查整个仓库范围内的不变量。Patchwork Problem 将导入、调用、依赖、配置、模式、资源、控制流和路由建模为相互协调的图。该研究涵盖 336 次生成，并在 43 个真实世界的 AI 生成仓库上验证了这些失败类别。论文提供的摘录没有报告精确率、召回率或数值失败率，因此现有证据支持的最主要贡献是验证器的覆盖范围和分类体系。

#### Evidence
- [ProjAgent: Procedural Similarity Retrieval for Repository-Level Code Generation](../Inbox/2026-07-09--projagent-procedural-similarity-retrieval-for-repository-level-code-generation.md): 支持过程检索、基于静态分析的修复以及报告的 REPOCOD 结果。
- [The Patchwork Problem in LLM-Generated Code](../Inbox/2026-07-09--the-patchwork-problem-in-llm-generated-code.md): 支持八类仓库图、评估范围、外部验证和报告限制。
