---
source: hn
url: https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2
published_at: '2026-03-03T23:48:02'
authors:
- btraut
topics:
- agentic-coding
- multi-agent-workflow
- worktrees
- persistent-memory
- developer-tools
relevance_score: 0.08
run_id: materialize-outputs
---

# Graduate from Single-Session Coding: My Full Agentic Coding Workflow

## Summary
这是一篇关于“代理式编程工作流”的经验性文章，主张从单会话 AI 编码升级为多代理并行、带持久记忆和工具链编排的软件开发系统。核心价值在于提升并行度、降低上下文退化，并把规划、实现、测试、审查和运维串成可复用流程。

## Problem
- 文章要解决的问题是：单一 AI 编码会话是**单线程**的，难以并行推进多个任务，而且多个代理共用同一工作副本时容易互相覆盖和冲突。
- 长对话会消耗上下文，接近或触发 compaction boundary 后，代理会“变笨/变懒”；同时还会出现 **context rot** 和 **context poisoning**，导致任务偏航且难以纠正。
- 这很重要，因为如果没有外部化的任务管理、上下文管理和执行工具链，AI 代理很难稳定地承担从需求规划到实现、测试、上线和维护的完整软件生命周期工作。

## Approach
- 核心方法很简单：把一个聊天窗口里的编程，拆成一个**多代理协作系统**。用 **worktrees** 给每个代理独立代码副本，实现安全并行开发。
- 用 **Conductor** 作为多代理编排层，管理 workspaces/worktrees、不同模型会话，以及规划/实现/测试等不同阶段的切换。
- 用 **Beads** 作为会话外的**持久记忆与任务系统**：先把需求沉淀成 markdown spec，再拆成 beads；父代理读取任务依赖图，派发子代理并行完成，每个子代理提交代码、关闭 bead、回写备注。
- 用 **Skills、AGENTS.md、CLI/MCP、浏览器自动化** 把最佳实践和操作流程显式化，让代理能重复执行规划、实现、PR 管理、线上排障、浏览器测试等任务。
- 作者还强调按任务选模型：主要用 Codex 写代码，Opus 用于代码审查、维护和本地 CLI 杂活，以形成“模型+工具+流程”的组合栈。

## Results
- 文中**没有提供正式实验、基准数据或可复现评测**，因此没有论文式的定量结果可报告。
- 最明确的量化说法之一是：使用 **Blacksmith** 作为 GitHub Actions 替代后，作者称其**构建时间减半**，即 build times cut in half；但未给出具体项目、绝对时延或对照配置细节。
- 作者声称该工作流已分享给“**several friends and peers**”，并反复得到“it works”的反馈，但没有样本量、任务类型、成功率或生产力增幅数据。
- 文章的主要突破性主张是工程流程层面的：通过 **worktrees + Conductor + Beads + Skills + browser/CLI loops**，开发者可以从“和一个聊天机器人结对编程”升级到“协调多个代理并行规划、编码、审查和维护真实软件”。
- 另一个明确但非定量主张是：Codex 在写代码上“明显强于 Claude”，不过这同样属于作者经验判断，没有附带标准化 benchmark 数字。

## Link
- [https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2](https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2)
