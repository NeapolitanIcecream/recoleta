---
kind: ideas
granularity: day
period_start: '2026-06-26T00:00:00'
period_end: '2026-06-27T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- developer tools
- terminal UI
- ratchets
- regex
- code quality
tags:
- recoleta/ideas
- topic/coding-agents
- topic/developer-tools
- topic/terminal-ui
- topic/ratchets
- topic/regex
- topic/code-quality
language_code: zh-CN
---

# 编码代理工作流防护

## Summary
大量使用代理的开发需要把控制放进日常工作流：禁止代码模式的计数器、并行代理会话的持久视图，以及面向需要 lookaround 的 Rust 规则扫描器的窄范围正则引擎测试。

## 针对代理创建的类型检查器抑制的棘轮检查
允许编码代理编辑生产代码的团队，可以为 `# pyrefly: ignore` 这类抑制写法添加棘轮检查。该检查把当前数量作为上限；代理新增实例时检查失败；是否提高上限交给有更多上下文的规划代理或人工评审者决定。

这是低成本防护，因为它避开了冗长的风格提示，也不需要 LLM 裁判。它适合那些少数情况下快速抑制可能有效、但默认使用会带来损害的场景。小规模试验可以从 CI 中的一条规则开始，报告当前数量，并且只阻止代理编写分支上的新增实例。

### Evidence
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): 摘要把 ratchet 描述为禁止模式的计数器，提到编码代理的风格违规，并将 `# pyrefly: ignore` 列为目标案例。
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): 源文本解释了类型检查器抑制示例，以及只有规划代理可以提高棘轮计数的工作流。

## 面向并行编码代理会话的持久终端工作区
同时运行多个编码代理 CLI 的开发者，可以测试一个全屏终端工作区，把每个代理、shell、打开的文件和工作树 diff 放在同一处可见。采用测试很直接：让两三个代理处理不同任务，在会话中重启 UI，然后检查操作员能否重新连接，且不丢失进程状态或文件变更线索。

Workbench 是这一模式的具体例子。它使用私有 tmux 服务器来持久化代理和终端窗格，支持 Claude Code、Gemini、Goose、OpenCode 和 Cursor，并为每个工作区添加只读文件查看器和实时 git diff。现有证据提供的是产品细节，没有任务成功率基准，所以第一轮检查应衡量操作员可见的失败：会话丢失、错误工作区编辑、遗漏 diff，以及在工具之间切换所花的时间。

### Evidence
- [Workbench: A TUI for parallel coding agents](../Inbox/2026-06-26--workbench-a-tui-for-parallel-coding-agents.md): 摘要说明 Workbench 是面向多个编码代理 CLI 的全屏 TUI，带有 tmux 持久化、文件查看器、shell 窗格和 git diff 跟踪。
- [Workbench: A TUI for parallel coding agents](../Inbox/2026-06-26--workbench-a-tui-for-parallel-coding-agents.md): 源文本描述了私有 tmux 服务器上的持久会话，以及实时 git 变更标签页。
- [Workbench: A TUI for parallel coding agents](../Inbox/2026-06-26--workbench-a-tui-for-parallel-coding-agents.md): 源文本给出了保存状态路径和私有 tmux socket，支持持久化这一说法。

## 面向需要 lookaround 的 Rust 规则扫描器的 Resharp 基准测试
基于 Rust 的规则扫描器维护者，在正则规则需要 lookaround 时，可以做一次范围受控的 Resharp 评估，尤其适用于通过 AST 查询难以表达的注释风格检查。测试应使用项目的真实规则，记录绝对运行时间、规则数量、硬件和多次运行的方差，并纳入兼容性失败，因为 Ratchets v0.4.0 是一次破坏性的引擎变更。

Ratchets 报告提供了一个有用起点：作者将 Rust 的 `regex` crate 替换为 Resharp 后，在 Sculptor 代码库上看到约 15% 的速度提升，并且没有报告其他代码变更。更可靠的测试理由是功能覆盖，因为最初的缺口是对基于正则的规则提供 proper lookaround 支持。

### Evidence
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): 源文本报告了 Ratchets v0.4.0 的引擎变更、Sculptor 上 15% 的速度提升，以及最初对 lookaround 断言的需求。
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): 源文本解释了为什么有些规则仍然基于正则，尤其是注释风格规则，并说明 Rust 的 `regex` crate 缺少 proper lookaround。
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): 摘要记录了所报告结果的限制：一个代码库、没有绝对运行时间、没有方差、没有硬件细节。
