---
source: arxiv
url: https://arxiv.org/abs/2606.02494v1
published_at: '2026-06-01T17:01:53'
authors:
- Marisa Ferrara Boston
- Glen Hanson
- Effi Georgala
- JD Hudgens
- Heather Frase
topics:
- agentic-systems
- agent-monitoring
- ai-ops
- fmea-triage
- reliability-engineering
- human-in-the-loop
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Monitoring Agentic Systems Before They're Reliable

## Summary
## 概述
本文主张，早期生产中的 agentic 系统需要先做结构监控，任务级错误检测才会有效。作者在一个合成的审计代理测试床上测试了基于方差的监控和 FMEA 分流方法，发现监控范围可以预测发现的故障类型。

## 问题
- 早期 agentic 系统常因阶段、工具或数据路径集成不良而失败，因此任务级监控可能看不到真正原因。
- 在审计、金融、医疗和法律服务等受监管流程中，平均准确率和阈值告警会掩盖少见但高风险的故障。
- 人工审阅者需要按严重程度分流，因为原始监控结果可能带来超出团队处理能力的复核工作量。

## 方法
- 该方法从三个维度评估代理行为：质量、适配性和效率。
- 它使用三种监控范围：单次运行内监控用于观察一次执行中的变化，跨运行监控用于观察重复执行之间的变化，结构监控用于发现集成缺口。
- 方差是主要信号。论文对大多数评估器使用 2.0 的 z 分数阈值，对时间敏感评估器使用 3.0 的阈值，并用变异系数来刻画监控类别。
- 结果进入一个 FMEA 风格的分流流程，分为四个严重级别：L1 灾难性、L2 严重、L3 边缘、L4 可忽略。
- 评估使用 120 组合成审计文档包：20 组干净文档包和 100 组错误文档包，覆盖 5 种错误子类型、4 个难度等级，以及每个单元格 5 个文档集，总计 220 次运行。

## 结果
- 单次运行内监控发现了方差很低的确定性阶段缺陷：CV = 0.02。这些结果数量多，严重程度低，主要是 L3。
- 跨运行监控发现了方差很高的随机性集成后果：CV = 1.25，其中 24% 的结果被归为 L2 严重。
- 结构监控发现了一个集成缺口，而且在各次运行中完全一致：CV = 0.00。
- 注入的任务级错误在统计上与干净基线没有区别，包括 100 个注入错误，这支持结构缺陷会掩盖不成熟系统中的任务级信号这一判断。
- 确定性分流把全部 10,210 个 L3 结果送入自动监控，把全部 243 个 L2 结果送入人工调查，文中将其报告为分析师复核量减少 43 倍。
- 摘要还报告，97% 的结果进入了自动跟踪，约 2% 进入了人工调查，用于处理可变的系统行为。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.02494v1](https://arxiv.org/abs/2606.02494v1)
