---
source: arxiv
url: http://arxiv.org/abs/2604.23455v1
published_at: '2026-04-25T22:10:53'
authors:
- Haoming Meng
topics:
- llm-agents
- failure-diagnosis
- benchmarking
- cross-modal-reasoning
- browser-to-backend
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# CUJBench: Benchmarking LLM-Agent on Cross-Modal Failure Diagnosis from Browser to Backend

## Summary
## 概要
CUJBench 是一个用于诊断软件故障的基准，这类故障从浏览器中可见的症状开始，并延伸到后端遥测。它把每个事件都封装为确定性的快照，因此可以在同一个跨模态诊断任务上比较不同的 LLM 代理。

## 问题
- 现有根因分析基准主要关注后端日志、追踪和指标，而网页代理基准主要关注在正常应用中完成任务。两者都不测试把浏览器中的用户旅程故障与后端原因关联起来的诊断能力。
- 真实的事故诊断通常从截图、网络请求或控制台错误开始，然后再查看追踪、日志和近期变更。现有基准缺少这种从浏览器到后端的推理路径。
- 在线环境会引入噪声，使代理之间的比较不可靠，因此有用的基准需要固定证据和可重复的工具输出。

## 方法
- 论文构建了 **CUJBench**，这是一个由失败的关键用户旅程（CUJ）组成的基准，形式是冻结的多模态快照，包含前端证据、后端可观测性数据和运维上下文。
- 它使用两个开源应用 OpenTelemetry Demo 和 Tractor Store，以覆盖以后端为主、以浏览器为主以及跨模态的故障。
- 该语料库包含 **87 个带标签的场景**，覆盖 **五类故障家族**：baseline、browser proxy faults、backend flag faults、compound faults 和 frontend mutations。
- 场景创建使用了一个 **LLM 辅助生成流水线**，先生成 **120 个候选场景**，再通过一个多代理审查流程进行筛选，其中包括两名 SRE 审查者、一名高级审查者和人工核验。最终有 **120 个中的 87 个** 场景被纳入。
- 评估使用固定的工具接口和确定性的缓存响应，其中包括截图和 HAR/网络数据等浏览器工具、日志和追踪等后端工具，以及近期变更和服务拓扑等上下文工具。

## 结果
- 在该基准上，六个前沿模型的 **总体准确率只有 19.7%**，报告的 **上限为 52%**，说明这个任务远未解决。
- 论文在 **三种基线** 下评估了 **六个模型**：仅检索、仅浏览器和完整工具集。
- 一个主要的经验结论是，**仅浏览器代理的整体表现优于完整工具集代理**，这说明额外工具常常会让代理进行范围更大但焦点更差的证据搜索。
- 基准分析认为，主要瓶颈是 **跨模态综合**：代理经常能检索到关键信息，但无法把它正确关联到真实原因。
- 论文引用的先前仅后端研究显示，在 OpenRCA 上，五个前沿模型的完整 RCA 准确率只有 **3.9% 到 12.5%**，这说明 CUJBench 是一个更难、范围更广的诊断场景。
- 该摘录没有给出每个模型的分数表、按数据集划分的指标，或仅浏览器与完整工具集之间的具体差值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23455v1](http://arxiv.org/abs/2604.23455v1)
