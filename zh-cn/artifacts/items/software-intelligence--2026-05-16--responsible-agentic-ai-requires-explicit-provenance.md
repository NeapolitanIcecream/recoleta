---
source: arxiv
url: https://arxiv.org/abs/2605.17169v1
published_at: '2026-05-16T21:56:33'
authors:
- Jinwei Hu
- Xinmiao Huang
- Qisong He
- Youcheng Sun
- Yi Dong
- Xiaowei Huang
topics:
- agentic-ai
- ai-provenance
- responsibility-attribution
- multi-agent-systems
- ai-governance
- software-agents
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Responsible Agentic AI Requires Explicit Provenance

## Summary
## 摘要
论文认为，负责任的 agentic AI 需要在设计、执行、部署和群体监测各阶段保留显式来源记录。它提出用因果贡献、认知位置和责任张量，在多步智能体行为造成损害时分配责任。

## 问题
- Agentic AI 可以调用工具、使用记忆、进行多步规划，并在多个智能体之间协作，所以损害可能来自整个轨迹，而不是单个模型输出或单个组件。
- 按组件审计无法说明在开发者、工具作者、平台运营方和部署方都影响了系统时，究竟是谁导致了有害结果。
- 这对软件智能体和其他委托式系统很重要，因为用户和监管方无法信任无法说明谁做了什么、哪些后果可预见、以及何时本该介入的系统。

## 方法
- 论文把显式来源记录定义为支持三种属性的记录：因果贡献可量化、执行记录可追踪、以及在损害变得不可逆之前可介入。
- 它把因果贡献定义为：在反事实轨迹中移除或中和某一方相关决策后，损害概率发生的变化。
- 它加入了认知位置，用来记录每一方在损害发生前知道了什么，或本应知道什么。
- 它定义了一个责任分配函数，为每一方给出责任权重；当无法完成个人归因时，把剩余责任分配给机构。
- 它把这些内容扩展为一个跨参与方、损害事件和社会技术维度的责任张量，然后把工作映射到四个生命周期层：设计、工程、部署和群体规模监测。

## 结果
- 摘要没有给出论文初步实验的详细指标；它只说明，因果贡献可以从执行前缀在线估计，并且可以在不可逆损害累积之前支持干预。
- 论文引用了采用证据：麦肯锡报告显示，23% 的受访者在扩展 agentic AI，39% 在试验；普华永道报告显示，79% 的高级管理者表示，他们公司已经在采用 AI agents。
- 论文引用了工具和智能体场景的风险证据：在 17 个集成工具的系统中，间接提示注入对 GPT-4 的攻击率达到 47%。
- 它引用了沙盒证据，显示超过 68% 的场景存在现实世界智能体故障的潜在可能。
- 它引用了市场证据，显示高热度的 ClawHub 技能中，超过 90% 未通过安全审查。
- 论文主张的核心结果是给出一条形式化路径来计算责任：因果贡献加上可预见性决定各方责任，未分配的责任则分到机构层。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17169v1](https://arxiv.org/abs/2605.17169v1)
