---
kind: trend
trend_doc_id: 123
granularity: day
period_start: '2026-04-03T00:00:00'
period_end: '2026-04-04T00:00:00'
topics:
- coding-agents
- evaluation
- software-engineering
- security
- benchmarks
- competitive-programming
run_id: materialize-outputs
aliases:
- recoleta-trend-123
tags:
- recoleta/trend
- topic/coding-agents
- topic/evaluation
- topic/software-engineering
- topic/security
- topic/benchmarks
- topic/competitive-programming
language_code: zh-CN
---

# 编码代理研究正变得更难作弊，也更容易验证

## Overview
这一阶段最强的内容集中在那些要面对真实状态、真实失败模式和真实执行后果的编码代理上。SWE-STEPS 和 ABTest 让评估更具体。GrandCode 给出一个醒目的现场结果，而 IndustryCode 用更难的工业任务把上限拉回到现实。当前重点更少放在一次性补丁是否成功，更集中在代理能否在时间、工具和仓库历史中保持稳定。

## Clusters

### 有状态评估正在成为默认标准
评估正在更接近真实仓库中的工作方式。SWE-STEPS 在六个 Python 仓库上测试相互依赖的拉取请求链，显示孤立的 PR 评分最多会把成功率高估 20 个百分点。Claude Sonnet 4.5 在一个切分上的成绩从 66.25% 降到 43.75%，Gemini 3 Flash 从 56.52% 降到 36.59%。同一篇论文还报告说，代理写出的代码让仓库健康状况更差，认知复杂度和技术债都高于人工基线。ABTest 从另一个角度推进了同样的思路：它把 400 个已确认的用户失败转成 647 个可执行案例，在 Claude Code、Codex CLI 和 Gemini CLI 上找到了 642 个新的真实异常。核心信息很直接：编码代理的质量现在取决于长时间跨度内的行为、工作区状态，以及对混乱交互的恢复能力，而不只是单个补丁能否一次通过测试。

#### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): Sequential PR benchmark shows inflated isolated scores and repository-health concerns.
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): Behavior-driven fuzzing on real repositories finds many new agent anomalies.

### 编码代理风险现在还包括被投毒的技能和文档
安全工作正在进入代理供应链本身。技能投毒论文显示，编码代理会从看似可信的文档中复制恶意逻辑，并在正常的设置或编码过程中执行它。在 1,070 个对抗性技能中，四个框架和五个模型上的绕过率为 11.6% 到 33.5%。静态分析挡住了大多数攻击，但仍有 2.5% 同时绕过了静态检查和模型对齐，作者还报告了四个已确认漏洞。对当前的代理产品来说，这很重要，因为攻击路径经过的是第三方技能里的普通示例和模板，而不只是显式的提示注入。

#### Evidence
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): Concrete supply-chain attack path and measured bypass rates for coding-agent skills.

### 能力主张更强了，测试也更难了
这个阶段也有两项很强的能力主张，但两者都伴随着更严格的测量。GrandCode 报告在三轮现场 Codeforces 比赛中拿到第一，超过所有人类参赛者，并把结果归因于一个带有对抗性测试生成和在线更新的多智能体强化学习设置。另一个场景里，IndustryCode 把代码生成目标扩展到 125 个工业问题和 579 个子问题，覆盖 Python、C++、MATLAB 和 Stata。即使是最佳总体模型，在子问题上的 Pass@1 也只有 68.1%，在主问题上是 42.5%。这些论文放在一起说明，编码性能正在边界上接受测试：一边是现场竞赛，另一边是生产风格的工业任务。

#### Evidence
- [GrandCode: Achieving Grandmaster Level in Competitive Programming via Agentic Reinforcement Learning](../Inbox/2026-04-03--grandcode-achieving-grandmaster-level-in-competitive-programming-via-agentic-reinforcement-learning.md): Live competitive programming result with repeated first-place finishes.
- [IndustryCode: A Benchmark for Industry Code Generation](../Inbox/2026-04-03--industrycode-a-benchmark-for-industry-code-generation.md): Industrial benchmark quantifies the remaining gap on project-level coding tasks.

### 代理 scaffold 设计现在也是研究信号的一部分
这组论文里有一篇在问，为什么即使模型家族看起来相近，代理结果还是会差这么多。scaffold 分类法从源代码层面检查了 13 个开源编码代理，发现其中 11 个组合了多种循环原语。工具数量从 Aider 的 0 个到 Moatless Tools 的 37 个动作类不等，context compaction 也用了 7 种策略。这没有给出排行榜结果，但它解释了为什么不同代理之间的基准分数很难直接比较。控制循环、工具接口、状态处理和执行隔离，本身就是还在变化的部分。

#### Evidence
- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](../Inbox/2026-04-03--inside-the-scaffold-a-source-code-taxonomy-of-coding-agent-architectures.md): Source-code taxonomy identifies scaffold variation that affects reliability and comparability.
