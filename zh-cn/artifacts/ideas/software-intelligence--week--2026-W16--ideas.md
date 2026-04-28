---
kind: ideas
granularity: week
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-20T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- verification
- evaluation
- repositories
- agent-operations
tags:
- recoleta/ideas
- topic/coding-agents
- topic/verification
- topic/evaluation
- topic/repositories
- topic/agent-operations
language_code: zh-CN
---

# 软件代理的执行控制层

## Summary
近期最明确的构建方向，是围绕代码代理的运行控制层：在补丁接收前加入硬性的沙箱重放门、让代理执行软件分析搭建并在拿到经过验证的项目证据后停止、以及为企业动作加入类型化动作契约层。每一种都由论文支持，这些论文已经不再停留在流畅的执行轨迹，而是报告了带有可测效果的具体执行、验证或权限机制。

## 用于仓库补丁接收的沙箱重放门
仓库代理可以在接受任何补丁之前加入强制执行门。这个星期的证据已经足够具体，可以支持一个明确的构建方案：在隔离容器里运行每一次拟议编辑，要求 fail-to-pass 测试通过且没有 pass-to-pass 回归，并把真实的 stdout、stderr 和测试失败信息送回修复循环。AgentForge 用这种结构在 SWE-bench Lite 上报告了 40.0% 的问题解决率，运行环境是网络隔离的 Docker sandbox，调试器最多重试三次。和只根据模型输出接受补丁相比，这是一种更强的运行模式。

第一批用户是那些已经在带测试的仓库里尝试代码代理、并看到看似合理的 diff 在 CI 中失败的团队。一个低成本检查可以很聚焦：选一个测试稳定的仓库，在合并前加入硬性的执行要求，再测量有多少代理补丁能在重放后通过且不需要人工清理。如果通过率上升、评审负担下降，这个门就有价值。如果仓库缺少可靠测试，这个流程会很快卡住，所以应当先在执行结果已经有明确约束力的地方开始构建。

### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): 展示了一种代码代理工作流：每次变更都必须先通过沙箱执行才能继续，并给出了基准结果和具体的沙箱约束。
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): 确认了闭环的 Tester–Debugger 设计、实时仓库索引，以及每个补丁都在受限 Docker sandbox 中执行。

## 带基于证据的完成检查的代理式软件分析搭建
采用分析器、模糊测试器、符号执行工具和性能分析器的团队，可以使用一个负责完整“搭建并证明”流程的代理，而不是只生成命令。AnalysisBench 为这种构建给出了明确目标：创建隔离容器、安装工具、构建项目、生成工具特定的前置产物、运行分析，并且只有在运行产出项目特定证据时才停止。AnalysisAgent 在 35 个工具-项目任务上达到了 94% 的验证成功率，而最好的基线是 77%。论文还说明了这层支持为什么重要：自验证仍然高估了成功，对人工验证的假阳性率达到 15%。

实际产品可以是一个面向内部 AppSec 和性能团队的搭建执行器，这些团队常常把时间耗在把工具接入陌生仓库上。最快的验证步骤是挑一个内部最痛苦的分析器部署案例，让代理产出一个可复现环境，再加上一个人类本来就会信任的证据产物，然后把搭建耗时和当前人工流程对比。停止标准必须严格。如果分析器没有产出真实的项目输出，那么一次成功构建或一个 `--help` 界面都不算完成。

### Evidence
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): 提供了基准、验证成功率差距、自验证的假阳性率，以及自动化软件分析的分阶段工作流。
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): 详细说明了常见失败模式，例如过早停止和错误定位不准，这些都支持基于证据的完成判定层。

## 用于企业代理执行的类型化动作契约层
企业里的编码和运维代理需要一层执行层：只暴露当前用户有权运行的类型化动作，在产生副作用前验证输入，并通过应用自身的服务来执行。两篇论文都指向同一个采用障碍。对 Claude Code 代码库的分析显示，它的大部分复杂度都在权限模式、上下文压缩、hooks 和围绕简单模型循环的工具控制上。BAL 报告称，类型化动作契约、运行时权限过滤、工作区范围控制和审批门在 25 个企业场景中完成了 23 个，而且 unsafe execution 为零；没有约束的配置只完成了 17 个。

一个明确的构建方向是为部署、工单变更、用户管理和数据导出这类高风险动作建立契约注册表。每个动作定义都需要输入 schema、permission predicate、validation function、execution callback 和结果格式。第一批买方是那些因为不敢让代理接触生产系统而卡住的团队。最低成本的测试方式是包装一小组现有内部动作，重放已知的坏案例，尤其是错误实体编辑和跨工作区请求，看看契约层能否在执行前把它们拦住。

### Evidence
- [Bounded Autonomy for Enterprise AI: Typed Action Contracts and Consumer-Side Execution](../Inbox/2026-04-16--bounded-autonomy-for-enterprise-ai-typed-action-contracts-and-consumer-side-execution.md): 展示了类型化动作契约、带权限感知的能力暴露、消费侧执行，以及在受限层下 unsafe execution 为零的企业试验结果。
- [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](../Inbox/2026-04-14--dive-into-claude-code-the-design-space-of-today-s-and-future-ai-agent-systems.md): 说明生产级代码代理的复杂度主要集中在权限、上下文管理、可扩展性和围绕简单代理循环的控制系统。
