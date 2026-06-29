---
kind: ideas
granularity: day
period_start: '2026-05-19T00:00:00'
period_end: '2026-05-20T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent reliability
- code generation
- runtime verification
- multi-agent systems
- code model calibration
tags:
- recoleta/ideas
- topic/agent-reliability
- topic/code-generation
- topic/runtime-verification
- topic/multi-agent-systems
- topic/code-model-calibration
language_code: zh-CN
---

# Agent State Verification

## Summary
Agent 部署正在获得具体的控制点：并行编码代理的写入时状态检查、桌面任务的可执行状态验证器，以及用于选择或延后生成代码的运行时证据。共同模式很简单：记录代理看到的内容，把动作和当前状态对齐检查，并在系统拒绝或转派输出时保留机器可读的原因。

## Versioned write gates for parallel coding agents
在同一个代码仓库里跑多个编码代理的团队，可以在扩展代理数量之前先加一个共享写入闸门。这个闸门为每个文件维护版本计数，记录每个代理读过的文件，并在读集里的任何文件发生变化时拒绝写入。拒绝时应返回当前目标文件、直接 diff，以及所有过期的依赖文件，这样代理就能带着当前上下文重试。

STORM 给出了这个流程的具体设计。它保留一个共享工作区，在每次写入前检查代理的读快照，并用结构化意图注释让附近的代理看出代码为什么变更。在 Claude Sonnet 4.6 上跑 Commit0-Lite 时，STORM 报告的加权通过率是 46.2，宏平均通过率是 82.5；GitWorktree 基线分别是 24.6 / 63.8。一个低成本测试是用隔离 worktree 和带版本的写入闸门分别跑同一批待办，然后比较集成失败、被拒绝的过期写入、重试率和墙钟时间。

### Evidence
- [Multi-agent Collaboration with State Management](../Inbox/2026-05-19--multi-agent-collaboration-with-state-management.md): STORM describes version counters, read snapshots, stale-write rejection, retry context, and benchmark gains over GitWorktree and single-agent baselines.
- [Multi-agent Collaboration with State Management](../Inbox/2026-05-19--multi-agent-collaboration-with-state-management.md): The paper explains why workspace isolation delays semantic conflicts until merge time and motivates write-time state management.

## Application-state verifiers for desktop-agent QA runs
Computer-use 代理需要在运行后检查已保存的应用状态、文件、数据库和设置的 QA 校验。一个实用做法是给每个目标应用做一个小型 verifier 包：Python CLI 端点返回浏览器配置文件、SQLite 数据库、LibreOffice 文档、D-Bus 状态、已保存文件和辅助功能状态的 JSON 检查。每个任务都可以附带初始沙盒状态、用户指令和可执行的成功条件。

OpenComputer 以 33 个桌面应用和 1,000 个任务展示了这种做法，平均每个应用 17.7 个 verifier 端点、每个任务 6.9 个检查。它的提醒同样适用于内部 QA：截图和 LLM 裁判会漏掉元数据或持久副作用中的错误。AgentAtlas 补上了审查时需要的轨迹层：给 Act、Ask、Refuse、Stop、Confirm 和 Recover 这类决策贴标签，并在代理循环、跳过确认、用了错误工具或恢复不好时记录失败类别。第一步可以先把十个常见桌面任务改成沙盒初始化器加可执行检查，然后对比只看截图的审查和 verifier 结果。

### Evidence
- [OpenComputer: Verifiable Software Worlds for Computer-Use Agents](../Inbox/2026-05-19--opencomputer-verifiable-software-worlds-for-computer-use-agents.md): OpenComputer details app-specific verifier modules, real application state inspection, sandboxed task generation, and benchmark scale.
- [OpenComputer: Verifiable Software Worlds for Computer-Use Agents](../Inbox/2026-05-19--opencomputer-verifiable-software-worlds-for-computer-use-agents.md): The source text explains why screenshots can miss file contents, metadata, and persistent side effects.
- [AgentAtlas: Beyond Outcome Leaderboards for LLM Agents](../Inbox/2026-05-19--agentatlas-beyond-outcome-leaderboards-for-llm-agents.md): AgentAtlas provides control-decision labels and trajectory failure categories for reviewing agent runs beyond final task success.

## Fuzzing-based candidate selection before returning generated code
编码助手可以先采样多个候选程序，再在展示给开发者之前运行一个本地选择器。DIFFCODEGEN 给出了一种可落地的版本：生成多样候选，用一个参考候选做 fuzz 来构造输入，在这些输入上执行每个候选，比较输出、错误、返回值、异常和退出码，然后返回最大行为簇的 medoid。

在没有公开测试、而再跑一遍 LLM 评审会增加成本或延迟时，这种方法很有用。论文报告说，选择阶段在初始生成后不需要额外模型调用；在 LiveCodeBench 上，对本地部署的 LLM，它只用此前测试时缩放方法大约 20% 的执行时间；对基于 API 的 LLM，大约是 5%；输入 token 约为前人工作的 4%。对于风险更高的任务，选择器可以接一个 defer 步骤：校准后低置信或低一致性的案例交给编译器检查、静态分析、验证器、提示扩展、任务拆分或人工复核。

### Evidence
- [Code Generation by Differential Test Time Scaling](../Inbox/2026-05-19--code-generation-by-differential-test-time-scaling.md): DIFFCODEGEN describes candidate generation, coverage-guided fuzzing, behavioral comparison, clustering, medoid selection, and reported time/token savings.
- [Code Generation by Differential Test Time Scaling](../Inbox/2026-05-19--code-generation-by-differential-test-time-scaling.md): The source text states why PASS@K does not match real coding assistants that must return one solution.
- [When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions](../Inbox/2026-05-19--when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-code-predictions.md): The defer-and-recover paper describes calibrated thresholds and routes uncertain code outputs to analysis tools or recovery steps.
