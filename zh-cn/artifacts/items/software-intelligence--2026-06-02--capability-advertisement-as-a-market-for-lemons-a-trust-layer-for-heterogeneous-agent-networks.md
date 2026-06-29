---
source: arxiv
url: https://arxiv.org/abs/2606.03034v1
published_at: '2026-06-02T02:17:30'
authors:
- Gaurav Naresh Mittal
topics:
- agent-networks
- trust-reputation
- capability-advertising
- multi-agent-systems
- mcp-a2a
- llm-reliability
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Capability Advertisement as a Market for Lemons: A Trust Layer for Heterogeneous Agent Networks

## Summary
## 摘要
这篇论文认为，MCP、A2A 和函数调用式的代理广告会让不可靠代理看起来和可靠代理一样。论文提出了一个 Trust Layer，在现有代理协议之上加入可靠性声明、测试、证明、声誉和漂移检查。

## 问题
- 现有代理广告只描述如何调用某个工具或技能，但不会说明它多久能成功、什么时候会失败、声明依据是什么，或者这个声明何时失效。
- 在开放的代理网络中，调用方看到的是公开宣称的能力，而不是真实可靠性。这会形成一个“柠檬市场”，便宜的夸大宣传可能挤出对可靠代理的投入。
- 这里对应的失败类型是“confident-wrong”：代理给出流畅、完整、错误的回答，却没有错误信号。经典的崩溃、超时和 Byzantine 处理方式并不适合这种概率性、相关性的失败模式。

## 方法
- 核心机制很直接：用有证据支撑的可靠性声明替代布尔式能力声明，然后随时间测试并跟踪这些声明。
- 概率型能力描述符加入了估计可靠性、基准名称、样本量、评估日期、输入限制、后端版本和过期时间等字段。
- 筛查使用调用方挑战、金丝雀任务和第三方证明。证明应包含可复现、带签名的评估记录，并可发布到仅追加日志中。
- 声誉记录会在检查后的结果、挑战、矛盾或下游验证之后更新。版本变化和过期描述符会触发重新检查，以捕捉漂移。
- 论文用信号传递、筛查和重复博弈中的声誉来建模这个系统。当维持夸大声明的成本 c 大于一次性夸大的收益 g 时，会出现区分均衡。

## 结果
- 论文没有给出真实部署测量，也没有新的 LLM 基准结果。结论来自分析和一个说明性的 Python 仿真。
- 级联委派的可靠性会相乘：在独立性假设下，3 跳链路每跳可靠性为 85%，端到端可靠性约为 61%。
- 在仿真中，低和高真实可靠性分别设为 rL = 0.55 和 rH = 0.92，因此夸大声明的收益 g = 0.37。
- 在基于信任的广告下，仿真的实际可靠性降到 rL = 0.55，真正投入可靠性的提供者比例在 24 个随机种子下接近 0。
- 在 Trust Layer 且 c = 1.5g 时，仿真可靠性保持在 rH = 0.92 附近，投入比例稳定在 0.58，接近预测值 0.583。
- 筛查成本扫描声称在 c = g 处出现明显转折：当 c 大于 g 时，在模型里夸大不再有利，诚实的能力信号可以把可靠和不可靠的提供者区分开来。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03034v1](https://arxiv.org/abs/2606.03034v1)
