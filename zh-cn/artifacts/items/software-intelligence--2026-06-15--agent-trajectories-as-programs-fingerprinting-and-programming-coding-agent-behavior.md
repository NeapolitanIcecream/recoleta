---
source: arxiv
url: https://arxiv.org/abs/2606.16988v1
published_at: '2026-06-15T17:28:41'
authors:
- Hamidah Oderinwale
topics:
- coding-agents
- software-engineering
- agent-traces
- behavioral-fingerprinting
- swe-bench
- trace-search
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Agent trajectories as programs: fingerprinting and programming coding-agent behavior

## Summary
## 摘要
论文认为，可以通过编码智能体的行动轨迹来识别它们，并对其行为进行编程；任务成功率只能提供评分的一部分。论文介绍了 ProcGrep，这是一个用于构建程序性指纹、比较智能体和搜索过往智能体轨迹的库。

## 问题
- 基准分数显示智能体是否解决了任务，但不显示智能体如何搜索、编辑、测试或失败。
- 随着编码智能体承担更多软件工作流，开发者需要轨迹级工具来做模型路由、监控、成本分析和调试。
- 自然语言计划和理由对行动的证明力较弱：论文报告了几个模型说明的低精确率，包括 Claude-4 精确率 `0.500` 和 Claude-3.7-thinking 精确率 `0.625`。

## 方法
- 该方法把智能体轨迹转为程序性动作序列，例如 `read_file`、`search_repo`、`edit`、`run_test` 和 `submit`。
- 它用 AST 解析解决方案补丁，加入代码上下文和模型写出的行为描述，然后从重复出现的动作子序列中归纳共享动作词表。
- 主要词表归纳方法是在动作轨迹上使用 BPE。论文在一次 V-measure 扫描后选择 `K=192`，报告的峰值为 `0.644`，并且在 `K=128` 到 `K=256` 之间出现平台期。
- 它用熵、压缩率、动作转移统计、最近邻检索和程序性分布上的 Jensen-Shannon 散度来比较智能体。
- ProcGrep 允许用户对轨迹编写确定性的结构查询，包括有序动作、计数、条件和缺失动作。

## 结果
- 在来自 10 个智能体的 SWE-bench Verified 轨迹上，这些智能体覆盖 GPT、Claude、DeepSeek、Qwen 衍生模型、SWE-agent、Agentless、DARS 和 Moatless 设置；程序性指纹能以 `85.7%` 的准确率把未见过的轨迹归因到正确智能体，随机基线为 `11.1%`。
- 不同的动作转移可识别智能体：DARS+R1 对 `search_repo → create_file` 的使用高出 `31.6×`，Moatless+V3 对 `edit → submit` 的使用高出 `15.7×`，Agentless+Claude-3.5 对 `run_test → run_test` 的使用高出 `12.5×`。
- 在情节式轨迹搜索中，ProcGrep 达到 `F1=1.000`，每次决策延迟为 `1.1 µs`。LLM 裁判更低：Claude Sonnet 4.6 在 `1.71 s` 下得到 `F1=0.278`，GPT-4o 在 `0.66 s` 下得到 `F1=0.230`，DeepSeek-chat 在 `1.51 s` 下得到 `F1=0.093`。
- 教师-学生的程序性相似度可以度量：Claude-3.7-thinking 到 SWE-agent-LM-32B 的蒸馏配对为 `JSD=0.250`，相比之下，跨代同模型家族内为 `0.518`，同一模型跨脚手架为 `0.533`。
- 在最近邻测试中，程序性表示比自然语言说明更能预测成功：结构模式重叠得到 `F1=0.347`，动作序列距离得到 `F1=0.274`，叙事描述得到 `F1=0.177`，随机检索范围为 `0.13` 到 `0.24`。
- 成本和行为因智能体而异：Claude-4 以每个已解决任务 `$2.02` 的成本解决 `59.0%` 的任务，Claude-3.7-thinking 以 `$1.53` 解决 `50.7%`，GPT-4 以 `$13.93` 解决 `18.0%`，Moatless+DeepSeek-V3 以 `$0.06` 解决 `30.7%`。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.16988v1](https://arxiv.org/abs/2606.16988v1)
