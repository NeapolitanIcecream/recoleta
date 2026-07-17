---
kind: ideas
granularity: day
period_start: '2026-07-16T00:00:00'
period_end: '2026-07-17T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent reliability
- evidence gating
- coding agents
- dynamic tools
- domain evaluation
tags:
- recoleta/ideas
- topic/agent-reliability
- topic/evidence-gating
- topic/coding-agents
- topic/dynamic-tools
- topic/domain-evaluation
language_code: zh-CN
---

# 与不断变化的依赖项、工具和工件绑定的执行证据

## 摘要
智能体控制应将成功执行绑定到促成该结果的外部状态：软件包来源和版本、工具架构、领域工作流以及非代码工件。近期最有价值的改动，是设置范围明确的发布和完成门禁，重放真实工作流，并在这些输入发生变化时使证据失效。

## 面向工具调用型智能体工作流的版本绑定发布门禁
智能体平台的发布工程师应让成功工作流的收据不仅标识源代码提交，还应记录执行期间使用的每个软件包来源和版本，以及确切的 MCP 服务器架构。软件包安装实验发现，智能体经常接受不可信的注册表；MCPEvol-Bench 则测得，工具演化后，两个前沿模型的任务性能分别下降了 13.7% 和 14.4%。Proof-or-Stop 展示了如何在生命周期证据过期或脱离受跟踪状态时拒绝该证据，但其当前评估尚未证明能够覆盖不断变化的外部工具。

发布门禁可以针对已锁定版本和候选依赖项/工具版本，重放一小组高价值工作流；在安装前运行确定性的软件包来源检查；并为代码提交、注册表身份、依赖锁文件、MCP 架构和测试输出签发收据。任何输入发生变化，都应使之前的收据失效。成本最低且有实际价值的检查，是在现有发布测试套件中修改一个注册表 URL 和一个 MCP 参数，验证门禁会阻止复用旧证据，并定位失败步骤。

### 资料来源
- [Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents](../Inbox/2026-07-16--setup-complete-now-you-are-compromised-weaponizing-setup-instructions-against-ai-coding-agents.md): 基于来源的软件包攻击在多个生态中都曾被漏检；对软件包名称、来源和版本进行确定性检查，弥补了大部分已观察到的差距。
- [MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers](../Inbox/2026-07-16--mcpevol-bench-benchmarking-llm-agent-performance-across-dynamic-evolutions-of-mcp-servers.md): GPT-5.4 和 Claude-Sonnet-4-6 在演化后的 MCP 服务器上，任务性能分别下降了 13.7% 和 14.4%。
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): 经过测试的生命周期门禁在 10 个场景中产生了零次 false-done 结果，并拒绝了 18 类收据篡改；评估范围仅限于一个模型系列和一个自托管语料库。

## AI/ML 维护问题的工件完整性关闭检查
AI/ML 仓库的维护者应在问题被标记为已解决前，要求工作流记录检查或修改过的提示词、数据集、模型设置、依赖项、运行时配置和源文件，并为每个受影响的工件附上相应的验证结果。一项涵盖四个 AI/ML 项目的研究发现，64 个 AI/ML 问题中有 28 个需要修改生产代码之外的内容。StructureClaw 的另一项研究发现，在结构工程基准中，要求模型、验证记录、求解器输出、检查结果和报告组成相互关联且可执行的证据链后，平均工作流成功率从 56.8% 提升到 88.6%。

实际改动可以是：使用问题模板和关闭门禁，在诊断期间建立工件影响清单；将工件哈希和执行条件带入重复测试或统计测试；当受影响工件没有当前验证记录时拒绝关闭问题。这样可以把可执行证据链扩展到维护工作中，因为代码测试通过时，提示词、数据集或运行时配置仍可能没有变化。低成本试点可以将该清单回溯应用于近期关闭的模型行为问题，并统计记录的修复方案遗漏某个工件的频率，再与拉取请求或复现步骤中后来识别出的工件进行比对。

### 资料来源
- [Rethinking Issue Resolution for AI/ML Systems](../Inbox/2026-07-16--rethinking-issue-resolution-for-ai-ml-systems.md): 这项定性研究发现，100 个来自四个项目的问题涉及跨阶段实验，以及对数据集、提示词和模型配置的协调修改。
- [StructureClaw: Traceable LLM Agents and an Executable Benchmark for Structural Engineering Workflows](../Inbox/2026-07-16--structureclaw-traceable-llm-agents-and-an-executable-benchmark-for-structural-engineering-workflows.md): 当基准要求采用受治理、以工件为中心的工作流时，平均成功率从 56.8% 提升到 88.6%。
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): Proof-or-Stop 将生命周期转换绑定到针对确切受跟踪源状态的新鲜证据，同时明确不声称能够证明语义正确性。

## 覆盖 API 和工具演化的支付集成回归测试套件
为编码智能体提供技能的支付 SDK 团队，应为每项技能发布可执行的回归用例，覆盖签名验证、异步通知、幂等性、退款和业务状态一致性，然后在旧版和候选版 API 或 MCP 工具版本上重新运行这些用例。Alipay-PIBench 发现，官方集成技能使平均评分标准通过率提高了 10.31 个百分点；但 MCPEvol-Bench 表明，工具的新增和修改会破坏智能体此前成功的计划。因此，一项技能可能改善初始实现，却在连接的接口演化后悄然变得不安全。

构建流程应将技能、工具架构和领域评分标准一起进行版本管理。确定性的端到端检查应决定是否发布；对于产品适配性或语义状态一致性等由 LLM 评判的属性，应针对发生变化的集成，使用新的人类标注进行校准，而不是沿用旧版本的校准结果。Kaleidoscope 的试点规模太小，无法广泛验证这一设计，但它提供了具体的校准方法，并警告说，在同一个评判提示中合并多个评分维度会降低性能。

### 资料来源
- [Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents](../Inbox/2026-07-16--alipay-pibench-a-realistic-payment-integration-benchmark-for-coding-agents.md): 在 6 个模型和 18 个任务中，官方技能使平均评分标准通过率提高了 10.31 个百分点；高级检查覆盖幂等性、异常交易、退款保护和资金安全。
- [MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers](../Inbox/2026-07-16--mcpevol-bench-benchmarking-llm-agent-performance-across-dynamic-evolutions-of-mcp-servers.md): 工具演化增加了规划和推理失败，其中新增和修改造成的性能损失最大。
- [Project Kaleidoscope: Contextual, Human-Aligned Evaluation for Real-World AI Applications](../Inbox/2026-07-16--project-kaleidoscope-contextual-human-aligned-evaluation-for-real-world-ai-applications.md): Kaleidoscope 使用人工审阅的标签校准特定于应用的自动评判器；其证据来自涵盖四个用例的早期三周试点。
