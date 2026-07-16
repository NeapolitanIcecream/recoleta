---
kind: ideas
granularity: week
period_start: '2026-06-15T00:00:00'
period_end: '2026-06-22T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent evaluation
- software verification
- program repair
- agent memory
- benchmark contamination
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-verification
- topic/program-repair
- topic/agent-memory
- topic/benchmark-contamination
language_code: zh-CN
---

# 代码智能体验收控制

## 摘要
代码智能体采用正在转向具体的验收检查：经过失败测试的仓库指令、围绕智能体工作的轨迹门禁，以及面向陌生语料的分配前考试。有用工作位于模型周围的支持层：智能体被告知了什么、它实际做了什么、它使用了哪些证据，以及在人类评审结果前通过了哪些检查。

## 面向仓库特定代码智能体的失败测试版 AGENTS.md 文件
使用代码智能体的团队可以把仓库指导纳入测试流程。一个可行做法是先写一个简短的 AGENTS.md 文件，为该仓库生成合成缺陷修复探针，让智能体尝试修复，并且只在失败运行显示指令缺失或误导时修改指导。最终文件应以紧凑形式列出子系统入口点、测试命令、已知脆弱路径和质量门禁。

Probe-and-Refine 给出了这个流程的具体形式。在 500 个 SWE-bench Verified 实例上，精炼后的指导达到 33.0% 的平均解决率；静态知识库为 28.3%，无上下文为 25.5%。报告中的提升主要来自更多可评估补丁，而不是更高的单补丁精度。这对维护者有用，因为糟糕的指令文件经常把智能体带到错误文件，或让它在生成有意义补丁之前卡住。

低成本采用测试可以这样做：让同一个智能体在一小组近期已修复缺陷上运行三种指导版本：无文件、手写文件、探针精炼文件。跟踪智能体是否找到正确文件、运行正确测试，并产出可进入评审的补丁。如果精炼文件只增加通用建议，就应像其他无用仓库产物一样被拒绝。

### 资料来源
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): 报告了 Probe-and-Refine 方法、SWE-bench Verified 解决率对比，以及精炼指导主要提高可评估补丁覆盖率的发现。
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): 描述了 AGENTS.md 类文件要捕获的操作知识，包括入口点、测试、约定和调试策略。

## 用于接受代码智能体 pull request 的轨迹门禁
智能体生成的 pull request 需要在 diff 旁边附上一小段动作日志。有用记录很简单：读取的文件、仓库搜索、编辑、命令、测试、重试和提交。CI 门禁随后可以检查规则，例如“最终编辑之后运行了测试”、“智能体在编辑前查看了被改动的子系统”，以及“任务没有在反复测试失败后提交”。这些检查让评审者在阅读补丁之前先看到工作路径的证据。

ProcGrep 说明了这件事为什么可行。它把代码智能体轨迹转成 `read_file`、`search_repo`、`edit`、`run_test` 和 `submit` 等动作序列，然后支持对这些轨迹进行确定性结构查询。在来自 10 个智能体的 SWE-bench Verified 轨迹上，过程指纹以 85.7% 的准确率把未见过的轨迹归因到正确智能体；ProcGrep 在一个分阶段轨迹搜索任务上达到 F1=1.000，单次决策延迟为微秒级。

GlueRun-go 为已经运行并行智能体的团队提供了一种实现模式。每个 worker 在单独的 Git worktree 中运行，持有一个 JSON lease，写入包含变更文件、命令、测试和证据的状态包，并把门禁结果送入审计和恢复路径。该项目证据是工程证据，不是标准基准结果，但形式有用：隔离工作，记录任务证据，并把门禁失败作为一等结果处理。

### 资料来源
- [Agent trajectories as programs: fingerprinting and programming coding-agent behavior](../Inbox/2026-06-15--agent-trajectories-as-programs-fingerprinting-and-programming-coding-agent-behavior.md): 定义了 ProcGrep 的动作轨迹表示、确定性轨迹查询、SWE-bench Verified 归因结果和分阶段搜索结果。
- [Show HN: Agentic coding workflows built on Git worktrees and task evidence](../Inbox/2026-06-20--show-hn-agentic-coding-workflows-built-on-git-worktrees-and-task-evidence.md): 描述了用于并行代码智能体工作的 Git worktree 隔离、JSON lease、状态包、门禁结果、审计裁决和恢复动作。
- [Show HN: Agentic coding workflows built on Git worktrees and task evidence](../Inbox/2026-06-20--show-hn-agentic-coding-workflows-built-on-git-worktrees-and-task-evidence.md): 展示了 worker 运行后使用的具体状态包和门禁结果流程。

## 把智能体分配给陌生仓库或文档前的语料考试
在把新代码库、内部库或私有文档集交给智能体之前，团队可以运行一次简短的开卷语料考试。智能体拿到它在真实任务中会使用的同一批语料，然后在几个 token 预算下回答隐藏问题。有用的问题会询问行为在哪里实现、哪个 API 是当前版本、什么配置不安全，以及哪些文档支持答案。评分应奖励在较低推理成本下给出准确答案，因为暴力搜索不适合日常工程工作。

StudyBench 把这种评估具体化。它把语料与隐藏考试配对，覆盖 DSPy 代码、OpenClaw 代码和近期机器学习文献，然后随着推理 token 增加来衡量性能。Qwen3.5-9B 在 DSPy 上的报告结果给智能体部署发出警告：强制执行 20 次搜索迭代把宽松分数从 9.6 提高到 29.4，这说明相关证据可能已经存在，但如果没有更好的学习行为，仍会被闲置。在 OpenClaw 上，两个 frontier 模型即使增加搜索，成绩也只略高于 10%。

团队可以先从近期事故、API 迁移和维护者评审意见中抽取 20 到 40 个私有问题。通过考试应要求引用文件路径或文档引用。即使智能体随后会写代码，失败答案也有用，因为它们指出会导致糟糕补丁的缺失笔记、过期文档和检索路径。

### 资料来源
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): 描述了 StudyBench、它的语料加隐藏考试设置、token 预算专业度指标，以及显示可用证据使用不足的早期结果。
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): 描述了智能体在训练后处理新库、研究论文和私有语料的实际场景。
- [Show HN: Vitrus – the company brain that tells you what it doesn't know](../Inbox/2026-06-20--show-hn-vitrus-the-company-brain-that-tells-you-what-it-doesn-t-know.md): 展示了一种有来源支撑的记忆设计，可为人类和智能体工作流返回引用、过期或无依据裁决，以及确定性缺口报告。
