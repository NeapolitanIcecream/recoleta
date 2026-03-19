---
source: hn
url: https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2
published_at: '2026-03-03T23:48:02'
authors:
- btraut
topics:
- agentic-coding
- multi-agent-workflow
- code-intelligence
- developer-tooling
- persistent-memory
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Graduate from Single-Session Coding: My Full Agentic Coding Workflow

## Summary
这是一篇面向工程实践的“代理式编码工作流”经验总结，核心目标是把单会话的人机结对编程升级为可并行、可记忆、可自动化的软件交付系统。文章强调通过工作树、多代理编排、持久化任务记忆和工具化提示，把规划、实现、测试、审查与运维串成一个闭环。

## Problem
- 传统单会话编码是**单线程**的：只有一个工作副本时，多代理会互相覆盖，难以并行开发。
- 长对话会消耗上下文，接近或触发 compaction boundary 后，代理会“变笨、变懒”，还会出现 **context rot / context poisoning**。
- 许多开发活动仍靠人工串联：规划、实现、测试、PR、浏览器验证、线上排障、密钥管理等缺少统一工作流，导致效率受限。

## Approach
- 用 **git worktrees + Conductor** 给每个并行任务提供独立工作空间，让多个代理安全并行；Conductor 负责 worktree 的创建、管理和清理，并支持在同一 harness 中切换 Claude/Codex。
- 用 **Beads** 作为代理外部的持久化记忆与任务层：先把计划写成 markdown spec，再拆成 beads（含依赖关系），新会话按 bead 执行，父代理并行派发子代理，每个子代理完成任务后提交代码、关闭 bead、回传备注。
- 用 **Skills / AGENTS.md** 把高频流程和局部规范编码化：如 brainstorm、beads-create、beads-implement，以及项目级/目录级开发规范、CLI 工具使用说明。
- 用 **browser/CLI loop** 扩展代理执行面：通过 agent-browser 或 Browser Bridge 做网页/Electron 验证，通过 gh、Sentry、Railway、Doppler 等 CLI/MCP 直接处理 PR、线上问题、部署与密钥。
- 在模型选择上采用分工：作者偏向 **Codex 负责主要编码**，用 **Opus** 做代码审查、维护任务和本地 CLI 杂务。

## Results
- 文中**没有提供严格实验、基准数据或可复现实验表格**，因此没有可核验的学术量化结果。
- 最明确的量化陈述是：使用 **Blacksmith** 替代 GitHub Actions 后，作者称**构建时间减少约 50%（cut my build times in half）**，且免费额度更高。
- 作者声称该工作流让其从“**pairing with one chat**”升级到“**running coordinated agents**”，可由多个代理协同完成计划、实现、评审和维护，但未给出吞吐量、缺陷率或周期时间等数字。
- 作者还声称该方法已分享给“**several friends and peers**”，并反复得到“**it works**”的反馈，但**未给出样本数、任务类型或对照基线**。
- 关于模型比较，文章提出“**Codex 对写代码明显强于 Claude**”这一强主张，但**没有提供基准名称、分数或任务级统计**。
- 整体上，文章的突破点更偏**系统工作流整合**而非新算法：把工作树、任务记忆、子代理并行、技能提示、浏览器/CLI 自动化整合成一个“软件交付操作系统”。

## Link
- [https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2](https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2)
