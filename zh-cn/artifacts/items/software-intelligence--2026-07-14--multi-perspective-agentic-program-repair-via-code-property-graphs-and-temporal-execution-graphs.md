---
source: arxiv
url: https://arxiv.org/abs/2607.12605v1
published_at: '2026-07-14T10:33:29'
authors:
- Zhili Huang
- Ling Xu
- Hongyu Zhang
topics:
- automated-program-repair
- code-intelligence
- multi-agent-software-engineering
- program-analysis
- agentic-software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Multi-Perspective Agentic Program Repair via Code Property Graphs and Temporal Execution Graphs

## Summary
## 摘要
CT-Repair 通过将静态证据和运行时证据组织为可查询图，并为静态、动态和混合诊断分别分配代理，改进了自动程序修复。在 Defects4J v3.0 上，CT-Repair 在混合模型配置下正确修复了 854 个 Java 缺陷中的 489 个；在受控的 GPT-5.4-mini 配置下正确修复了 388 个缺陷。

## 问题
- 原始执行轨迹规模庞大且重复，使语言模型难以检索相关的故障证据；一项针对 100 个缺陷的研究发现，每个缺陷平均包含 238 万个运行时事件，其中 99.95% 被归类为重复事件。
- 重复采样补丁可能产生不同的实现，却无法产生不同的根因假设或修复策略。
- 该问题之所以重要，是因为 APR 需要紧凑的行为证据和真正多样化的诊断，才能在有限的模型上下文和生成预算内修复复杂缺陷。

## 方法
- CT-Repair 使用 Joern 构建代码属性图，表示语法、控制流、数据流和调用关系；同时构建时间执行图，表示带时间戳的方法调用、状态、分支和执行顺序。
- 三阶段过滤流程会在构建 TEG 之前，移除未执行的方法、结构简单的方法，以及与有效执行流不相连的运行时记录。
- 三个由有限状态机引导的代理分别从静态、动态和混合视角独立分析每个缺陷，查询相关图证据，形成根因假设，并提出修复策略。
- 策略引导的轮流生成流程将每个策略转化为候选补丁，通过编译和测试对其进行验证，评估修复的失败数量与引入的新失败数量，并在必要时进一步优化表现最强的策略。

## 结果
- 在 Defects4J v3.0 的 854 个真实世界 Java 缺陷上，CT-Repair 在混合模型配置下正确修复了 489 个缺陷。
- 在使用 GPT-5.4-mini 的受控对比中，CT-Repair 正确修复了 388 个缺陷，比 ReinFix 多 19 个，比 RepairAgent 多 30 个；相对于 ReinFix，论文报告的相对提升为 5.15%。
- 结合静态、动态和混合视角后，修复的缺陷数量比表现最强的单一视角多 99 个，这支持这些推理路径之间具有互补性。
- 执行过滤平均将候选方法范围缩小 94.85%，行为过滤则在此基础上进一步减少 55.97% 的保留运行时记录。
- 证据仅限于 Defects4J Java 基准，并采用完美故障定位；该摘录无法证明其在其他语言、基准或不完美故障定位设置下的性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.12605v1](https://arxiv.org/abs/2607.12605v1)
