---
kind: trend
trend_doc_id: 1652
granularity: day
period_start: '2026-06-26T00:00:00'
period_end: '2026-06-27T00:00:00'
topics:
- coding agents
- developer tools
- terminal UI
- ratchets
- regex
- code quality
run_id: materialize-outputs
aliases:
- recoleta-trend-1652
tags:
- recoleta/trend
- topic/coding-agents
- topic/developer-tools
- topic/terminal-ui
- topic/ratchets
- topic/regex
- topic/code-quality
language_code: zh-CN
---

# 编码智能体工作正在集中于操作员控制和护栏

## 概览
当天语料规模小，内容偏实用。Workbench 关注在不丢失状态的情况下运行多个编码智能体。Ratchets 关注低成本规则检查，用来阻止智能体添加不想要的模式。

## 研究发现

### 并行智能体工作台
Workbench 把多智能体编码打包成全屏终端用户界面（TUI）。每个工作区可以包含一个智能体窗格、多个 shell 窗格、打开的文件，以及实时 git diff。这个设计针对一个常见的操作问题：同时运行多个智能体时，仍能在一个地方看到文件、变更和会话。

最具体的细节是持久化。智能体和终端窗格运行在一个私有 tmux 服务器内，所以重启 UI 后可以重新连接到仍在运行的进程。该工具称支持 Claude Code、Gemini、Goose、OpenCode 和 Cursor，但语料没有提供任务基准、延迟结果或用户研究。

#### 资料来源
- [Workbench: A TUI for parallel coding agents](../Inbox/2026-06-26--workbench-a-tui-for-parallel-coding-agents.md): 摘要描述了 Workbench 的 TUI、基于 tmux 的持久化、智能体后端、查看器，以及缺少基准证据。

### 面向智能体编写代码的规则 ratchet
Ratchets 把代码风格和安全规则视为计数器，用来阻止新增被禁止的模式，同时容忍已有债务。这适合智能体工作流，因为模型可能在缺少足够项目上下文时选择快速抑制，例如 `# pyrefly: ignore`。

Ratchets v0.4.0 用 Resharp 替换了 Rust 的 `regex` crate。给出的原因是需要环视支持，用于更适合写成文本模式的规则，尤其是注释风格规则。在 Sculptor 代码库上，作者报告称更换正则引擎后速度提升约 15%，但没有提供绝对运行时间或重复运行细节。

#### 资料来源
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): 摘要报告了 Resharp 替换、环视支持、Ratchets 工作流，以及 Sculptor 上 15% 的速度结果。
