---
kind: trend
trend_doc_id: 1872
granularity: week
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-13T00:00:00'
topics:
- coding agents
- agent harnesses
- software verification
- long-horizon evaluation
- repository workflows
- context engineering
run_id: materialize-outputs
aliases:
- recoleta-trend-1872
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-harnesses
- topic/software-verification
- topic/long-horizon-evaluation
- topic/repository-workflows
- topic/context-engineering
language_code: zh-CN
---

# 可执行控制与验证正在决定编码智能体的上限

## 概览
本周，编码智能体的进展取决于大语言模型（LLM）周围的控制层，包括可执行 harness、运行时检查和仓库工作流。TTHE 在模型权重冻结的情况下取得了较大提升，长时域评测则暴露出严重的任务完成限制。产品设计采用了类似的控制措施，但对比证据仍然有限。

## 研究发现

### 自适应 harness 与长时域评测
测试时 Harness 演进（TTHE）使用无标签执行轨迹改写并选择可执行的控制程序。在 DeepSeek-V4-Flash 上，模型权重保持不变时，SWE-bench Verified 性能从 20.0% 提升到 35.0%，BIRD 从 12.0% 提升到 50.0%。该方法仍依赖不完美的代理信号，也可能选中较弱的 harness。

Long-Horizon-Terminal-Bench 展示了剩余的运行限制。在 46 个容器化任务中，智能体平均每项任务使用 990 万个 token，耗时 85.3 分钟。测试中最强的模型在 0.95 奖励阈值下只完成了 15.2% 的任务，超时占未解决运行的 79%。密集的子任务评分揭示了部分进展，也比单一最终通过率为 harness 设计者提供了更有用的失败证据。

#### 资料来源
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): 介绍 TTHE 方法、基准测试提升、冻结权重设置和代理信号选择的局限。
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): 提供任务规模、token 和运行时间成本、通过率、密集评分结果以及超时频率。

### 可执行规范与配对验证
仓库任务正在产生更有用的中间产物。ReProAgent 通过缺陷定位、根因分析、仓库检索和运行时验证，将 issue 报告转换为从失败到通过的复现测试。它在 SWT-bench-lite 上复现了 58.43% 的 issue，在 SWT-bench-verified 上复现了 70.30% 的 issue，平均每个案例成本为 0.14 美元。

DualVeri 将可复用的属性模板应用于 Apache Spark，并使用 Lean 4 证明和针对 PySpark 的基于属性的测试同时检查每个属性。模板使证明合成成功率平均提高 1.6 倍，将证明幻觉减少 59%，并使测试合成成本平均降低 3.8 倍。证明与测试之间的不一致还暴露了形式化模型和运行中实现之间的差距。

#### 资料来源
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): 说明 ReProAgent 的分阶段方法、复现率和平均成本。
- [Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing](../Inbox/2026-07-10--agentic-proof-and-property-based-testing-via-property-templates-in-data-intensive-computing.md): 详细说明 DualVeri 的证明与测试配对设计，以及在 400 个属性上的测量改进。

### 上下文、工作流与成本控制
运维工具正在让智能体的输入和操作在部署前变得可检查。ContextOps 静态检查上下文冗余度、密度、结构和来源集中度，并提供命令行和持续集成（CI）门禁。其公开示例估算可节省 12% 的 token，但项目没有报告准确率或误报率对比。

OneDev 将智能体置于 issue、隔离工作区、拉取请求、评审和 CI 流程中。Avriz 将影子评测、流量上限和模型等级上限应用于一个学习型路由器，该路由器面对 12 倍的输出 token 价格差。这些设计明确了有用的控制措施，但两个来源都没有提供相对于基线的总体质量或成本收益。生产设计走在证据前面。

#### 资料来源
- [ContextOps, an ESLint-like static analyzer for LLM context](../Inbox/2026-07-11--contextops-an-eslint-like-static-analyzer-for-llm-context.md): 描述确定性的上下文检查、CI 集成、示例节省量以及缺少对比验证的问题。
- [OneDev AI: Coding Agents as Teammates in Issues, Pull Requests, and CI](../Inbox/2026-07-12--onedev-ai-coding-agents-as-teammates-in-issues-pull-requests-and-ci.md): 记录从 issue 到拉取请求的智能体集成、受控工作区以及缺少测量评估的问题。
- [We taught our platform to learn its own pricing decisions](../Inbox/2026-07-12--we-taught-our-platform-to-learn-its-own-pricing-decisions.md): 提供学习型路由设计、12 倍价格差、部署门禁以及缺少总体结果指标的信息。
