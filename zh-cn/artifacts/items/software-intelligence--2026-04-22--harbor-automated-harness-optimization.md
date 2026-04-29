---
source: arxiv
url: http://arxiv.org/abs/2604.20938v1
published_at: '2026-04-22T13:45:12'
authors:
- Biswa Sengupta
- Jinhua Wang
topics:
- bayesian-optimization
- llm-agents
- code-intelligence
- agent-harness
- automated-tuning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# HARBOR: Automated Harness Optimization

## Summary
## 摘要
这篇论文认为，在长时程编程代理中，主要的复杂性来源于代理 harness，而不是底层模型；一旦功能之间的交互变多，靠人工调整 harness 标志位就会失效。论文提出了 Harbor，这是一套用于自动化 harness 配置的贝叶斯优化系统，并用一个生产级编程代理研究来支持这一观点。

## 问题
- 长时程代理依赖许多 harness 功能，例如缓存、记忆、压缩、工具预测和自我评估，而这些功能之间会相互作用，使人工调参不可靠。
- 在论文引用的生产环境中，harness 占了系统代码的大部分：文中引用对 Claude Code 的一次审计，称其中约 98.4% 是 harness 代码，只有 1.6% 是 AI 决策逻辑；一个拥有 100 个工具的代理，甚至可能在用户任务开始前就把最多 40% 的上下文窗口用在工具描述上。
- 这很重要，因为团队通常通过小规模消融循环来发布 harness 改动，但论文中的案例研究显示，把已发表的方法叠加起来，反而可能降低通过率，而不是提高它。

## 方法
- 论文将自动化 harness 优化表述为：在由 harness 标志位和评估保真度组成的混合配置空间上进行带约束、含噪声的贝叶斯优化，并考虑不同配置运行成本不一致的问题。
- Harbor 使用块加性 SAAS 代理模型、多保真且考虑成本的采集规则，以及 TuRBO 信任域，来决定下一步测试哪些标志位组合。
- 它会对冷启动效应做奖励修正，这样在基准任务无法让记忆充分预热时，跨会话功能就不会被评得过低。
- 它加入了后验机会约束安全检查，以及由遥测驱动的静默标志位检测，以便在搜索过程中排除损坏或未生效的功能。
- 具体测试平台是一个带标志位门控的 codex-py 编程代理 harness，总体约有 30 种增强能力，其中评估了 9 个标志位，包括 semantic cache、cross-session memory、conversation compression、trajectory replay、speculative tool prediction、self-evaluation、ACON compression、Reflexion 和 PASTE。

## 结果
- 在 Terminal-Bench 2 的人工调参案例研究中，共有 89 个任务，全部标志位关闭的基线通过了 15/89 个任务。
- B 轮启用了 5 个原生 harness 标志位，达到 17/89，是报告中的几轮调参里唯一相对基线有明确提升的一轮。
- C 轮加入 self-evaluation gate 后，成绩降到 13/89，比 B 轮少了 4 个任务。
- D 轮再加入 ACON、Reflexion 和 PASTE 后，成绩降到 12/89，比 B 轮少了 5 个任务。
- 所有已测试配置的 oracle union 达到 81/89，作者用这一点说明性能对配置非常敏感，而且没有任何一个人工调好的组合覆盖了大部分本来可以获得的提升。
- 这段摘录没有给出 Harbor 端到端搜索的最终定量结果，除了人工 A-D 研究之外，没有更多数据。因此，在这段文本里，关于 Harbor 最强的具体结论是它的优化问题表述和参考求解器设计，而不是它在已报告结果中明确胜过人工调参。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20938v1](http://arxiv.org/abs/2604.20938v1)
