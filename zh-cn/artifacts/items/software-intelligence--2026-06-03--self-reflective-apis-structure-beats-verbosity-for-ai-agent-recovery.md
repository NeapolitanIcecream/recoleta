---
source: arxiv
url: https://arxiv.org/abs/2606.05037v1
published_at: '2026-06-03T16:02:11'
authors:
- Arquimedes Canedo
- Grama Chethan
topics:
- llm-agents
- api-error-recovery
- structured-feedback
- agent-tool-use
- benchmark-leakage
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Self-Reflective APIs: Structure Beats Verbosity for AI Agent Recovery

## Summary
## 摘要
自反思式 API 在验证错误中加入机器可读的修复建议，这样 AI 代理就能修复失败的 API 调用并重试。论文报告称，在对抗性 API 恢复任务上，Anthropic 模型的提升很大；在试点中，gpt-4o-mini 没有显著提升。

## 问题
- AI 代理在 API 验证错误后常常失败，因为普通错误信息只说明哪里错了，却没有给出恢复所需的具体请求修改。
- 当 API 执行的是领域特定或专有规则时，这个问题最明显，比如认证无麸质品牌、菜系限制、酸面团工艺或精确缩放数值。
- 纯英文、冗长的错误信息会在基准测试中泄露答案，所以论文也把泄露审计当作评估问题的一部分。

## 方法
- API 在验证失败时返回一个顶层 `recovery_feedback` 对象，其中的 `suggestions[]` 数组包含类型化操作和下一次请求要用的字面参数值。
- 一个重试循环代理最多调用 API 5 次，把建议中的参数合并到下一次请求里，并在不改动验证器或业务逻辑的情况下重试。
- 实验比较 3 种响应模式：传统通用错误、传统的逐条冗长诊断但不给出字面修复、以及带结构化建议的反思式诊断。
- 主要测试场景是一个食谱转换 API，包含 10 个对抗性任务，覆盖配料兼容性、乳糜泻认证、数值精度和多错误恢复。
- 作者审计了两条泄露路径：会暴露修复方法的验证器消息，以及暴露成功标准的任务提示。

## 结果
- 试点设计：10 个任务 × 3 种模式 × 3 次运行 × 3 个 LLM，每个模型/模式单元有 30 次尝试。
- 在 Anthropic 模型上，结构化建议比纯英文诊断提高了 +36.7 到 +40.0 个百分点的任务完成率，Fisher 精确检验 p ≤ 0.0022。
- 与 Verbose 基线相比，claude-haiku-4-5 的单位成功 token 效率提高 1.8 倍，claude-sonnet-4-6 提高 2.2 倍。
- 在 gpt-4o-mini 上，提升为 +13.3 个百分点，且没有统计显著性：p = 0.435。
- 对 gpt-4o-mini 而言，Reflective 和 Verbose 的单位成功 token 使用接近：3,548 对 3,665 token。
- 文摘称作者在第二个领域的账单 API 上做了复现，以确认这一模式，但没有给出详细数值结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05037v1](https://arxiv.org/abs/2606.05037v1)
