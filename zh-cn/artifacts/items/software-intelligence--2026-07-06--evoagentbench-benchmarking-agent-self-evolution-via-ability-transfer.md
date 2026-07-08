---
source: arxiv
url: https://arxiv.org/abs/2607.05202v1
published_at: '2026-07-06T15:17:09'
authors:
- Xingze Gao
- Chuanrui Hu
- Hongda Chen
- Pengfei Yao
- Zhao Wang
- Yi Bai
- Zhengwei Wu
- Yunyun Han
- Xiaofeng Cong
- Jie Gui
- Yafeng Deng
- Teng Li
topics:
- agent-self-evolution
- llm-agents
- code-intelligence
- software-engineering
- benchmarking
- procedural-transfer
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# EvoAgentBench: Benchmarking Agent Self-Evolution via Ability Transfer

## Summary
## 摘要
EvoAgentBench 是一个基准，用来测试 LLM 智能体能否把过去任务轨迹转化为可在后续任务中复用的流程。它覆盖网页研究、算法推理、软件工程和知识工作，并使用 Ability Graph 保证每个测试任务都有相关的训练侧流程支持。

## 问题
- 现有智能体基准大多测试单次任务成功率，因此无法显示智能体是否复用了从早期工作中学到的流程。
- 记忆基准关注存储事实、检索或个性化，而这篇论文关注可复用流程，例如搜索计划、调试步骤和验证工作流。
- 这个缺口会影响长周期智能体，因为更高可靠性依赖于在任务之间迁移有用流程，同时避免记忆答案或依赖近重复样例。

## 方法
- 该基准使用三种构建骨干 Kimi-K2.5、GLM-5.1 和 DeepSeek-V3.2，收集四个领域中的 no-skill 智能体轨迹。
- 它从轨迹中提取原始 Ability 卡片。每张卡片记录触发条件、可复用流程、支持证据、适用边界和角色：Method、Guard 或 Workflow。
- 它通过基于嵌入的候选分块、三个 LLM 裁判和专家审查来规范化 Ability 卡片，然后只保留操作上等价的单元。
- 它构建领域专属的 Ability Graphs；当任务共享一个符合连边条件的 Ability 时，这些任务会被连接。
- 它创建训练/测试划分，其中每个测试任务都至少与同一 Ability 社区中的一个训练任务共享一个经过验证的 Ability。

## 结果
- EvoAgentBench 使用跨四个领域的 528 训练 / 267 测试划分：BrowseComp-Plus、SWE-Bench Verified、LiveCodeBench 和 GDPVal。
- 构建过程从 2,605 个源任务开始，从 2,516 个任务中提取 7,326 张原始 Ability 卡片，将其规范化为 170 个 Ability 单元，并保留一个包含 1,108 个任务的 Ability Graph；最终测试划分中有 0 个无支持的测试任务。
- 诊断性的 Anchor Skill 条件提升了每个报告的 scaffold-domain-backbone 单元。平均准确率在 Qwen3.5-27B 上从 37.5% 升至 45.0%（+7.5），在 Qwen3.5-397B 上从 49.2% 升至 59.7%（+10.5），在 Gemma-4-31B 上从 36.7% 升至 42.5%（+5.8）。
- 自动方法的迁移效果不一致。相对于 Vanilla 的平均增益分别为：Memento：-2.4、+1.5、-0.7；ReasoningBank：+3.6、+2.4、+0.4；GEPA：+1.2、+3.5、+5.7，对应 Qwen3.5-27B、Qwen3.5-397B 和 Gemma-4-31B。
- 某些单元中出现了较大的负迁移：Memento 使 Qwen3.5-27B Nanobot SWE 下降 36.3 点，GEPA 使 Qwen3.5-27B OpenClaw knowledge work 下降 12.3 点，ReasoningBank 使 Gemma-4-31B OpenClaw algorithmic reasoning 下降 10.9 点。
- 论文称，人工整理的 Ability 内容可以跨模型家族迁移，而当前自动自进化方法无法在所有领域、脚手架和骨干上都保持正增益。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05202v1](https://arxiv.org/abs/2607.05202v1)
