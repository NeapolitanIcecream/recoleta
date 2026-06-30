---
source: arxiv
url: https://arxiv.org/abs/2606.30573v1
published_at: '2026-06-29T17:17:45'
authors:
- Mohit Raghavendra
- Anisha Gunjal
- Aakash Sabharwal
- Yunzhong He
topics:
- coding-agents
- swe-benchmark
- multi-turn-evaluation
- user-simulation
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions

## Summary
## 摘要
SWE-INTERACT 在多轮软件任务中测试编码代理：模拟用户先提出模糊请求，检查代码，再逐步披露需求。在相同的底层任务上，这种设置把顶尖模型的解决率从约 50% 降到约 25–27%，同时增加步骤数、token 数和成本。

## 问题
- 标准 SWE 基准在一个提示中给代理完整任务规格，但许多真实的编码代理会话从简短、不完整的用户请求开始，并经过多轮审查。
- 现有的 user-in-loop SWE 基准通常从较清晰的提示开始，或使用无法检查工作区的用户模拟器，因此遗漏了目标发现、修订和需求保持。
- 这一点很重要，因为能解决完整规格任务的代理，在面对通过反馈披露约束的开发者时仍可能失败。

## 方法
- 作者将 75 个任务转换为交互式会话：分别来自 SWE-bench Pro、SWE Atlas Refactoring 和 DeepSWE，各 25 个。
- 每个任务保留原始 Docker 环境和最终验证器，但完整需求集隐藏在用户模拟器中。
- 模拟器使用基于 SWE-chat 数据的 Expert Nitpicker 人设：短消息、精确的 API 关注点、迭代式批评，以及延迟披露需求。
- 模拟用户可以用 `git`、`grep`、`sed` 和 `find` 等工具检查代理工作区，然后通过 Harbor 中的 `ask_user` 工具给出有依据的反馈。
- 代理保存初始 `PLAN.md`，并在用户反馈后提交修订，这让作者能够衡量目标发现，并沿轨迹审计失败。

## 结果
- 最好的单轮解决率是 Opus 4.8 的 50.7% 和 GPT 5.5 的 48.0%；在 SWE-INTERACT 中，它们分别降到 26.7% 和 24.7%，下降 24.0 和 23.3 个百分点。
- 所有 5 个被评估的代理在多轮模式下得分都更低：Kimi K2.6 从 25.3% 降到 14.7%，Gemini 3.5 Flash 从 29.3% 降到 17.3%，Sonnet 4.6 从 21.3% 降到 18.8%。
- 多轮运行使用更多计算资源。GPT 5.5 每次试验的步骤数从 108.6 增至 424.8，token 数从 0.14M 增至 0.36M，成本从 $2.78 增至 $9.84。
- 交互轨迹平均每次试验约有 7 条用户消息；一次长运行包含 27 条用户消息、332 次用户工具调用，以及超过 1000 个代理步骤。
- 目标发现不能保证正确性：GPT 5.5、Opus 4.8 和 Sonnet 4.6 最终平均处理了超过 90% 的任务目标，但许多最终补丁仍未通过验证器。
- 在 287 条失败轨迹中，最常见的语义失败标签是技术实现错误和遗忘需求，各约占所分配标签的三分之一；误解或错误假设约占 14%，遗漏用户需求约占 12%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30573v1](https://arxiv.org/abs/2606.30573v1)
