---
source: hn
url: https://role-model.dev/
published_at: '2026-06-28T22:16:36'
authors:
- handfuloflight
topics:
- ai-routing
- model-orchestration
- capability-aware-routing
- llm-infrastructure
- agent-runtime
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Role-model: protocol for assigning the right AI model for the right job

## Summary
## 摘要
role-model 提出了一套开放协议和参考运行时，用于根据任务需求、能力、策略和实测性能把 AI 请求路由到端点。使用多个模型的系统需要这种做法，因为路由决策需要可检查、可移植，并且要和具体端点的行为相关联。

## 问题
- 多模型系统需要一种持久方式来说明请求需要什么、适用哪些角色和任务、哪些端点可以完成工作，以及哪些策略允许这次调用。
- 按模型标签路由，对能力匹配、成本、本地性、工具、模态和回退行为的控制较弱。
- 运营人员需要审计记录，说明为什么选择或排除了某个端点。

## 方法
- 请求携带任务类型、所需能力、模态、工具需求、约束和策略上下文。
- 该协议把角色、任务、端点身份、端点配置、路由策略和可观测性产物描述为可单独检查的对象。
- 参考路由器按角色、任务、策略范围、能力、模态、工具支持、本地性、预算和绑定规则筛选端点。
- 符合条件的端点会按实测质量、延迟、吞吐量、成本、可靠性和偏好数据评分；缺少测量数据时使用声明数据和中性默认值。
- 运行时返回 RouterDecision，其中包含选定端点、回退端点、排除项和选择理由。

## 结果
- 摘录报告了 0 个定量基准结果：没有提供准确率、延迟、吞吐量、成本、可靠性或路由质量测量数据。
- 其声称的产出是一套打包的参考运行时，加上一套可供客户端和运营人员检查的开放路由协议。
- 路由器使用 5 阶段决策流程：规范化意图、缩小候选范围、执行资格检查、为端点评分，并输出决策。
- 首次运行设置列出 7 个操作步骤：安装运行时、连接端点、激活模型和角色、运行基准测试、查看结果、选择策略，并验证一次已路由的请求。
- 最具体的主张是：使用角色、任务、声明能力、策略和观测到的性能，在具体端点之间进行可解释路由。

## Problem

## Approach

## Results

## Link
- [https://role-model.dev/](https://role-model.dev/)
