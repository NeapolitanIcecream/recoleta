---
source: arxiv
url: https://arxiv.org/abs/2605.08717v1
published_at: '2026-05-09T06:02:08'
authors:
- Chenyu Zhao
- Shenglin Zhang
- Yihang Lin
- Wenwei Gu
- Zhimin Chen
- Yongqian Sun
- Dan Pei
- Chetan Bansal
- Saravan Rajmohan
- Minghua Ma
topics:
- software-engineering-agents
- agent-recovery
- code-intelligence
- telemetry
- failure-diagnosis
- aiops
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents

## Summary
## 摘要
PROBE 通过把失败运行的遥测数据转成有证据支撑的重试指导，提升软件工程智能体的失败后恢复能力。它面向代码修复、企业工作流和 AIOps 服务缓解中的智能体失败运行。

## 问题
- 软件工程智能体会在工具错误、未检查的结果、错误的工作流状态或过早提交之后失败；人工恢复慢且不一致。
- 最终的基准失败标签无法说明哪一步出错、哪些证据重要，或下一次尝试应改变什么。
- 在 257 个首次尝试未解决的案例中，172 个案例（66.93%）来自验证不足、工具/子进程故障处理不当，或状态/工作流错误。

## 方法
- PROBE 记录失败运行的 span 级遥测数据，包括指标、日志、追踪、智能体意图、工具-环境状态，以及可选的评估器结果。
- 它用基于 MAD 的 z 分数、经验分位数、Isolation Forest、日志签名、重复工具失败、追踪模式和评估器信号进行指标异常检查，从而定位失败证据。
- 它把相关发现融合为结构化证据记录，包含锚点、时间范围、严重性、支持证据、冲突和来源。
- 锚点优先的诊断步骤会输出结构化字段，例如失败锚点、主要原因、行为错误、促成因素、证据和置信度。
- Guidance Gate 只在诊断有证据支撑、可执行且处于智能体侧可控范围内时，生成包含目标、操作、验证信号和边界条件的重试指导。

## 结果
- 评估覆盖 SWE-bench、EnterpriseOps-Gym 和 AIOpsLab 中 257 个初始未解决案例，三者分别为 102、106 和 49 个案例。
- PROBE 报告的 Top-1 诊断准确率为 65.37%，比最强的非 PROBE 基线高 43.58 个百分点。
- PROBE 报告的恢复率为 21.79%，比最强的非 PROBE 基线高 12.45 个百分点。
- 论文报告了诊断-恢复差距：诊断准确率为 65.37%，恢复率为 21.79%，因此正确诊断经常无法转化为下一次运行成功。
- 一个 Microsoft IcM 原型把 PROBE 作为旁路接入，要求对智能体策略、工具集或执行预算做 0 项更改；摘录未给出 IcM 成功率的定量指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08717v1](https://arxiv.org/abs/2605.08717v1)
