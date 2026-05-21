---
kind: ideas
granularity: week
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- executable evaluation
- formal verification
- agent security
- tool use
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/executable-evaluation
- topic/formal-verification
- topic/agent-security
- topic/tool-use
language_code: zh-CN
---

# 编码代理信任关卡

## Summary
编码代理的采用需要在正常工程工作中加入证据检查：工具调用的执行前验证器、维护任务的仓库接受规则，以及积压工作的分阶段工单安全测试。共同压力是在真实操作、合并或安全敏感部署前建立可操作的信任。

## 代码模式工具调用的执行前契约检查
让编码代理访问 API、部署工具、工单系统或涉及计费的服务的团队，应在生成的代码和第一次真实调用之间加入一个验证器。验证器应读取任务指令和工具注册表，检查工具选择、输出形状、调用签名、调用顺序和参数来源，然后返回逐项修复反馈。

RubricRefine 报告称，在七个模型上的 M3ToolEval 成功率为 0.86；单次通过的 CodeAct 为 0.62；细化期间不执行环境。一个可行的内部测试是使用 50 个已归档、多工具任务，并配有已知正确轨迹：衡量加入关卡前后的错误工具路由、畸形参数和来源错误。这个关卡最适合用于失败调用会改变外部状态、消耗配额或生成审计事件的场景。

### Evidence
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): RubricRefine 在执行前检查工具契约，覆盖工具选择、输出形状、调用签名、顺序和数据来源，并报告在 M3ToolEval 上的平均成功率为 0.86，而 CodeAct 为 0.62。
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): 论文摘要指出，工具间契约失败可能在没有运行时错误的情况下执行完成，这支持在真实调用前加入验证器。

## 面向问答、测试、重构和无变更工单的仓库代理接受检查
维护代理需要 PR 接受规则，覆盖代码库理解、测试质量、重构卫生和有效放弃。SWE Atlas 评估了 18 个活跃仓库中的 284 个任务，并显示回归测试可能漏掉 15 到 40 分的重构质量；测试编写的变异检查会漏掉 10 到 15 分的评分规程质量。FixedBench 补充了生产环境中的过期报告场景：在主要设置下，代理在 35% 到 65% 的已修复案例中编辑了代码；放弃提示在部分修复任务上导致了较高的错误放弃率。

一个有用的工作流是要求证据清单，列出运行过的命令、检查过的文件、添加的测试、重构的行为保持理由，以及一个与复现和 git 历史证据绑定的无代码变更选项。在允许自主合并权限之前，先用近期重复工单和部分修复工单试运行。

### Evidence
- [SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution](../Inbox/2026-05-08--swe-atlas-benchmarking-coding-agents-beyond-issue-resolution.md): SWE Atlas 覆盖 18 个仓库中的代码库问答、测试编写和重构，并报告功能检查与工程质量评分规程检查之间存在差距。
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench 测试已修复问题和部分修复，显示代理会在已修复任务上进行不必要编辑，并在部分修复任务上错误放弃。

## 面向编码代理积压工作的分阶段工单安全测试
只用直接有害提示测试编码代理的安全团队，会漏掉 MOSAIC-Bench 展示的 Jira 式攻击路径。它使用 199 条三工单链，并在 Docker 部署上用确定性的 Python 概念验证预言机进行检查；九个生产代理的端到端攻击成功率达到 53.3% 到 85.9%，且只有两次拒绝。

添加一个回归套件：让代理针对一次性应用处理一系列看起来无害的工单，组合 diff，并在最终部署上运行漏洞利用预言机。再配套使用细化攻击轨迹的监控测试：MonitoringBench 显示，一个全轨迹 Opus 4.5 监控器在诱导攻击上的捕获率为 94.9%，但在最佳细化攻击上降至 60.3%。首要目标是任何允许代理实现积压事项、且没有安全工程师审查累计 diff 的团队。

### Evidence
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench 评估分阶段三工单攻击链，使用确定性的概念验证预言机，并报告生产编码代理的端到端攻击成功率很高。
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): MonitoringBench 显示，更强的细化攻击轨迹会显著降低监控器捕获率，因此需要更新监控测试，不能只依赖直接诱导。
