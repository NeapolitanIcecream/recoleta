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
## 总结
Claw-Eval-Live 是一个面向 LLM 工作流代理的动态基准，用来测试代理是否能在业务服务和本地工作区中完成真实任务。它的核心观点是，代理评测需要更新任务来源，并基于记录下来的动作、服务状态和工作区工件来评分。

## 问题
- 静态代理基准会随着用户工作流需求变化而过时，因此任务构成可能不再匹配当前的自动化需求。
- 只看最终答案的评分会奖励流畅的报告，即使代理跳过了必要的读取、写错了对象，或没有修复工作区。
- 真实工作流通常同时包含服务操作和本地文件或终端工作，而许多基准只覆盖其中一个界面。

## 方法
- 这个版本从带时间戳的 ClawHub Top-500 公共技能快照开始，然后对工作流模式聚类，并按信号量给任务家族加权。
- 候选任务使用固定的提示、夹具、工具、服务、工作区和任务专用评分器构建。
- 一个混合整数线性规划从 157 个筛选候选项中选出 105 个公共任务，同时满足版本规模、家族覆盖和试点模型区分要求。
- 评分尽量使用确定性证据：工具轨迹、服务审计日志、真实夹具、命令轨迹、运行后文件、测试和服务状态。
- 结构化 LLM 评判只用于完整性或报告质量等语义部分，由 GPT-5.4 按任务评分细则和记录轨迹进行判断。

## 结果
- 公开版本包含 105 个任务，覆盖 22 个细粒度家族：87 个带服务支持的工作流任务和 18 个工作区修复任务。
- 它评测了 13 个公开模型，及格阈值为 0.80，默认工作流预算为 24 轮和 300 秒。
- Claude Opus 4.6 排名第一，及格率为 66.7%，105 题中过了 70 题，总完成分数为 83.6。
- GPT-5.4 排名第二，及格率为 63.8%，过了 67 题，总分为 81.7。
- Claude Sonnet 4.6 和 GLM-5 都通过了 61.9% 的任务，各过 65 题；总分分别为 79.9 和 78.1。
- 没有任何被评测模型达到 70% 的及格率；论文指出，HR、管理和多系统业务工作流比本地工作区修复更难。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.28139v2](https://arxiv.org/abs/2604.28139v2)
