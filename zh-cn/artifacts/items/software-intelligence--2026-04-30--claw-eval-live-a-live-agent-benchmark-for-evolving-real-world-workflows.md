---
source: arxiv
url: https://arxiv.org/abs/2604.28139v2
published_at: '2026-04-30T17:23:19'
authors:
- Chenxin Li
- Zhengyang Tang
- Mingxin Huang
- Yunlong Lin
- Shijue Huang
- Shengyuan Liu
- Bowen Ye
- Rang Li
- Lei Li
- Benyou Wang
- Yixuan Yuan
topics:
- agent-benchmark
- workflow-agents
- tool-use
- workspace-repair
- llm-evaluation
- human-ai-interaction
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows

## Summary
## 摘要
Claw-Eval-Live 是一个面向 LLM 工作流代理的实时基准，用来测试代理能否跨业务服务和本地工作区完成真实任务。它的核心主张是：代理评测需要持续更新任务来源，并根据记录下来的动作、服务状态和工作区产物进行评分。

## 问题
- 静态代理基准会随着用户工作流需求变化而过时，因此任务组合可能不再符合当前的自动化需求。
- 只看最终答案的评分可能奖励流畅的报告，即使代理跳过了必要读取、写错了对象，或没有修复工作区。
- 真实工作流常常同时包含服务操作和本地文件或终端工作，而许多基准只覆盖其中一种操作面。

## 方法
- 该发布版本从带时间戳的 ClawHub Top-500 公共技能快照开始，然后聚类工作流模式，并按信号量为任务族分配权重。
- 候选任务使用固定提示、夹具、工具、服务、工作区和任务专用评分器构建。
- 一个混合整数线性规划从 157 个经过筛选的候选任务中选择 105 个公开任务，同时约束发布规模、任务族覆盖率和试点模型区分度。
- 评分在可行时使用确定性证据：工具轨迹、服务审计日志、真实值夹具、命令轨迹、运行后文件、测试和服务状态。
- 结构化 LLM 评判只用于完整性或报告质量等语义部分，由 GPT-5.4 根据任务评分规则和记录轨迹进行评判。

## 结果
- 公开发布版包含 105 个任务，覆盖 22 个细粒度任务族：87 个有服务支撑的工作流任务和 18 个工作区修复任务。
- 它评测了 13 个公开模型，通过阈值为 0.80，默认工作流预算为 24 轮和 300 秒。
- Claude Opus 4.6 排名第一，通过率为 66.7%，105 个任务中通过 70 个，整体完成分数为 83.6。
- GPT-5.4 排名第二，通过率为 63.8%，通过 67 个，整体分数为 81.7。
- Claude Sonnet 4.6 和 GLM-5 都通过了 61.9% 的任务，各通过 65 个；它们的整体分数分别为 79.9 和 78.1。
- 没有被评测模型达到 70% 的通过率；论文报告称，HR、管理和多系统业务工作流比本地工作区修复更难。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.28139v2](https://arxiv.org/abs/2604.28139v2)
