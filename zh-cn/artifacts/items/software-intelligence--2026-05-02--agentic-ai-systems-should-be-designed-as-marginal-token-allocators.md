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
## 概要
论文主张，智能体式 AI 系统应按预期质量收益减去计算、延迟和风险成本来分配每个新增 token。它用一个编码智能体请求说明路由、智能体动作、服务和训练如何纳入同一条分配规则。

## 问题
- 扁平的逐 token 核算把模型选择、规划、验证、KV 缓存使用和 RL rollout 视为同一类成本，但它们对质量、延迟和风险的影响不同。
- 局部优化可能浪费 token：廉价的路由选择可能迫使智能体做额外验证，造成服务拥塞，并产生质量较低的训练轨迹。
- 这对编码智能体和其他会采取行动的系统很重要，因为削减 token 可能提高错误提交、漏测、过期缓存和服务变慢的成本。

## 方法
- 论文把每种可能的 token 用法定义为一个选项：廉价模型、前沿模型、检索、规划、工具调用、验证器、prefill、decode、KV 传输、RL rollout、奖励计算或梯度更新。
- 核心规则很简单：把下一个 token 花在 `task value × marginal quality gain - compute cost - latency cost - risk cost` 最高的地方。
- 它把同一条规则映射到 4 个层次：路由是模型筛选，智能体策略是规划-行动-验证分配，服务是 prefill/decode/KV 生产，训练是对未来能力的投资。
- 它提出对计算、延迟和风险使用共享影子价格，让上游选择能计入下游成本。
- 它把常见故障归结为定价错误：过度路由、过度委派、验证不足、服务拥塞、过期 rollout 和缓存误用。

## 结果
- 这是一篇立场论文，没有报告经验基准收益、消融结果或生产环境测量。
- 它给出一个路由示例：廉价模型质量为 `0.7`、成本为 `1`，前沿模型质量为 `0.9`、成本为 `5`；在不考虑风险时，当任务价值超过 `20`，前沿模型更优。
- 在同一示例中，加入廉价模型 `0.05`、前沿模型 `0.01` 的错误行动概率，并设置风险价格 `50` 后，交叉点移到约 `10`。
- 它声称一个一阶条件覆盖 `4` 个系统层次：需求、行动、供给和资本。
- 它识别出 `6` 种由边际 token 定价错误解释的反复出现的故障模式：过度路由、过度委派、验证不足、拥塞、过期 rollout 和缓存误用。
- 它建议用于评估和运行的具体产物：基于 regret 的路由器评估、按行动类别制定的自主性计划，以及针对 prefill、decode 和 KV 资源记录的影子价格。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01214v1](https://arxiv.org/abs/2605.01214v1)
