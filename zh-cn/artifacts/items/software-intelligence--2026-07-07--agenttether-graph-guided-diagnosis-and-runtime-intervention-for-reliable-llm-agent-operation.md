---
source: arxiv
url: https://arxiv.org/abs/2607.06273v1
published_at: '2026-07-07T13:40:31'
authors:
- Chenyu Zhao
- Shenglin Zhang
- Wenwei Gu
- Yongqian Sun
- Dan Pei
- Chetan Bansal
- Saravan Rajmohan
- Minghua Ma
topics:
- llm-agents
- agent-repair
- runtime-intervention
- graph-diagnosis
- tool-use
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# AgentTether: Graph-Guided Diagnosis and Runtime Intervention for Reliable LLM Agent Operation

## Summary
## 摘要
AgentTether 是面向 LLM 代理的运行时修复层。它用依赖图诊断失败的工具使用运行，然后指导并监督下一次运行。它针对这类失败：早期错误操作导致后续错误，且一次性反馈会在长执行过程中失效。

## 问题
- 状态型工具工作流中的 LLM 代理可能因为早期错误的工具调用、缺失操作或错误参数改变后续状态，并引发下游错误。
- 盲目重试和结果反馈无法定位失败步骤；如果没有基于轨迹证据的支撑，自我反思可能会重复同样的错误。
- 这对生产环境中的代理很重要，因为失败或高风险操作可能浪费轮次和 token，违反工作流策略，或错误地改变外部状态。

## 方法
- AgentTether 在不改变代理的情况下记录一次运行，然后把轨迹压缩为 Transition Units：每个决策周期的观察、信念、动作和反馈。
- 它构建 Critical Transition Graph，其中节点是 Transition Units，边捕捉步骤之间的时间顺序和共享状态依赖。
- 它用两个检测器定位可疑子轨迹：一个在 21,143 条仅成功轨迹上训练的异构图 transformer，以及一个基于 25 个图上下文特征的运行内 Isolation Forest。
- 一个分析 LLM 将定位出的证据转化为根因、转折点和恢复提示；反馈构建器再把这些内容转化为简短的、限定行为范围的指导。
- Repair Memory 在多次尝试之间携带已修复和未解决的指令；运行时 harness 会在注入受保护的纠正前，检查循环、意图漂移、预期偏差和缺失的纠正动作。

## 结果
- 在 Retail、Airline 和 Banking 三个领域的 261 个 τ-bench 任务上，使用 Qwen3.7-max 时，AgentTether 修复了 69.11% 的初始失败任务。
- 相比盲目重试，它的总体修复率提高了 26.02 个百分点，在 Banking 上提高了 32.53 个百分点。
- 在 Qwen3.7-max Banking 上，它修复了 59.04% 的初始失败任务，即 83 个中的 49 个。
- 在 GPT-5.4 Banking 上，它修复了 65.12% 的初始失败任务，即 86 个中的 56 个，显示出在测试领域内可跨代理骨干迁移。
- 在 Qwen3.7-max Banking 上，受保护的运行时干预增加了 12.05 个百分点，当时反馈遵循能力较弱。
- 论文还报告了更少的代理轮次和更低的端到端方法 token 数，但摘录没有给出确切的轮次或 token 数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06273v1](https://arxiv.org/abs/2607.06273v1)
