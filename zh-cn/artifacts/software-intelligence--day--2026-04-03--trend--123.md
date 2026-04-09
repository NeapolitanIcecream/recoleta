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

# 编码代理研究越来越难被“刷分”，也越来越容易验证

## Overview
这一时期最突出的研究，集中在那些要面对真实状态、真实失败模式和真实执行后果的编码代理。SWE-STEPS 和 ABTest 让评测更具体。GrandCode 给出一个醒目的实时结果，而 IndustryCode 用更难的工业任务把上限拉回现实。当前重点更少放在一次性补丁是否成功，而更多放在代理能否在时间推进、工具使用和代码仓库历史累积中保持稳定。

## Clusters

### 有状态评测正在成为默认门槛
评测正在更接近真实代码仓库中的工作方式。SWE-STEPS 在六个 Python 代码仓库上测试相互依赖的 pull request 链，显示孤立的 PR 评分会把成功率高估最多 20 个百分点。Claude Sonnet 4.5 在一个划分上从 66.25% 降到 43.75%，Gemini 3 Flash 从 56.52% 降到 36.59%。同一篇论文还报告，代理编写的代码会让代码仓库健康状况更差，认知复杂度和技术债务都高于人工基线。ABTest 从另一个角度得出相同结论：它把 400 个已确认的用户失败案例转成 647 个可执行用例，并在 Claude Code、Codex CLI 和 Gemini CLI 中发现 642 个新的真实异常。共同的信息很明确：现在，编码代理的质量取决于长时程行为、工作区状态，以及在混乱交互后恢复的能力，不只是看单个补丁是否一次通过测试。

#### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): 顺序 PR 基准显示，孤立评分会高估结果，并暴露代码仓库健康问题。
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): 在真实代码仓库上进行的行为驱动模糊测试发现了许多新的代理异常。

### 编码代理风险现在包括被投毒的技能和文档
安全研究正在进入代理自身的供应链。关于技能投毒的论文显示，编码代理会从看似可信的文档中复制恶意逻辑，并在正常的环境搭建或编码工作中执行它。在 1,070 个对抗性技能中，四种框架和五个模型上的绕过率为 11.6% 到 33.5%。静态分析能拦住大多数攻击，但仍有 2.5% 同时绕过了静态检查和模型对齐，作者还报告了四个已确认漏洞。这对当前的代理产品很重要，因为攻击路径经过第三方技能中的普通示例和模板，不只是显式的提示注入。

#### Evidence
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): 给出了针对编码代理技能的具体供应链攻击路径和测得的绕过率。

### 能力声明更强了，测试也更难了
这一时期也有两个很强的能力声明，但两者都配套了更严格的测量。GrandCode 报告在三场实时 Codeforces 比赛中拿到第一名，领先所有人类参赛者，并将结果归因于一个带有对抗测试生成和在线更新的多代理强化学习设置。在另一种场景中，IndustryCode 把代码生成的目标扩展到 125 个工业问题和 579 个子问题，覆盖 Python、C++、MATLAB 和 Stata。即使是整体最好的模型，在子问题上的 Pass@1 也只有 68.1%，在主问题上是 42.5%。这两篇论文合起来说明，编码能力测试正在逼近边界：一边是实时竞赛，另一边是接近生产环境的工业任务。

#### Evidence
- [GrandCode: Achieving Grandmaster Level in Competitive Programming via Agentic Reinforcement Learning](../Inbox/2026-04-03--grandcode-achieving-grandmaster-level-in-competitive-programming-via-agentic-reinforcement-learning.md): 实时竞赛编程结果显示其多次获得第一名。
- [IndustryCode: A Benchmark for Industry Code Generation](../Inbox/2026-04-03--industrycode-a-benchmark-for-industry-code-generation.md): 工业基准量化了项目级编码任务上仍然存在的差距。

### 代理脚手架设计现在也是研究信号的一部分
这一组论文中有一篇在问，为什么即使模型家族看起来相似，代理结果也会差这么多。这篇脚手架分类研究在源代码层面检查了 13 个开源编码代理，发现其中 11 个结合了多种循环原语。工具数量从 Aider 的零个，到 Moatless Tools 的 37 个动作类别不等，上下文压缩也横跨七种策略。这不给出排行榜结果，但它为为什么不同代理之间的基准分数难以直接比较提供了实际解释。控制循环、工具接口、状态处理和执行隔离本身仍然都是变化中的部分。

#### Evidence
- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](../Inbox/2026-04-03--inside-the-scaffold-a-source-code-taxonomy-of-coding-agent-architectures.md): 源代码分类法识别出会影响可靠性和可比性的脚手架差异。
