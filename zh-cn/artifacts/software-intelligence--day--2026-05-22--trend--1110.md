---
kind: trend
trend_doc_id: 1110
granularity: day
period_start: '2026-05-22T00:00:00'
period_end: '2026-05-23T00:00:00'
topics:
- coding agents
- software evaluation
- AI code quality
- developer tools
- AI cost tracking
run_id: materialize-outputs
aliases:
- recoleta-trend-1110
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-evaluation
- topic/ai-code-quality
- topic/developer-tools
- topic/ai-cost-tracking
language_code: zh-CN
---

# AI 编码主张现在需要日志、负责人和预算

## 概览
这个时期的 AI 编码工作，正在按可检查的证据、人类负责制和运行成本来接受评估。最清楚的例子是谷歌的操作系统代理演示、Claude Code 使用追踪，以及 Planet Maiko 的本地代理工作台。

## 研究发现

### 可审计的代理演示
谷歌声称用大约 900 美元让代理构建了一个操作系统，这件事后来成了缺少证据的案例。批评不是重新跑这个任务，而是要求判断结果所需的材料：完整提示词、生成的源代码、运行日志、重试次数、dry-run 历史，以及对复制公开代码的检查。

报告里的搭建方式也很重要。这个任务用了专门角色、子代理委派、重启基础设施和反作弊组件。这些做法可能是有效的工程设计，但如果没有日志和发布材料，就很难把结果只归因于模型能力。

#### 资料来源
- [Did Google's AI agents build an operating system for $916?](../Inbox/2026-05-22--did-google-s-ai-agents-build-an-operating-system-for-916.md): Summary lists the missing prompt, code, logs, retry counts, cost, and copying checks.

### 生成代码的人类负责制
质量讨论的核心是维护。大语言模型（LLM）的输出可以增加代码量，但评审、调试、事故响应和后续修改仍然由人负责。实际标准是工程师能否解释、重构、删除和运维这些生成代码。

另一篇关于机器人和教学的案例通过实践得出了同样的操作规则。Claude Code 帮忙处理了 LaTeX、Python、一次卡尔曼滤波器修改和 ROS 迁移，但作者必须在 package.xml 问题上把它拉回正轨，也拒绝了薄弱的研究想法。提出的政策很直接：可以自由使用 AI，然后让一位具名的人负责审查许可、准确性和质量。

#### 资料来源
- [When Code Is Cheap, Does Quality Still Matter?](../Inbox/2026-05-22--when-code-is-cheap-does-quality-still-matter.md): Summary states the code-quality argument and lists narrow diffs, tests, boundaries, and human ownership as controls.
- [The First Hit Is Free](../Inbox/2026-05-22--the-first-hit-is-free.md): Summary covers the human-led AI policy, robotics examples, and need for expert review.

### 本地代理工作台
Planet Maiko 展示了代理工具如何进入开发者日常的控制面板。这个项目把任务状态、代码审查、代理会话、通知和自动化放进一个本地桌面工作流里。它最强的贡献是整合，而不是基准性能。

这些设计选择指向当前用户需要。它运行在笔记本上，声称没有遥测或托管账户，并连接 PagerDuty、Linear、Calendar 和 GitHub。它还包括本地检索增强生成（RAG）、应用内 diff 审查、代理聊天和按成本感知的模型路由。目标是在保留私有工作数据本地存放的同时，减少人工盯着代理和来回切换上下文。

#### 资料来源
- [I was bored so I turned my dev tools into an alien planet ruled by my dog](../Inbox/2026-05-22--i-was-bored-so-i-turned-my-dev-tools-into-an-alien-planet-ruled-by-my-dog.md): Summary describes Planet Maiko as a local developer workbench with agent orchestration, integrations, RAG memory, and no benchmark results.

### token 成本可见性
tokenflex.ing 的帖子把 AI token 用量当作代理式编码的运营指标。标题里的数字很高：在每月 200 美元的套餐下，一个月用了价值 30,983 美元的 Claude Code tokens。帖子没有给出可复现的测量方法，但它抓住了一个真实的管理问题：开发者通常要等到查看日志或账单数据后，才知道实际用了多少 token。

有用的建议很具体。预先写好的项目说明可以减少重复摸索代码库。涉及超过三个文件的任务应该拆开，并给出明确规格。简单的搜索和重构工作，通常更适合用 grep、文件搜索或查找替换。评论者补充了模型路由、提示缓存、按代理设预算，以及按交付功能数或合并请求数来衡量 token 的结果指标。

#### 资料来源
- [I used $30,983 of AI tokens last month in Claude Code on $200/mo plan](../Inbox/2026-05-22--i-used-30983-of-ai-tokens-last-month-in-claude-code-on-200-mo-plan.md): Summary gives the $30,983 usage claim, 65% cost-cutting anecdote, and requests for outcome metrics.
