---
kind: ideas
granularity: day
period_start: '2026-06-12T00:00:00'
period_end: '2026-06-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent harnesses
- AI workflow
- engineering judgment
- blockchain state
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-harnesses
- topic/ai-workflow
- topic/engineering-judgment
- topic/blockchain-state
language_code: zh-CN
---

# Bounded Coding Agent Control

## Summary
编码代理工作正朝着更小的规则表面、更窄的操作集合和定时的人类审查移动。真正有用的变化是代理配置迁移工具、安全本地编码的受限命令面，以及在长时间 AI 会话中强制做范围审查的检查点提示。

## MCP-backed scoped rule harness for team coding agents
使用 Claude Code 或类似代理的团队，可以把不断变长的指令文件改成带作用域的规则目录，再配一个只暴露当前任务所需上下文的 MCP 服务器。具体做法是一套迁移和审计工具：扫描庞大的 `CLAUDE.md`，按主题和项目路径拆分规则，标出相互矛盾的规则，然后发布像 `get_context(topic)` 这样的查询，以及用于验证状态和预算的资源。

这个问题很容易看出来：单个代理配置长到记不住，规则会套用到不该生效的项目里，团队也没有一条清晰的路径去更新共享默认值。一个小型试点可以选一个正在使用的仓库，把项目专属规则移到按路径划分的文件里，再对比拆分前后的代理错误。检查项应包括规则冲突、会话里加载了无关上下文、以及验证步骤失败，因为原始案例提到在冲突规则不再放在同一个文件里后行为更好了，但没有给出基准数字。

### Evidence
- [From a Single File to an MCP Server: Six Rewrites of My Own Harness](../Inbox/2026-06-12--from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness.md): 描述了从一个 1,800 行的 `CLAUDE.md` 迁移到作用域文件和 `keystone-mcp`，包括上下文查询、脚手架、verify 和 budget 资源。
- [From a Single File to an MCP Server: Six Rewrites of My Own Harness](../Inbox/2026-06-12--from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness.md): 显示了运行层面的失败：作者记不住大配置里的规则，写出了互相矛盾的规则，然后按主题拆分了文件。
- [From a Single File to an MCP Server: Six Rewrites of My Own Harness](../Inbox/2026-06-12--from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness.md): 展示了针对项目和语言的按路径激活方式，随着无关规则移入仓库和子树，全局文件也缩小了。

## No-shell Rust coding agent for constrained local changes
对日常 Rust 工作来说，受限的编码代理是可行的，前提是 shell 访问是主要的采用障碍。具体测试对象可以是一个只处理 Rust 的 TUI 代理，它能改文件、执行 Rust 专用操作，同时阻止任意终端命令。这样可以给维护者一个更安全的环境，用于本地机器上的小型重构、诊断和测试驱动编辑。

Agent Joe 是一个早期例子：它移除了 shell 访问，缩小了操作集合，只保留 Rust 相关操作，并被描述为可用，但仍落后于 Codex，因为提示更弱，而且没有计划模式。下一步可以在编辑前加入明确的计划步骤，然后把同一组问题分别交给 Agent Joe 和一个通用 CLI 代理。跟踪已完成任务、用户介入、未想要的命令尝试，以及失败的 `cargo` 检查。价值在于把安全取舍展示得足够清楚，让那些现在不愿在自己机器上使用 CLI 代理的团队也能看见差异。

### Evidence
- [Show HN: Agent Joe – a Rust only coding agent with no shell access](../Inbox/2026-06-12--show-hn-agent-joe-a-rust-only-coding-agent-with-no-shell-access.md): 概括了 Agent Joe 作为一个没有 shell 访问、操作更少、并且承认质量不如 Codex 的 Rust-only 终端编码代理。
- [Show HN: Agent Joe – a Rust only coding agent with no shell access](../Inbox/2026-06-12--show-hn-agent-joe-a-rust-only-coding-agent-with-no-shell-access.md): 作者说明这个工具只适用于 Rust，阻止 shell 访问，把操作限制为 Rust 专用，而且没有计划模式。

## Thirty-minute goal review in AI-assisted coding sessions
当用户还在继续提需求，而原始任务已经偏离时，AI 编码会话需要一个可见的停点。一个轻量实现可以放在 IDE、终端包装器或代理聊天里：在会话开始时记录用户声明的目标，每 30 分钟暂停一次代理，隐藏提示框，然后让工程师在没有模型输出的情况下回看目标。

这个检查点应该问三个决定：当前工作是否还符合用户问题、架构是否比任务需要得更复杂、测试或清理的程度是否和影响范围匹配。这些问题对应工程“品味”文章里的人工判断：产品思维、系统思维和质量校准。第一次验证可以做一个小团队试验，对比有无暂停的范围内任务，测量额外改动的文件数、计划外重构、放弃的分支，以及原始问题是否被关闭。

### Evidence
- [AI Doesn't Just Save Time. It Removes the Pauses](../Inbox/2026-06-12--ai-doesn-t-just-save-time-it-removes-the-pauses.md): 指出了失败模式：AI 去掉了停顿，鼓励持续追问，并且可能把短任务变成数小时的范围扩张。
- [AI Doesn't Just Save Time. It Removes the Pauses](../Inbox/2026-06-12--ai-doesn-t-just-save-time-it-removes-the-pauses.md): 给出了具体习惯：每 30 分钟停止追问、走动一下，并在没有模型的情况下回看用户想做什么。
- [What Do Engineers Mean When We Say "Taste"?](../Inbox/2026-06-12--what-do-engineers-mean-when-we-say-taste.md): 把工程判断拆成产品思维、系统思维和质量作为校准，作为 AI 处理更多机械编码时的人类贡献。
