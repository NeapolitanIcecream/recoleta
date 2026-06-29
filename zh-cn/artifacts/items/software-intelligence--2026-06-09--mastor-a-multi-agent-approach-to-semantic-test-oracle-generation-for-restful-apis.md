---
source: arxiv
url: https://arxiv.org/abs/2606.10465v1
published_at: '2026-06-09T06:35:21'
authors:
- Sida Deng
- Rubing Huang
- Zhenzhen Yang
- Man Zhang
- Xuan Xie
- Rongcun Wang
topics:
- rest-api-testing
- test-oracle-generation
- multi-agent-systems
- code-intelligence
- automated-testing
- llm-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs

## Summary
## 摘要
MASTOR 通过读取实现源码并协调基于 LLM 的智能体，为 RESTful API 生成语义测试 Oracle。它针对的是状态码检查、崩溃检查和模式检查常常遗漏的故障。

## 问题
- REST API 测试通常只验证 HTTP 状态码、运行时失败或模式符合性，因此可能漏掉业务逻辑错误和依赖状态的不一致。
- 正确行为可能取决于控制器分支、服务逻辑、仓库调用、模型字段、异常路径，以及端点之间的关系。
- 仅看 API 规范，可能会遗漏输入长度限制、响应字段过滤规则，以及隐藏在成功 HTTP 响应后的副作用。

## 方法
- MASTOR 分为两个阶段：源码分析和 Oracle 生成。
- 源码提取智能体通过读取相关源文件的传递导入闭包，为每个端点构建 Source 上下文，并记录输入约束、响应模式和源码证据。
- 单操作路径基于源码事实，为每个端点生成状态 Oracle 和字段 Oracle。
- 多操作路径利用源码分析阶段发现的跨操作关联，为端点序列生成行为一致性 Oracle。
- Challenger 智能体会审查生成的 Oracle，给出修复提示，触发定向重生成，然后由归一化步骤过滤结构无效的 Oracle。

## 结果
- 该基准包含来自 WFD 和 PRAB 的 13 个开源 RESTful API 项目、296 个端点操作和 251,303 行代码。
- MASTOR 生成了 10,022 个 Oracle，在这 13 个 API 上的平均变异得分为 75.4%。
- 单个 API 的变异得分介于 69.0% 到 95.9% 之间。
- 在 50 个选定端点操作上，仅使用状态和字段 Oracle 时，MASTOR 得分为 69.9%，Direct Prompting 为 39.8%，提高了 30.1 个百分点。
- 在同样的 50 个操作对比中，MASTOR 得分为 69.9%，SATORI 为 20.5%，提高了 49.4 个百分点。
- 报告的中位推理成本为每个 API 0.56 美元，使用的是 DeepSeek V4 Pro 和 Qwen3.6-Plus。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10465v1](https://arxiv.org/abs/2606.10465v1)
