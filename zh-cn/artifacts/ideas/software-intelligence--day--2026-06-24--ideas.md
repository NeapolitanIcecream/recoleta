---
kind: ideas
granularity: day
period_start: '2026-06-24T00:00:00'
period_end: '2026-06-25T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- agent harnesses
- tool reliability
- code benchmarks
- test migration
- agent governance
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-harnesses
- topic/tool-reliability
- topic/code-benchmarks
- topic/test-migration
- topic/agent-governance
language_code: zh-CN
---

# 编码代理可靠性测试架

## 摘要
编码代理的采用已经适合转向更窄的测试架工作：分离的 bug 修复角色、围绕不可靠工具的恢复测试，以及面向库行为重叠团队的基于意图的测试迁移。证据最强的部分来自报告可执行评估、测量回归，或通过工作流水线发现真实缺陷的论文。

## 用于 GitHub issue 修复的 Explorer、Patch Editor、Validator 分离工作流
在仓库 issue 上使用编码代理的团队，可以把修复循环拆成三个角色：Explorer 查找文件、函数和调用链；Patch Editor 修改代码；Validator 编写并运行复现测试和回归测试。关键控制点是补丁编写和验证之间的边界。i cat-agent 向 Patch Editor 隐藏测试代码和断言，同时让代理之间传递结构化事件，例如通过/失败结果和可疑语句。

这种做法适合遇到以下问题的团队：代理通过自己编写的弱测试，或在较长的 issue 线程中丢失上下文。可以先做一个小型 issue 质量门禁：如果工单写明文件、函数、修复策略和复现步骤，就直接送入补丁编写和验证；如果缺少这些信息，就先运行探索。在 SWE-bench Pro 上，使用 GPT-5.4-xhigh 的 i cat-agent 解决了 67.4% 的任务，比使用同一模型的 mini-SWE-agent 高 8.3 个百分点。论文还报告，在该基准上它的平均单实例成本低于 Claude Code。

### 资料来源
- [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](../Inbox/2026-06-24--unlocking-model-potentials-through-adaptive-multi-agent-scaffolding-for-efficient-issue-resolution.md): 概述 i cat-agent 的 Explorer、Patch Editor、Validator 角色、隐藏的验证器断言、issue 质量门禁和 SWE-bench 结果。
- [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](../Inbox/2026-06-24--unlocking-model-potentials-through-adaptive-multi-agent-scaffolding-for-efficient-issue-resolution.md): 报告 67.4% 的 SWE-bench Pro 结果和成本比较背景。
- [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](../Inbox/2026-06-24--unlocking-model-potentials-through-adaptive-multi-agent-scaffolding-for-efficient-issue-resolution.md): 说明测试过拟合和补丁过拟合是单代理轨迹中的失败模式。

## 面向编码代理工具调用的可恢复工具故障测试
代理团队应为编码代理调用的工具添加一组本地故障注入测试：仓库搜索、包管理器、CI 日志、issue 跟踪器、内部 API 和 MCP 服务器。每个用例都应保留一条有效恢复路径，例如超时后重试、使用备用命令、归一化变化后的输出、检查第二个来源，或解决相互冲突的证据。

ToolBench-X 给出了一个具体模板。它在可执行的多步骤任务中注入 Specification Drift、Invocation Error、Execution Failure、Output Drift 和 Cross-source Conflict。参与评估的模型没有一个整体准确率达到 0.60，最高分是 0.513。工具响应失败后，代理经常重试同一个工具，但重试频率和任务准确率不一致。有效指标是代理是否诊断出风险并选择正确的恢复动作。小型内部版本可以在 CI 中针对记录下来的工具轨迹运行，并在常见风险上的恢复准确率下降时阻止代理上线。

### 资料来源
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): 概述 ToolBench-X 的任务设计、风险类型、模型准确率、重试行为和定向恢复提示结果。
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): 将 ToolBench-X 定义为带有五类可恢复可靠性风险和有效恢复路径的可执行多步骤任务。
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): 解释真实工具故障，例如过期文档、重命名字段、超时、不完整返回和相互冲突的证据。

## 相似库之间基于意图的单元测试迁移
在相似库之间移植行为的维护者，可以使用面向意图的单元测试迁移流水线。工作流很具体：把源测试拆成更小的子测试，把每个子测试转换成一条 Test Description Language 记录，将意图映射到目标仓库图，收集构造函数和依赖项，生成目标测试，然后运行验证步骤。

这种方法最适合领域重叠但 API 或语言不同的库，例如 JSON、HTML 和 Time 库。IntentTester 评估了九个 Java 和 Python 开源项目。它从 2,058 个源测试生成 5,536 个子测试，过滤后保留 3,257 个。它生成了 2,776 个语法正确的测试，正确率为 85%，相比之下 MUT 为 51%，METALLICUS 为 43%。生成的测试暴露了 25 个真实缺陷，包括栈溢出和空指针解引用 bug。团队可以先在一个源库和一个目标库上试用该方法，再衡量可执行的迁移测试数量和新失败的行为检查。

### 资料来源
- [IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration](../Inbox/2026-06-24--intenttester-intent-driven-multi-agent-framework-for-cross-library-test-migration.md): 概述 IntentTester 的 TDL 转换、仓库图映射、验证循环、评估规模、正确率和发现的缺陷。
- [IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration](../Inbox/2026-06-24--intenttester-intent-driven-multi-agent-framework-for-cross-library-test-migration.md): 说明跨库、跨语言迁移方法使用与语言无关的 Test Description Language 和仓库图上下文。
- [IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration](../Inbox/2026-06-24--intenttester-intent-driven-multi-agent-framework-for-cross-library-test-migration.md): 报告生成的测试数量、85% 正确率、74% 有效性和此前未知的缺陷。
