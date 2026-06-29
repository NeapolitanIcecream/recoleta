---
source: hn
url: https://verkyyi.github.io/hermesbench/
published_at: '2026-05-30T23:03:40'
authors:
- verkyyi26
topics:
- agent-evaluation
- personal-ai-agents
- workflow-reliability
- code-agent-runner
- human-ai-interaction
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: HermesBench – workflow reliability evals for personal AI agents

## Summary
## 摘要
HermesBench 评估完整的个人智能体配置，覆盖真实工作流配方，并发布有轨迹依据的分数。当前公开基线是 78.2，覆盖 27 个配方，因此它的主要价值在于为智能体部署提供透明的可靠性测试。

## 问题
- 个人智能体的质量取决于提示、模型/提供商选择、工具、记忆、安全行为、委派、延迟和稳定性，所以只测模型会漏掉很多用户可见的故障。
- 个人智能体如果完成了错误任务、使用了不安全的副作用、隐藏不确定性，或者慢到不适合日常使用，就会造成伤害。
- 早期的智能体基准常常没有可检查的轨迹和清楚的限制，这让不同配置之间的比较很难让人信服。

## 方法
- HermesBench 会把场景配方运行在完整的 Hermes 配置上，包括提示、模型/提供商、工具、AgentSkills、记忆、网关行为、委派、安全、延迟和稳定性。
- 每个配方都有场景定义、公开评分轴、驱动关闭决策、确定性检查和脱敏后的轨迹时间线。
- 用户可以通过 Codex、Claude 或其他编码智能体运行默认的单配方路径，方法是加载 HermesBench skill 并保存产物。
- 完整 bundle 运行是可选的，因为它们更耗时，也更贵。
- 评分会奖励有用的完成、真实的不确定性、安全行为、稳定性、及时响应和清晰沟通；失衡的分数会被扣分。

## 结果
- 已发布的基线分数是 78.2，覆盖 27 个个人智能体配方。
- 捆绑目录覆盖 10 个工作流领域：上下文、日历、网页、报告、沟通、位置、旅行、财务、安全，以及高级用户集成。
- 公开站点有 3 个证据标签页，分别是配方、配置档案和轨迹。
- 摘录提到 1 个早期公开基线，并说明这不是基础模型排行榜。
- 摘录没有提供按轴分数、置信区间、失败次数，也没有和其他智能体基准的比较。

## Problem

## Approach

## Results

## Link
- [https://verkyyi.github.io/hermesbench/](https://verkyyi.github.io/hermesbench/)
