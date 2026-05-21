---
kind: ideas
granularity: day
period_start: '2026-05-10T00:00:00'
period_end: '2026-05-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI coding agents
- software testing
- tool use
- agent monitoring
- security
- maintenance cost
- smart contracts
- tool provenance
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/software-testing
- topic/tool-use
- topic/agent-monitoring
- topic/security
- topic/maintenance-cost
- topic/smart-contracts
- topic/tool-provenance
language_code: zh-CN
---

# 代理故障模式关卡

## Summary
代理软件工作正在转向针对具体故障模式的检查：实时工具调用可能返回看似合理的错误答案，监控器可能只用狭窄攻击集测试，C/C++ 库的顺序测试可能漏掉共享内存交互。实际做法是在这些工作流周围加入小型关卡，再让代理接触生产系统或安全关键代码库。

## 代码模式工具使用代理的执行前契约检查
使用代码模式代理调用实时工具的团队，可以在第一次环境动作之前增加一次验证。验证器应读取任务指令和工具注册表，然后检查生成程序的输出形状、工具选择、调用签名、参数来源和调用顺序。检查失败时，应给出具体修复指令，并在不执行工具调用的情况下重新生成。

RubricRefine 是一个有用模板，因为它针对的是不会触发运行时异常但仍会失败的情况：路由错误、工具之间的数据流断裂，以及用错误中间值拼出的看似有效的最终答案。在 M3ToolEval 上，它报告七个模型的平均成功率为 0.86，单次通过的 CodeAct 为 0.62；细化期间没有执行尝试。第一次内部测试应使用多步任务，其中一次错误的实时调用可能改变状态、花费资金、触发速率限制或暴露数据。

### Evidence
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): RubricRefine 定义了针对任务和注册表的执行前检查，并报告在 M3ToolEval 上成功率从 0.62 提高到 0.86。
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): 论文解释了为什么在执行后重试代价高：工具调用可能改变外部状态，或受到速率限制、付费要求或安全约束。

## 用更广的攻击轨迹刷新编码代理监控器的红队测试
编码代理的监控器评估应包含可重复的攻击生成步骤，不能只使用一组固定的直接提示。安全团队可以构建一个小型流水线，把攻击策略、沙箱执行和事后轨迹细化分开处理，然后只保留副任务成功且轨迹仍符合策略的攻击。

MonitoringBench 说明了这对部署前测试的意义。直接诱导 Opus 4.6 会收缩到狭窄的攻击分布，81% 的攻击落入五个技术层级中的两个。经过分类法引导的生成和细化后，Opus 4.5 全轨迹监控器对直接诱导的 Opus 攻击的捕获率为 94.9%，对最佳细化攻击的捕获率降至 60.3%。该攻击集包含具有实际操作相关性的破坏行为，例如防火墙后门、sudo 权限提升、凭据外泄和恶意软件下载。

### Evidence
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): MonitoringBench 描述了分类法、策略/执行/细化的拆分，以及在更强攻击下捕获率下降的结果。
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): 摘要说明了半自动红队方法和包含 2,644 条轨迹的 BashArena 基准。
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): 论文描述了直接诱导攻击中的模式坍缩，并警示高监控器分数可能来自较弱的红队测试。

## 面向 C/C++ 库的共享内存访问对测试驱动
C/C++ 库维护者可以把代理生成的测试对准共享内存访问对，从而提高测试效果。工作流很具体：用静态分析找出公开入口点、共享变量、共享内存访问位置和冲突访问对；从目标访问向后追踪，找到能到达该访问的输入和对象状态；生成多线程驱动；在 ThreadSanitizer 等动态分析器下运行；把未覆盖的访问对和构建失败反馈给下一轮生成。

ConCovUp 在九个真实 C/C++ 库上报告了这种模式，这些库合计约 1,000 kLoC。它把平均 Shared Memory Access Pair Coverage 从 Claude Code 基线的 36.6% 提高到 68.1%。报告的增益是并发交互覆盖率提升，并不声称每个新测试都会发现缺陷。因此，低成本采用检查是在一个库上测量新增 SMAP 覆盖率和 ThreadSanitizer 发现，再决定是否加入常规 CI。

### Evidence
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): ConCovUp 结合静态共享访问分析、反向路径推理、多线程驱动生成和执行反馈，并给出 SMAP Coverage 从 36.6% 到 68.1% 的结果。
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): 论文指出，TSan 等动态工具需要能在运行时到达关键共享内存交互的测试驱动。
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): 引言解释了为什么顺序单元测试会漏掉开源库中的内部同步交互。
