---
kind: ideas
granularity: week
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent harnesses
- software verification
- long-horizon evaluation
- repository workflows
- context engineering
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-harnesses
- topic/software-verification
- topic/long-horizon-evaluation
- topic/repository-workflows
- topic/context-engineering
language_code: zh-CN
---

# 编码代理工作流中的可执行反馈

## 摘要
编码代理团队可以通过要求提供可执行的缺陷复现、针对保留任务测试控制程序修改，并利用实时覆盖率信号监督测试生成，来改进仓库工作。每项改动都可以在固定模型上试点，并与当前流程进行衡量。

## 在问题接收阶段加入失败后通过的复现测试
使用修复代理的维护团队应在生成补丁前加入复现阶段。该阶段应定位疑似缺陷、检索仓库上下文、生成测试，并在受影响的版本上执行测试。ReProAgent 在 SWT-bench-lite 中复现了 58.43% 的问题，在 SWT-bench-verified 中复现了 70.30% 的问题，平均每个案例成本为 $0.14；生成的测试还提升了后续修复效果。

可以用 50 个已有已知修复方案的已关闭问题开展试点。只有当生成的测试在修复前的提交上失败、在记录的修复后通过时，才接受该测试；随后将补丁成功率、维护者审查时间和错误复现率与现有修复代理流程进行比较。通过这项检查的团队，可以要求问题中包含可执行的复现产物，再启动自主修复流程。

### 资料来源
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): 报告了 ReProAgent 的复现率、运行时验证、平均成本和对后续修复的收益。
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): 将失败后通过的测试定义为可执行规范：测试在有缺陷的代码上失败，在参考修复后通过。

## 基于执行轨迹的控制程序试验与保留仓库检查
运行编码代理的团队应将可执行控制程序与模型分开进行版本管理，并在影子运行器中测试拟议的控制程序修改。每次试验都可以重放近期执行轨迹，调整上下文构建、工具使用规则、验证步骤或故障恢复逻辑；只有候选版本通过保留的仓库任务并满足成本限制后，才应将其投入使用。

TTHE 在模型权重冻结的情况下展示了这类改进的幅度：在 DeepSeek-V4-Flash 上，SWE-bench Verified 的结果从 20.0% 提升到 35.0%。论文记录的选择遗憾和评审错误也说明了部署时需要保留任务进行检查。Long-Horizon-Terminal-Bench 提供了一种有用的评估设计：在运行过程中持续评估可执行子任务，并记录超时情况，因为未解决运行中有 79% 以超时结束。低成本试验可以在相同模型、任务集、令牌预算和墙钟时间限制下比较两个控制程序版本，跟踪最终完成率、检查点进度、回归问题和成本。

### 资料来源
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): 描述了可执行控制程序的适应过程、固定模型取得的改进，以及基于不完善代理指标的选择所导致的失败。
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): 报告了密集子任务评分、较低的长时程完成率、资源使用情况和超时比例。

## 面向代理生成单元测试的覆盖率感知监督
使用编码代理生成单元测试的 Java 团队，可以加入一个监督器，在每轮迭代后读取当前行覆盖率、分支覆盖率、遗漏的复杂代码和令牌成本。监督器决定让代理继续常规生成、接收未覆盖路径的程序分析结果，还是停止生成。这种做法针对代理在简单路径上过早结束的问题，也能限制那些没有带来覆盖率提升的重复调用。

Scate 使用了这种模式，并结合上下文老虎机和 MCP 程序分析工具。与无监督代理基线相比，Gemini CLI 的行覆盖率提高了 32.3%，分支覆盖率提高了 30.9%；Claude Code 的两项指标分别提高了 6.0% 和 5.9%。仓库试点应固定模型和令牌预算，再比较分支覆盖率、变异得分、生成测试的维护失败率，以及每个被接受测试的成本。论文没有报告最终绝对覆盖率或统计显著性，因此在扩大采用范围前应先完成这些检查。

### 资料来源
- [SCATE: Learning to Supervise Coding Agents for Cost-Effective Test Generation](../Inbox/2026-07-09--scate-learning-to-supervise-coding-agents-for-cost-effective-test-generation.md): 详细说明了覆盖率感知监督器、它的动作选择，以及两种编码代理的相对覆盖率提升。
- [SCATE: Learning to Supervise Coding Agents for Cost-Effective Test Generation](../Inbox/2026-07-09--scate-learning-to-supervise-coding-agents-for-cost-effective-test-generation.md): 记录了代理在复杂分支上过早停止，以及监督器试图减少的人工监控负担。
