---
source: arxiv
url: https://arxiv.org/abs/2605.14866v1
published_at: '2026-05-14T14:13:59'
authors:
- Lingzhe Zhang
- Tong Jia
- Kangjin Wang
- Chiming Duan
- Minghua He
- Rongqian Wang
- Xi Peng
- Meiling Wang
- Gong Zhang
- Renhai Chen
- Ying Li
topics:
- multi-agent-systems
- llm-agents
- microservice-observability
- root-cause-localization
- aiops
- software-reliability
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Towards In-Depth Root Cause Localization for Microservices with Multi-Agent Recursion-of-Thought

## Summary
## 摘要
RCLAgent 通过将 LLM 智能体映射到 trace span，并沿 trace graph 并行执行诊断，定位微服务故障的根因。它针对的是基于 LLM 的根因定位中的上下文增长和串行工具使用延迟问题。

## 问题
- 微服务故障会跨服务、pod、节点、日志、指标和 trace 扩散，因此表层症状可能掩盖导致事故的组件。
- 现有图方法和深度学习方法可能难以跨部署迁移，或难以解释。
- 现有 LLM 方法常把过多运行时证据混入一个不断增长的上下文，并逐步推理，这可能丢失早期信号并拖慢诊断。

## 方法
- RCLAgent 为每个 trace span 分配一个专用智能体，使每个智能体检查请求路径中的一个小型局部部分。
- 每个智能体为自己的 span 使用 trace、日志和指标工具，然后接收来自子智能体的紧凑证据，而不是原始下游数据。
- 智能体按 trace graph 递归执行：父智能体把自己的局部发现与子报告合并，并向上传递简短假设。
- 独立分支并行运行，同时由智能体池限制并发智能体数量以控制成本。
- 根智能体使用 Root-Level Diagnosis Report 和 Global Evidence Graph 做出最终诊断，后者保留局部假设以供审查。

## 结果
- 论文在 AIOPS 2022、Augmented-TrainTicket 和 RCAEval 上评估了 RCLAgent。
- 论文称，在测试基准上，RCLAgent 的准确率比次优根因定位方法高约 7.51%。
- 论文称，相比现有基于 LLM 的方法，推理速度提升超过 1.75×。
- 实证研究包括对来自北京大学和 Huawei Theory Lab 的 15 名开发者和 SRE 的访谈。
- 在对单智能体 ReAct-style CoT 基线的 100 个失败 AIOPS 2022 案例进行事后分析时，43 个失败涉及证据稀释，57 个涉及浅层推理；43 个证据稀释案例包括 8 个根因丢失案例和 35 个根因降级案例。
- 实验中的失败定义为：当请求的入口 span 延迟超过正常平均延迟的 100× 时，该请求被视为异常。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14866v1](https://arxiv.org/abs/2605.14866v1)
