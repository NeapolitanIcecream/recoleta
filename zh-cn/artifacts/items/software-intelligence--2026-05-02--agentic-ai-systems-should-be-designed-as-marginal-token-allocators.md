---
source: arxiv
url: https://arxiv.org/abs/2605.01214v1
published_at: '2026-05-02T03:06:02'
authors:
- Siqi Zhu
topics:
- agentic-ai
- token-allocation
- coding-agents
- llm-routing
- serving-systems
- rl-training
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic AI Systems Should Be Designed as Marginal Token Allocators

## Summary
## 摘要
本文认为，代理式 AI 系统应按每增加一个 token 的预期质量收益减去计算、延迟和风险成本来分配 token。它用一个编码代理的请求说明路由、代理动作、服务和训练如何都服从同一套分配规则。

## 问题
- 统一的按 token 记账会把模型选择、规划、验证、KV cache 使用和 RL rollout 当成同一种成本，尽管它们对质量、延迟和风险的影响不同。
- 局部优化会浪费 token：便宜的路由选择可能迫使代理做更多验证，制造服务拥塞，并生成更差的训练轨迹。
- 这对编码代理和其他会采取行动的系统很重要，因为减少 token 可能会提高错误提交、遗漏测试、缓存陈旧和服务变慢的代价。

## 方法
- 论文把每一种可能的 token 用法都定义为一个选项：便宜模型、前沿模型、检索、规划、工具调用、验证器、prefill、decode、KV 传输、RL rollout、奖励计算或梯度更新。
- 核心规则很简单：把下一个 token 用在 `任务价值 × 边际质量收益 - 计算成本 - 延迟成本 - 风险成本` 最大的地方。
- 它把同一规则映射到 4 层：路由作为模型筛选，代理策略作为规划-行动-验证分配，服务作为 prefill/decode/KV 生产，训练作为对未来能力的投入。
- 它提出为计算、延迟和风险设定共享影子价格，让上游选择能计入下游成本。
- 它把常见故障转成定价错误：过度路由、过度委派、验证不足、服务拥塞、滚动更新陈旧和缓存误用。

## 结果
- 这是一篇立场论文，没有报告任何实证基准提升、消融实验或生产环境测量。
- 论文给出一个路由示例：便宜模型质量为 `0.7`、成本为 `1`，前沿模型质量为 `0.9`、成本为 `5`；当任务价值超过 `20` 且没有风险时，前沿模型更优。
- 在同一示例中，加入错误动作概率后，便宜模型为 `0.05`，前沿模型为 `0.01`，风险价格为 `50`，交叉点会移到约 `10`。
- 论文声称一个一阶条件覆盖 `4` 个系统层面：需求、行动、供给和资本。
- 它指出 `6` 种常见故障都能用误定价的边际 token 解释：过度路由、过度委派、验证不足、拥塞、滚动更新陈旧和缓存误用。
- 它建议用于评估和运行的具体产物包括：基于后悔值的路由评估、按动作类别制定自治计划，以及记录 prefill、decode 和 KV 资源的影子价格。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01214v1](https://arxiv.org/abs/2605.01214v1)
