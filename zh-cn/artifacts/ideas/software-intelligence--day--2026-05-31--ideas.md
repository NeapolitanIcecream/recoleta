---
kind: ideas
granularity: day
period_start: '2026-05-31T00:00:00'
period_end: '2026-06-01T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- token efficiency
- workflow automation
- LLM-assisted software
- domain modeling
tags:
- recoleta/ideas
- topic/coding-agents
- topic/token-efficiency
- topic/workflow-automation
- topic/llm-assisted-software
- topic/domain-modeling
language_code: zh-CN
---

# Repository-Scale Coding Agent Governance

## Summary
代码代理的采用正在仓库边界上获得更具体的支持：更小的启动上下文、代码地图、使用日志、明确的工作流文件，以及保护领域词汇的审查做法。具体工作是先把 agent 行为做成可测、可重复，再让团队把它用在更大的代码变更上。

## Repository setup that caps startup context and measures coding-agent token use
使用 Claude Code 或 Cursor 的团队可以把 token 浪费当作仓库卫生问题来处理。agent-stack 给出一个具体做法：在一次初始化里生成 `CLAUDE.md`、`AGENTS.md`、`.claudeignore`、hooks、Cursor rules、skills 和 `.agent-stack/graph.md`，再通过 Stop hook 把使用情况写入 `.agent-stack/usage.jsonl`。

最有用的是代码地图。它会索引源文件和导出符号，这样 agent 可以先查一个紧凑文件，再打开源代码。README 示例声称地图里有 142 个文件和 906 个顶层符号，`CLAUDE.md` 的启动 token 上限是 800，input tokens/day 从 12,340 降到 7,180。那些数字来自项目自己的说法，所以实际采用时最直接的检验方法是：在一个正在使用的仓库里跑一次初始化，保留基线，过一周正常的 agent 工作后对比 input tokens/day。

### Evidence
- [Agent-stack – one command to make any repo token-efficient for Claude Code](../Inbox/2026-05-31--agent-stack-one-command-to-make-any-repo-token-efficient-for-claude-code.md): Summarizes generated repo files, code map, usage logging, and the README token reduction claim.
- [Agent-stack – one command to make any repo token-efficient for Claude Code](../Inbox/2026-05-31--agent-stack-one-command-to-make-any-repo-token-efficient-for-claude-code.md): Shows the setup output with 20 generated files, wired hooks, verified setup, and generated code map.
- [Agent-stack – one command to make any repo token-efficient for Claude Code](../Inbox/2026-05-31--agent-stack-one-command-to-make-any-repo-token-efficient-for-claude-code.md): Describes the code map and the agent behavior of grepping the index before opening source files.

## JSON workflows for coding-agent tasks with explicit branch conditions
有重复多步工作的 agent 团队可以把控制流放进工作流文件里。BotCircuits 把每个 workflow 存成 `.botcircuits/workflows/` 下的 JSON；加载后，这个 workflow 就会变成一个可调用工具。LLM 仍然处理每个 `agentAction`，运行时则按 `start`、`next` 和编译后的分支条件执行。

这适合顺序很重要的任务：发布检查、支持分流、文件生成任务，或在已知条件下必须提前停止的代码库审计。README 给出一个 11 步示例，用 `end_id` 参数控制提前终止，还给出 `/workflow add` 命令，可以在不重启的情况下起草、预览、写入并注册 workflow。还缺少的是测量：团队应先记录任务完成率、分支准确率、延迟和 token 使用量，再说它比普通 agent prompt 更安全。

### Evidence
- [New AI Agent Architecture to fix LLM deviations and token costs](../Inbox/2026-05-31--new-ai-agent-architecture-to-fix-llm-deviations-and-token-costs.md): Summarizes BotCircuits’ deterministic workflow engine, JSON workflow files, branch conditions, and lack of benchmark results.
- [New AI Agent Architecture to fix LLM deviations and token costs](../Inbox/2026-05-31--new-ai-agent-architecture-to-fix-llm-deviations-and-token-costs.md): Shows workflows stored under `.botcircuits/workflows/` and registered as callable tools.
- [New AI Agent Architecture to fix LLM deviations and token costs](../Inbox/2026-05-31--new-ai-agent-architecture-to-fix-llm-deviations-and-token-costs.md): Shows workflow creation, preview, file writing, live registration, and direct workflow runs.

## Pull request review for generated code vocabulary and tests
接受 LLM 生成代码的团队，需要在名字、边界、不变量和测试上加审查步骤。Martin Fowler 的文章把代码描述为机器指令，也描述为团队共享的概念模型。对生成代码来说，风险在于代码能跑，但会带入团队在维护时解释不清的词、结构或抽象。

一个实用改动，是在 pull request 审查里加一个简短的 generated-code 部分：列出所有新的领域术语，把它们映射到已有的 bounded context，或者说明新边界；在测试里标出不变量；让作者删掉那些只是照着 prompt 复述的名字。这样模型以后能拿到更好的上下文，审查者也有一个具体办法在认知债扩散到整个代码库之前把它抓出来。

### Evidence
- [What Is Code](../Inbox/2026-05-31--what-is-code.md): Summarizes the essay’s claim that LLM-assisted work depends on shared domain meaning, stable abstractions, and tests.
- [What Is Code](../Inbox/2026-05-31--what-is-code.md): Describes concepts, names, boundaries, relationships, and shared vocabulary as the visible conceptual model.
- [What Is Code](../Inbox/2026-05-31--what-is-code.md): Connects domain vocabulary to code structures such as types, interfaces, invariants, and workflows.
