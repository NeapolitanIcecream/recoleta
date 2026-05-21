---
kind: ideas
granularity: day
period_start: '2026-04-28T00:00:00'
period_end: '2026-04-29T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- code editing
- agent harnesses
- software testing
- agent infrastructure
- model efficiency
tags:
- recoleta/ideas
- topic/coding-agents
- topic/code-editing
- topic/agent-harnesses
- topic/software-testing
- topic/agent-infrastructure
- topic/model-efficiency
language_code: zh-CN
---

# 编码智能体的可执行防护措施

## Summary
具体机会在模型周围的代码编辑路径中：更窄的读取结果、专用补丁执行、由测试支撑的修复循环、带版本管理的 harness 变更，以及来自未覆盖代码的排序报告。团队可以先用现有仓库和可执行测试检查这些做法，再改变主要开发者工作流。

## 把代码编辑拆成文件查看、补丁编写和测试修复
代码助手团队应把仓库编辑拆成三个可度量步骤：查看器只返回与任务相关的代码块，编辑器执行高层补丁请求，验证器运行真实测试，并把结构化失败信息反馈给修复流程。对于已经调用文件读取、grep、编辑和测试工具的 IDE 助手、CI 修复机器人和内部编码智能体，这是一项可以落地的改动。

SWE-Edit 给出了读写拆分的实际形态。它的 Viewer 接收路径和自然语言查询，然后返回相关代码块；它的 Editor 接收路径和编辑指令，然后应用变更。在 SWE-bench Verified 上，论文报告解决率从 69.9% 升至 72.0%，编辑成功率从 93.4% 升至 96.9%，推理成本下降 17.9%。SAFEdit 为按指令编辑加入测试循环：Planner 编写编辑计划，Editor 修改代码，Verifier 运行单元测试，最多进行三轮修复。它报告的 EditBench 任务成功率为 68.6%，高于 60.0% 的 GPT-4.1 ReAct 基线。

一个低成本的采用测试是，在不更换基础模型的情况下包装现有编码智能体。把读取请求路由到返回代码块的查看器，把编辑请求路由到补丁执行器，每次补丁后运行项目测试，并在固定问题集上比较编辑成功率、无关 diff 大小、已解决任务数和 token 成本。Claude Code 回归报告给出了一条实现警告：Read 和 Grep 结果中反复出现的安全提醒会让子智能体拒绝普通重构，并浪费上下文。文件读取路径里的安全文本需要自己的回归测试，包括在良性仓库上并行运行子智能体。

### Evidence
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): SWE-Edit 报告了 Viewer/Editor 拆分、SWE-bench Verified 收益、编辑成功率提升和更低的推理成本。
- [SAFEdit: Does Multi-Agent Decomposition Resolve the Reliability Challenges of Instructed Code Editing?](../Inbox/2026-04-28--safedit-does-multi-agent-decomposition-resolve-the-reliability-challenges-of-instructed-code-editing.md): SAFEdit 报告了带有真实单元测试和修复轮次的 Planner/Editor/Verifier 循环，并且 EditBench 任务成功率高于 ReAct 基线。
- [Regression: malware reminder on every read still causes subagent refusals](../Inbox/2026-04-28--regression-malware-reminder-on-every-read-still-causes-subagent-refusals.md): Claude Code 缺陷报告显示，在读取结果中反复加入 harness 文本会在正常代码编辑流程中导致子智能体拒绝任务并浪费 token。

## 基于 rollout 轨迹的文件化 harness 变更评审
运行编码智能体的团队可以把 harness 当作需要评审的代码。把系统提示、工具描述、工具实现、中间件、技能、子智能体设置和长期记忆存为可编辑文件。在一次基准测试或内部任务 rollout 后，将轨迹转换为任务报告，把每个 proposed harness 变更关联到它要处理的失败，记录预期收益和回归风险，然后只在重放证明预测成立后保留该变更。

