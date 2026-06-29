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
RCLAgent 通过把 LLM 智能体映射到 trace span，并沿 trace 图并行诊断，定位微服务故障的根因。它针对基于 LLM 的根因定位中的上下文增长和串行工具调用延迟问题。

## 问题
- 微服务故障会扩散到服务、Pod、节点、日志、指标和 trace，表面症状可能掩盖真正引发事故的组件。
- 现有的图方法和深度学习方法在不同部署之间可能难以迁移，也可能不易解释。
- 现有的 LLM 方法常把过多运行时证据塞进不断扩大的上下文里，并按步骤逐层推理，这会丢失早期信号并拖慢诊断。

## 方法
- RCLAgent 给每个 trace span 分配一个专用智能体，让每个智能体只检查请求路径中的一小部分局部内容。
- 每个智能体使用 trace、日志和指标工具分析自己的 span，然后接收来自子智能体的压缩证据，而不是原始下游数据。
- 智能体按 trace 图递归工作：父智能体把自己的局部发现与子报告合并，再向上传递一个简短假设。
- 独立分支并行运行，智能体池限制并发智能体数量以控制成本。
- 根智能体使用 Root-Level Diagnosis Report 和 Global Evidence Graph 做最终诊断，后者保留可供审查的局部假设。

## 结果
- 论文在 AIOPS 2022、Augmented-TrainTicket 和 RCAEval 上评估了 RCLAgent。
- 论文称，RCLAgent 在测试基准上的准确率比第二好的根因定位方法平均高约 7.51%。
- 论文称，它的推理速度比现有基于 LLM 的方法快超过 1.75×。
- 这项实证研究采访了来自北京大学和华为 Theory Lab 的 15 名开发者和 SRE。
- 对单智能体 ReAct 风格 CoT 基线在 AIOPS 2022 中 100 个失败案例的事后分析显示，43 个失败与证据稀释有关，57 个与浅层推理有关；这 43 个证据稀释案例里包括 8 个丢失根因案例和 35 个根因降级案例。
- 实验中的失败定义把请求的 entry span 延迟超过正常平均延迟 100 倍视为异常。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14866v1](https://arxiv.org/abs/2605.14866v1)
