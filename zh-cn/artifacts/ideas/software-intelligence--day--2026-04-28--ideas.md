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

# 面向编码代理的可执行保护措施

## 摘要
具体的切入点都在模型周边的代码编辑路径上：更窄的读取结果、专门的补丁执行、带测试的修复循环、可版本管理的 harness 变更，以及来自未覆盖代码的排序报告。团队在改变主开发流程之前，都可以先用现有仓库和可执行测试把这些点验证一遍。

## 将文件查看、补丁写入和测试修复拆开处理代码编辑
代码助手团队应该把仓库编辑拆成三个可衡量的步骤：一个只返回与任务相关代码块的查看器，一个应用高层补丁请求的编辑器，以及一个运行真实测试并把结构化失败反馈回修复流程的验证器。对于已经调用文件读取、grep、编辑和测试工具的 IDE 助手、CI 修复机器人和内部编码代理，这是一项可落地的改造。

SWE-Edit 给出了读写拆分的具体做法。它的 Viewer 接收路径和自然语言查询，只返回相关代码块；它的 Editor 接收路径和编辑指令，并应用修改。在 SWE-bench Verified 上，论文报告 resolved rate 从 69.9% 升到 72.0%，edit success 从 93.4% 升到 96.9%，推理成本下降 17.9%。SAFEdit 为带指令的代码编辑加入测试循环：Planner 写编辑计划，Editor 修改代码，Verifier 运行单元测试，最多进行三轮修复。它报告 EditBench 任务成功率为 68.6%，高于 60.0% 的 GPT-4.1 ReAct 基线。

一种低成本的落地测试，是在不改基础模型的情况下给现有编码代理加一层包装。把读取请求路由到返回代码块的查看器，把编辑请求路由到补丁执行器，在每次补丁后运行项目测试，并在固定问题集上比较 edit success、无关 diff 大小、resolved tasks 和 token 成本。Claude Code 的回归报告给出了一条实现层面的警告：Read 和 Grep 结果里反复出现安全提醒，会让子代理拒绝普通重构并浪费上下文。文件读取路径里的安全文本需要单独做回归测试，包括在良性仓库上的并行子代理运行。

### 资料来源
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): SWE-Edit reports the Viewer/Editor split, SWE-bench Verified gains, edit-success gains, and lower inference cost.
- [SAFEdit: Does Multi-Agent Decomposition Resolve the Reliability Challenges of Instructed Code Editing?](../Inbox/2026-04-28--safedit-does-multi-agent-decomposition-resolve-the-reliability-challenges-of-instructed-code-editing.md): SAFEdit reports a Planner/Editor/Verifier loop with real unit tests, repair rounds, and higher EditBench task success than a ReAct baseline.
- [Regression: malware reminder on every read still causes subagent refusals](../Inbox/2026-04-28--regression-malware-reminder-on-every-read-still-causes-subagent-refusals.md): The Claude Code bug report shows that repeated harness text in read results can cause subagent refusals and token waste during normal code-editing workflows.

## 基于 rollout 轨迹的文件级 harness 变更评审
运行编码代理的团队可以把 harness 当作需要评审的代码。把系统提示、工具说明、工具实现、中间件、技能、子代理设置和长期记忆都存成可编辑文件。在基准测试或内部任务 rollout 之后，把轨迹转成任务报告，把每个拟议的 harness 变更和它对应的失败关联起来，记录预期收益和回归风险，然后只在重放验证预测成立后保留这项变更。

Agentic Harness Engineering 给出了这个流程的具体评估方式。它把七类 harness 组件暴露为文件，使用清洗后的 rollout 轨迹生成证据，让 Evolve Agent 编辑 harness 文件，并为每次变更记录一份 manifest。下一轮会检查任务层面的结果，并在文件级回滚被拒绝的编辑。经过 10 轮迭代，论文报告 Terminal-Bench 2 的 pass@1 从 69.7% 升到 77.0%，覆盖 89 个任务。在 SWE-bench-verified 上，冻结后的 harness 在每次试验中使用的 token 少于种子 harness，同时整体成功率相近。

第一批用户是已经有代理轨迹、但通过临时改 prompt 处理 harness 变更的工程团队。最小试点可以从 30 到 100 个代表性任务、一个带版本管理的 harness 文件目录，以及每次 prompt、工具、中间件、记忆或技能修改都必须附带的变更 manifest 开始。通过/失败检查应该包含 token 使用和回归案例，因为 AHE 的消融结果显示收益主要来自记忆、工具和中间件，而只改系统提示的版本表现低于种子配置。

### 资料来源
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](../Inbox/2026-04-28--agentic-harness-engineering-observability-driven-automatic-evolution-of-coding-agent-harnesses.md): AHE describes file-level harness components, rollout evidence, change manifests, outcome checks, reversions, Terminal-Bench 2 gains, SWE-bench-verified transfer, token use, and ablation results.
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](../Inbox/2026-04-28--agentic-harness-engineering-observability-driven-automatic-evolution-of-coding-agent-harnesses.md): The paper states that prompts, tools, middleware, context control, execution, and recovery are model-external harness components and that manual adaptation struggles as models change.

## 来自未覆盖 Python 代码的排序 bug 报告
Python 维护者可以加一个预分诊任务，扫描当前测试覆盖之外的代码，并生成一个供人工审核的、经过排序的小型 bug 报告队列。这个任务应包含覆盖发现、LLM 生成的 issue 报告、复现步骤和建议修复、重新排序，以及对候选补丁的测试运行，这样会破坏现有测试的报告就会降权。

IssueSpecter 给出了这一流程的具体版本。SlipCover 找出未覆盖的 Python 代码段。GPT-5-mini 审查每个代码段，并生成包含严重性、受影响操作系统、复现步骤和建议修复的 issue 报告。筛选步骤保留每个项目的前几条报告，GPT-5-mini 再按影响范围、覆盖范围和紧急程度重新排序。在 13 个活跃的 Python 项目上，系统生成了 10,467 条报告。对 130 条排名靠前报告的人工审查发现了 49 个有效 bug、61 个需要进一步调查的问题和 20 条无效报告。论文报告，LLM 排序在 precision@3 上比规则排序高 50%，在 mean reciprocal rank 上高 41%。

这对测试套件较完整、但仍有持续未覆盖模块的项目最有用，尤其是维护者已经不信任原始 AI issue 洪流时。一个受控试点可以按周运行，默认不公开创建 issue，只把每个仓库排名前 3 的报告发给维护者，并附上覆盖位置、复现步骤、拟议修复和测试结果。评审指标应该是每个维护者小时的有效或可行动报告数，因为这些误报仍然需要人工分诊。

### 资料来源
- [LLM-Guided Issue Generation from Uncovered Code Segments](../Inbox/2026-04-28--llm-guided-issue-generation-from-uncovered-code-segments.md): IssueSpecter describes uncovered-code discovery, structured LLM-generated reports, reranking, test-based demotion, human validation results, and ranking improvements.
- [LLM-Guided Issue Generation from Uncovered Code Segments](../Inbox/2026-04-28--llm-guided-issue-generation-from-uncovered-code-segments.md): The paper reports the false-positive rate, ranking gains, bug-type coverage, and comparison with CoverUp under matched evaluation conditions.
