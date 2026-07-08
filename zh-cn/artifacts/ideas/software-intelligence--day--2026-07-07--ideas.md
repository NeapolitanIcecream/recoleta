---
kind: ideas
granularity: day
period_start: '2026-07-07T00:00:00'
period_end: '2026-07-08T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software verification
- agentic code review
- trajectory diagnostics
- agent reliability
- developer learning
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-verification
- topic/agentic-code-review
- topic/trajectory-diagnostics
- topic/agent-reliability
- topic/developer-learning
language_code: zh-CN
---

# 编码 Agent 的信任控制

## Summary
编码 agent 的采用正在转向工作循环内的外部检查：AI 拉取请求推进前进行代码库感知评审，用轨迹诊断判断哪些 agent 运行值得信任，并为 agent 系统依赖的 Python 库增加规范感知测试。

## 面向 AI 生成拉取请求的代码库感知评审循环
接受 AI 生成拉取请求的团队，可以增加一道自动化评审，采用和人工评审相同的最低证据要求：检查代码库、运行命令、决定批准或要求修改，并返回具体修复指导。SWE-Review 给出了这个工作流的可执行形态。它的评审器接收一个代码库检出、一个 issue 和一个 AI 生成的 PR，然后产出合并决策和用于修订的诊断。​​

实际要处理的是这类 PR：diff 看起来合理，但代码库其他位置的问题仍未解决。在 SWE-Review 中，迭代式生成-评审-修订把 Qwen3-30B-A3B PRs 在 SWE-bench Verified 上的解决率从 27.5% 提高到 56.9%，把 Qwen3-Coder-30B-A3B PRs 的解决率从 50.9% 提高到 68.8%。一个低成本的内部测试可以在最近 50 个需要人工返工的 AI PRs 上运行这个循环，然后比较三个数字：正确拒绝率、被接受的坏 PRs 数量，以及评审后修复率。

### Evidence
- [SWE-Review: Closing the Loop on Issue Resolution with Agentic Code Review](../Inbox/2026-07-07--swe-review-closing-the-loop-on-issue-resolution-with-agentic-code-review.md): SWE-Review 定义了感知代码库的评审器、它的批准/要求修改输出、评审引导的修订循环，以及报告的解决率提升。
- [SWE-Review: Closing the Loop on Issue Resolution with Agentic Code Review](../Inbox/2026-07-07--swe-review-closing-the-loop-on-issue-resolution-with-agentic-code-review.md): 论文描述了基准设置、评审器输出，以及完成率、决策准确率和修订后解决率等指标。

## 用于编码 agent 发布评估的轨迹诊断
Agent 团队应在最终通过或失败之外，用轨迹证据给编码 agent 打分。TraceProbe 展示了一条具体实现路径：把每次运行转换为规范动作类型，例如读取文件、写入文件、搜索、命令、计划和推理，然后附加 failed、reverted、justified、off-anchor 等效果标签。

这有助于处理一个常见发布问题：两个 agent 可以解决同一个 issue，但带来很不同的评审负担。在 TraceProbe 的 SWE-Bench pytest-7982 示例中，Claude Code with Opus 4.6 用 10 步解决任务且没有失败动作，而 OpenCode with GLM-5 也解决了任务，但用了 49 步，并出现了反复失败和恢复的片段。一个有用的采用检查，是对已接受的 agent 补丁运行这种轨迹规范化，并在人类评审前标记带有搜索循环、跳过验证、无依据完成声明或大段恢复过程的运行，避免直接把它们用作正样本。

### Evidence
- [What Resolve Rate Hides: Trajectory Structure Diagnostics for Coding Agents](../Inbox/2026-07-07--what-resolve-rate-hides-trajectory-structure-diagnostics-for-coding-agents.md): TraceProbe 的摘要列出了九种动作类型、确定性的效果标签、反模式检查，以及 2,500 条轨迹的 SWE-Bench Verified 评估。
- [What Resolve Rate Hides: Trajectory Structure Diagnostics for Coding Agents](../Inbox/2026-07-07--what-resolve-rate-hides-trajectory-structure-diagnostics-for-coding-agents.md): 论文的引导示例比较了两次成功运行，它们的步骤数和恢复行为差异很大。

## 面向 agent 框架升级的规范感知回归测试
基于 LangChain、LlamaIndex、CrewAI 或类似库构建系统的团队，可以在把某个框架版本投入生产前，增加升级测试，生成有效但覆盖边界情况的 API 调用。LogicHunter 是一种具体模式：挖掘源代码、类型提示、Pydantic schemas、文档和代码库用法来创建可执行种子测试，再把有效调用变异为行为探针，用来检查字段保留、幂等性、边界行为和返回类型一致性。

运维痛点是失败分诊噪声高。在 agent 库中，ValueError 或 KeyError 可能是正确拒绝、调用方误用，也可能是库 bug；静默的错误行为可能不会抛出异常。LogicHunter 的 Agentic Oracle 会检查文档、源代码、复现脚本和运行时状态，再给异常打上 bug 标签。在 LangChain、LlamaIndex 和 CrewAI 上，这项研究发现了 40 个先前未知的 bug，其中 30 个得到确认，26 个已修复。这个工作流的小型版本可以先作为 nightly job，覆盖少数涉及工具、记忆、回调和异步执行的框架 API。

### Evidence
- [LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle](../Inbox/2026-07-07--logichunter-testing-llm-agent-frameworks-with-an-agentic-oracle.md): LogicHunter 的摘要描述了有效种子生成、行为探针、Agentic Oracle，以及在 LangChain、LlamaIndex 和 CrewAI 上确认的 bug 结果。
- [LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle](../Inbox/2026-07-07--logichunter-testing-llm-agent-frameworks-with-an-agentic-oracle.md): 论文解释了为什么普通异常和静默语义失败会给纯 Python agent 框架带来 oracle 问题。
