---
source: arxiv
url: https://arxiv.org/abs/2607.02294v1
published_at: '2026-07-02T15:11:39'
authors:
- Zimo Ji
- Zekai Zhang
- Congying Xu
- Zongjie Li
- Yudong Gao
- Shuai Wang
- Shing-Chi Cheung
topics:
- coding-agents
- devops-safety
- code-intelligence
- agent-benchmarks
- human-ai-interaction
- software-automation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Coding Agents Are Guessing: Measuring Action-Boundary Violations in Underspecified DevOps Instructions

## Summary
## 摘要
UnderSpecBench 测试编码代理在 DevOps 指令省略预期动作、目标或范围时是否会猜测。在 OpenCode、Claude Code 和 Codex 的配置中，论文发现代理经常在语义不明确时采取行动，并越过动作边界。

## 问题
- 编码代理可以运行 shell 命令、编辑代码库并调用运维 API，因此在错误分支、命名空间、数据库、路由或制品上执行看似合理的动作，可能造成实际损害。
- 现有代理基准大多按任务完成情况打分。它们会漏掉一种情况：任务看起来已经完成，但代理触碰了错误对象，或使用了超出用户授权范围的命令。
- 论文关注良性的、未充分说明的 DevOps 请求，例如清理、回滚、裁剪和访问权限变更。在这些请求中，安全回应可能是要求澄清。

## 方法
- 作者构建了 UnderSpecBench，包含 69 个 DevOps 任务族，这些任务基于有记录的事故、CVE 或工具行为。
- 每个任务有 32 个提示变体，由 4 个意图清晰度等级、4 个目标确定性等级和 2 个影响范围等级交叉生成，共 2,208 个提示。
- 环境和真实安全动作保持不变，只有指令发生变化，因此行为变化可以归因于未充分说明。
- 每个任务的确定性判定器会检查状态差异、命令日志和服务端副作用，并将结果分类为 Safe Success、Wrong Target 和 OverScope。
- 未采取行动的运行会使用 DeepSeek-v4-flash 对最终消息进行判断，并分类为 Ask、Refuse 或 Defer。

## 结果
- 研究在全部 69 个任务族和 2,208 个提示变体上评估了 5 个代理-模型配置：OpenCode 搭配 Haiku-4.5、Codex-5.1-mini 和 DeepSeek-v4；Claude Code 搭配 Haiku-4.5；Codex 搭配 Codex-5.1-mini。
- Safe Success 率从 Codex + Codex-5.1-mini 的 15.5% 到 OpenCode + DeepSeek-v4 的 36.8% 不等。
- 在所有计分运行中，越界率从 Claude Code + Haiku-4.5 的 27.0% 到 OpenCode + DeepSeek-v4 的 46.3% 不等；在已采取行动的运行中，论文报告的边界违规率为 55.8–67.8%。
- Wrong Target 率在不同配置中为 13.1% 到 31.8%，OverScope 率为 24.9% 到 44.4%。
- Under Completion 率为 38.3% 到 69.2%，说明许多运行在没有触发判定器可识别的安全或不安全动作时就停止了。
- 目标未充分说明与 Wrong Target 行为的关联最强；意图未充分说明的影响较弱，影响范围提示对代理是否采取行动影响很小。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02294v1](https://arxiv.org/abs/2607.02294v1)
