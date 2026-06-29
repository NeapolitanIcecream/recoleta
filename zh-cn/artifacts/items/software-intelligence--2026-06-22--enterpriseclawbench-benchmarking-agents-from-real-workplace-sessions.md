---
source: arxiv
url: https://arxiv.org/abs/2606.23654v1
published_at: '2026-06-22T17:39:43'
authors:
- Jincheng Zhong
- Weizhi Wang
- Che Jiang
- Kai Tian
- Zhenzhao Yuan
- Junlin Yang
- Dianqiao Lei
- Kaiyan Zhang
topics:
- agent-benchmark
- enterprise-agents
- workspace-automation
- artifact-evaluation
- skill-transfer
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions

## Summary
## 摘要
EnterpriseClawBench 是一套协议，用于把真实企业智能体会话转成可复现的工作场景任务，并按交付文件、质量、成本和运行时间给智能体评分。Lite 子集最高结果为 0.663，因此论文认为当前企业智能体仍未满足许多产物交付和内容质量要求。

## 问题
- 企业智能体在基于文件的工作区内执行任务，成功取决于能否找到输入、使用工具、保留状态并产出可用产物；只给出正确的聊天回答不足以说明任务成功。
- 现有智能体基准常使用公开、模拟或人工编写的任务，因此漏掉了工作会话中的许多复杂需求。
- 企业团队需要按运行器-模型组合、任务类别、产物类型、成本、运行时间和技能迁移来查看分数，因为单独的基础模型分数可能掩盖交付失败。

## 方法
- 该流程从一家员工超过 100 人的 AI 初创公司在 2026 年 3 月至 5 月的内部工作会话开始。
- 它将会话轮次拆分并合并为候选任务，然后按长度、可恢复的输入夹具、脱敏恢复、网络依赖和自包含用户意图进行筛选。
- 通过筛选的任务被改写为单轮提示，并与恢复文件、角色类别、45 个技能子类、预期交付物、硬性规则以及文本或视觉评分细则一起打包。
- 每个运行器-模型组合都在新的 Linux 沙箱中运行；运行程序上传输入、调用智能体、下载输出和轨迹，并记录完成情况、耗时、token 用量、成本和工具调用。
- 评分结合客观文件检查和语义评审器，评估有依据的准确性、任务相关性、实质内容深度、实用性和沟通质量。

## 结果
- 构建漏斗从 5,291 个原始 TaskInstances 开始，得到 852 个最终基准任务；人工审核的 Lite 子集包含 120 个任务。
- 在 120 任务 Lite 集上，32 个运行器-模型组合中的最佳结果是 Codex 搭配 GPT-5.5，得分 0.663；Sonnet 4.6 在 Claude Code、DeepAgents 和 OpenClaw 下约为 0.62-0.64，但在 Hermes 下为 0.458。
- 在 DeepAgents 下的完整 852 任务集上，GPT-5.5 总分为 0.766，其中文本 0.813、视觉 0.642、规则 0.959；Sonnet 4.6 得分 0.749，Haiku 4.5 得分 0.632，GPT-4.1-mini 得分 0.336。
- 在留出的前端页面生成任务上进行技能注入，结果显示迁移效果取决于技能创建者：GPT-5.5 技能平均 +0.0681，Kimi K2.6 技能平均 +0.0518，Haiku 4.5 技能平均 -0.0941。
- 评审器检查显示，文本分数上的 LLM-LLM 一致性很强，GPT-5.4-text 与 Sonnet 4.6 在 1,853 个案例上的 Spearman 为 0.918；视觉一致性较低，在 1,428 个案例上为 0.866。
- 对 48 个包的人工审核发现，文本校准优于视觉校准：文本 MAE 为 0.134，Spearman 为 0.790；视觉 MAE 为 0.303，Spearman 为 -0.259。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23654v1](https://arxiv.org/abs/2606.23654v1)
