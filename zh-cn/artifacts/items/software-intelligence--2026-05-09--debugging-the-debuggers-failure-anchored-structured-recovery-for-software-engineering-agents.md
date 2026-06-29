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
PROBE 通过把失败运行的遥测转成有证据支撑的重试指导，提升软件工程代理在失败后的恢复能力。它面向代码修复、企业工作流和 AIOps 服务缓解中的失败代理运行。

## 问题
- 软件工程代理会在工具错误、结果未校验、工作流状态错误或过早提交后失败；人工恢复速度慢，而且做法不一致。
- 最终基准里的失败标签看不出是哪一步出错、哪些证据重要、下一次尝试该改什么。
- 在 257 个首次未解决案例中，172 个案例（66.93%）来自验证不足、工具/子进程失败处理问题，或状态/工作流错误。

## 方法
- PROBE 记录失败运行的跨度级遥测，包括指标、日志、轨迹、代理意图、工具环境状态，以及可选的评估器结果。
- 它用基于 MAD 的 z 分数、经验分位数、Isolation Forest、日志特征、重复工具失败、轨迹模式和评估器信号做指标异常检查，定位失败证据。
- 它把相关发现融合成结构化证据记录，包含锚点、时间范围、严重程度、支持信息、冲突和来源。
- 先锚定后诊断的步骤会输出结构化字段，如失败锚点、主要原因、行为错误、促成因素、证据和置信度。
- 只有当诊断有证据支撑、可执行，而且在代理侧控制范围内时，Guidance Gate 才会生成重试指导，包含目标、操作、验证信号和边界条件。

## 结果
- 评估覆盖 SWE-bench、EnterpriseOps-Gym 和 AIOpsLab 中 257 个最初未解决案例：分别为 102、106 和 49 个。
- PROBE 的 Top-1 诊断准确率为 65.37%，比最强的非 PROBE 基线高 43.58 个百分点。
- PROBE 的恢复率为 21.79%，比最强的非 PROBE 基线高 12.45 个百分点。
- 论文报告了诊断-恢复差距：诊断准确率是 65.37%，恢复率是 21.79%，所以正确诊断常常不会转化为成功的下一次运行。
- 一个 Microsoft IcM 原型把 PROBE 作为旁路接入，代理策略、工具集或执行预算都不需要改动；摘要没有给出 IcM 的定量成功指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08717v1](https://arxiv.org/abs/2605.08717v1)
