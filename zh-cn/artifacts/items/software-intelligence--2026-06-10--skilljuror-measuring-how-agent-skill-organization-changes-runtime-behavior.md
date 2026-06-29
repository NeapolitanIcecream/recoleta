---
source: arxiv
url: https://arxiv.org/abs/2606.11543v1
published_at: '2026-06-10T01:11:50'
authors:
- Zhiyu Chen
- Zihan Guo
- Bo Huang
- Bingwei Lu
- Jianghao Lin
- Yuanjian Zhou
- Weinan Zhang
topics:
- agent-skills
- llm-agents
- skill-evaluation
- runtime-behavior
- procedural-knowledge
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior

## Summary
## 摘要
SkillJuror 测试在内容不变时，重新组织 Agent Skill 是否会改变大语言模型代理在运行时的行为。在 82 个 SkillsBench 任务上，Progressive Disclosure 提高了轨迹中的资源使用，并且相比扁平 Skill 基线带来了小幅通过率提升。

## 问题
- Agent Skill 基准测试常常比较不同的 Skill，这会把内容覆盖、作者风格、辅助工具可用性和组织方式混在一起。
- 这很重要，因为团队需要的是关于 Skill 应该怎么写的证据，而不只是加上 Skill 是否有帮助。
- 这篇论文研究的，是仅靠 Skill 组织方式是否就能改变代理的搜索、资源访问、实现、检查和修复行为。

## 方法
- SkillJuror 为每个 Skill 构建两个匹配版本：一个规范化的扁平基线版本，一个采用 Progressive Disclosure 的版本，后者用简短的 `SKILL.md` 指向支持文件。
- 两个版本保持相同的任务范围、命令、辅助契约、约束、数值阈值、schema 和输出规则。
- 系统通过确定性门控、基于评分表的语义审计，以及对标记案例的人审来检查这些变体。
- 它在同一个 Harbor 支持的沙箱中运行匹配试验，使用相同的模型、任务环境、验证器、超时设置和推理设置。
- 它测量验证器通过率、成本、时间、token 使用量、触达的资源数量，以及 Effective Resource Uptake，其中 uptake 指代理在实现、验证、更正或定位阻塞原因时使用了某个资源。

## 结果
- 主要运行时研究：82 个 SkillsBench 任务 × 3 个条件 × 5 次试验 = 1,230 次试验；每个条件有 410 次试验。
- 通过率从扁平基线的 172/410（42.0%）提高到 Progressive Disclosure 的 189/410（46.1%），增加了 17 个验证器通过的试验，即 +4.1 个百分点。
- No-Skill 得分为 119/410，29.0%，所以两个 Skill 版本在总体通过率上都优于无 Skill 条件。
- 每条轨迹触达的不同 Skill 资源数从扁平基线的 1.18 上升到 Progressive Disclosure 的 3.85。
- Effective Resource Uptake 事件数从每条轨迹 1.33 次上升到 3.92 次。
- 按产出归一化后的效率从基线的 20.1 分钟/通过、0.22M token/通过 和 $1.28/通过，变为 Progressive Disclosure 的 17.8 分钟/通过、0.21M token/通过 和 $1.31/通过；收益依赖任务，在精确输出规范、数值阈值和长篇产物生成流水线上更弱。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.11543v1](https://arxiv.org/abs/2606.11543v1)
