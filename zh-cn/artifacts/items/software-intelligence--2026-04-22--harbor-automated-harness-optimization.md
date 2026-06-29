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
这篇论文认为，在长周期编码代理中，主要复杂性来自代理 harness，而不是基础模型；当 harness 标志位之间的交互增多后，手工调参就会失效。论文提出 Harbor，一套用于自动配置 harness 的贝叶斯优化系统，并用一个生产环境编码代理研究来支持这一观点。

## 问题
- 长周期代理依赖许多 harness 功能，比如缓存、记忆、压缩、工具预测和自评估，这些功能之间的交互让手工调参不可靠。
- 在引用的生产环境中，harness 几乎占了系统代码的大部分：文中引用对 Claude Code 的审计结果约为 98.4% 是 harness 代码，1.6% 是 AI 决策逻辑；一个包含 100 个工具的代理在用户任务开始前，最多可把 40% 的上下文窗口用于工具描述。
- 这会带来实际影响，因为团队通常通过小规模消融循环来发布 harness 改动，但论文中的案例研究显示，把已发表的方法叠加起来，可能会降低通过率，而不是提高它。

## 方法
- 论文把自动 harness 优化表述为带约束的噪声贝叶斯优化，搜索空间是由 harness 标志位和评测保真度组成的混合配置空间，运行成本也不一样。
- Harbor 使用分块可加的 SAAS 代理模型、多保真度的成本感知采集规则，以及 TuRBO 信任区域，来决定下一步测试哪些标志位组合。
- 它会对冷启动效应修正奖励，这样在基准任务不允许记忆预热时，跨会话功能就不会被过度惩罚。
- 它加入了后验机会约束安全检查和基于遥测的静默标志检测，这样在搜索时就能排除失效或未激活的功能。
- 具体测试平台是一个由标志位控制的 codex-py 编码代理 harness，总共大约有 30 项增强能力，其中评估了 9 个标志位，包括语义缓存、跨会话记忆、对话压缩、轨迹回放、推测性工具预测、自评估、ACON 压缩、Reflexion 和 PASTE。

## 结果
- 在 Terminal-Bench 2 的 89 个任务上进行的手工调参案例研究中，所有标志位都关闭的基线通过了 15/89 个任务。
- B 轮启用了 5 个原生 harness 标志位，结果达到 17/89，这是文中报告的调参轮次里唯一一次相对基线的净提升。
- C 轮加入自评估门控后，性能降到 13/89，比 B 轮少 4 个任务。
- D 轮再加入 ACON、Reflexion 和 PASTE 后，性能降到 12/89，比 B 轮少 5 个任务。
- 对所有测试配置取 oracle 并集后，结果达到 81/89。作者用这一点说明，性能高度依赖配置，而且没有任何一个手工调好的堆栈能覆盖大部分可获得的收益。
- 这段摘要没有给出 Harbor 端到端搜索的最终定量结果，只给出了手工 A-D 研究。因此，在这段文字里，Harbor 最明确的结论是优化问题的形式化和参考求解器设计，而不是一个优于手工调参的已报告搜索结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20938v1](http://arxiv.org/abs/2604.20938v1)
