---
source: arxiv
url: https://arxiv.org/abs/2607.06184v1
published_at: '2026-07-07T12:09:46'
authors:
- Rui Shu
- Chun Yong Chong
- Xin Zhou
- Yun Peng
- Zihan Wu
- Xu Han
- Zeyang Zhuang
- Guowen Yuan
- Yuan Wang
topics:
- coding-agents
- trajectory-analysis
- swe-bench
- agent-evaluation
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# What Resolve Rate Hides: Trajectory Structure Diagnostics for Coding Agents

## Summary
## 摘要
TraceProbe 通过把原始轨迹转换为可比较的动作序列和基于规则的过程信号，诊断编码代理的运行。它为 SWE-Bench 式的解决率补充过程证据，让开发者看到代理在哪里搜索、编辑、验证、失败，或做了无效工作。

## 问题
- 解决率只说明最终补丁是否通过目标测试。它遗漏了一次运行失败的原因，也遗漏了通过测试的运行为什么用了额外步骤、token 和工具调用。
- 原始代理轨迹把读取、搜索、编辑、命令、计划、推理和日志混在特定脚手架格式中，导致跨代理比较很难。
- 这个问题关系到代码代理开发，因为两个代理可以用很不同的成本和失败恢复模式解决同一个任务。

## 方法
- TraceProbe 将每次运行规范化为 9 种标准动作类型：文件读取、文件写入、搜索、命令、子代理启动、计划、导航、获取和推理。
- 它根据观察到的轨迹状态分配确定性的效果标签，例如 survived、failed、reverted、justified、recorded、off-anchor 和 reasoning。
- Insight 模块用固定规则扫描单条轨迹，识别命名的反模式，包括搜索循环、重复读取消耗、冗余搜索、跳过验证和无支撑的完成声明。
- Converge 模块用序列匹配对齐两次运行，然后把未匹配或重新排序的片段标记为分歧，例如 off-anchor exploration、scope drift 和 rapid rewrite。
- 可用时，Gold SWE-Bench 补丁提供锚点文件，因此 TraceProbe 可以测量首次相关读取、首次相关写入、写入所有锚点、首次通过验证和首次有依据的动作。

## 结果
- 该研究将 TraceProbe 应用于 SWE-Bench Verified 上的 2,500 条轨迹，覆盖 5 个生产设置、3 个脚手架和 3 个模型主干。
- 在论文用于说明动机的 SWE-Bench pytest-7982 示例中，Claude Code 搭配 Opus 4.6 用 10 步解决任务且没有失败动作；OpenCode 搭配 GLM-5 也解决了任务，但用了 49 步，并出现重复的失败和恢复片段。
- 论文称，文件级选择过于粗糙，难以区分成功和失败；函数选择和完成行为能提供更局部的失败证据。
- 论文报告称，搜索循环是在各项检查中最稳定的 Insight 反模式，其他反模式对数据切分更敏感。摘录未提供这些检测器差距的比例、置信区间或效应量。
- Converge 发现，即使是已解决的运行，在到达相关代码的时间、失败工作量以及脚手架/模型特定的过程变化上也有差异。摘录未提供聚合的里程碑中位数或解决率差值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06184v1](https://arxiv.org/abs/2607.06184v1)