Agentic Harness Engineering 为这个流程提供了具体评估。它把七类 harness 组件暴露为文件，使用清理后的 rollout 轨迹生成证据，让 Evolve Agent 编辑 harness 文件，并为每项变更记录 manifest。下一轮迭代会检查任务级结果，并可在文件级回滚被拒绝的编辑。经过 10 次迭代后，论文报告 Terminal-Bench 2 pass@1 在 89 个任务上从 69.7% 升至 77.0%。在 SWE-bench-verified 上，冻结后的 harness 每次试验使用的 token 少于种子 harness，同时达到相近的总体成功率。

第一个用户是已经拥有智能体轨迹、但仍通过临时提示词编辑来处理 harness 变更的工程团队。最小试验可以从 30 到 100 个代表性任务、一个带版本管理的 harness 文件目录，以及每次提示词、工具、中间件、记忆或技能编辑都必须提交的变更 manifest 开始。通过/失败检查应包括 token 使用量和回归用例，因为 AHE 消融发现收益主要来自记忆、工具和中间件，而仅修改系统提示的方案低于种子配置。

### Evidence
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](../Inbox/2026-04-28--agentic-harness-engineering-observability-driven-automatic-evolution-of-coding-agent-harnesses.md): AHE 描述了文件级 harness 组件、rollout 证据、变更 manifest、结果检查、回滚、Terminal-Bench 2 收益、SWE-bench-verified 迁移、token 使用量和消融结果。
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](../Inbox/2026-04-28--agentic-harness-engineering-observability-driven-automatic-evolution-of-coding-agent-harnesses.md): 论文指出，提示词、工具、中间件、上下文控制、执行和恢复是模型外部的 harness 组件，并且随着模型变化，手动适配会变得困难。

## 从未覆盖的 Python 代码生成排序后的缺陷报告
Python 维护者可以增加一个预分诊任务，扫描当前测试覆盖之外的代码，并为人工评审生成一小队已排序的缺陷报告。该任务应包括覆盖率发现、由 LLM 生成且带复现步骤和建议修复的 issue 报告、重新排序，以及对候选补丁的测试运行，让破坏现有测试的报告降低优先级。

IssueSpecter 给出了这个流程的具体版本。SlipCover 查找未覆盖的 Python 代码段。GPT-5-mini 审查每个代码段，并生成带有严重程度、受影响操作系统、复现步骤和建议修复的 issue 报告。一个筛选步骤保留每个项目的靠前报告，GPT-5-mini 再按影响、范围和紧急程度重新排序。在 13 个活跃 Python 项目上，系统生成了 10,467 份报告。人工评审 130 份排名靠前的报告后，发现 49 个有效缺陷、61 个需要进一步调查的问题和 20 个无效报告。论文报告称，基于 LLM 的排序在 precision@3 上比基于规则的排序高 50%，在平均倒数排名上高 41%。

这最适合拥有有意义测试套件且长期存在未覆盖模块的项目，因为这些维护者通常不信任未经筛选的 AI issue 洪流。受控试点可以每周运行，默认不创建公开 issue，只把每个仓库排名前三的报告发给维护者，并附上覆盖位置、复现步骤、建议修复和测试结果。评审指标应是每个维护者小时产生的有效或可行动报告数，因为报告中的误报仍需要严格分诊。

### Evidence
- [LLM-Guided Issue Generation from Uncovered Code Segments](../Inbox/2026-04-28--llm-guided-issue-generation-from-uncovered-code-segments.md): IssueSpecter 描述了未覆盖代码发现、结构化 LLM 生成报告、重新排序、基于测试的降级、人工验证结果和排序改进。
- [LLM-Guided Issue Generation from Uncovered Code Segments](../Inbox/2026-04-28--llm-guided-issue-generation-from-uncovered-code-segments.md): 论文报告了误报率、排序收益、缺陷类型覆盖，以及在匹配评估条件下与 CoverUp 的比较。
