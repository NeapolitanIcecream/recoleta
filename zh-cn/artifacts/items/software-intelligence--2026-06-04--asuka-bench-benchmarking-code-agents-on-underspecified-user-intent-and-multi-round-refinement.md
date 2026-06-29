---
source: arxiv
url: https://arxiv.org/abs/2606.05920v1
published_at: '2026-06-04T09:24:30'
authors:
- Xin Wang
- Liangtai Sun
- Yaoming Zhu
- Shuang Zhou
- Jiaxing Liu
- Fengjiao Chen
- Lin Qiu
- Xuezhi Cao
- Xunliang Cai
- Licheng Zhang
- Zhendong Mao
topics:
- code-agents
- web-generation
- benchmarking
- iterative-refinement
- user-feedback
- browser-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Asuka-Bench: Benchmarking Code Agents on Underspecified User Intent and Multi-Round Refinement

## Summary
## 摘要
Asuka-Bench 测试代码代理在构建网页应用时的表现：一开始用户需求很模糊，代理还要在多轮反馈中把网站改好。它之所以重要，是因为很多代码基准给出的是完整的一次性规格，而真实用户往往要在看到可运行界面后才补充缺失需求。

## 问题
- 它解决了一个评测不匹配问题：现有代码生成基准只看一个提示和一个答案，因此看不到代理能否在用户反馈后修复网页应用。
- 这个问题对自动化软件生产很重要，因为生成的项目要处理界面元素、交互逻辑和边界情况，而且要以已部署行为为准。
- 该基准对代码代理隐藏完整 PRD，只按浏览器渲染后的行为和内部标准对比，用来测试代理在意图不完整时的恢复能力。

## 方法
- 每个任务都从一个不完整的网页需求开始；隐藏的 Clarified PRD 定义完整需求和预期行为。
- Code Agent 构建网页项目，UI Agent 在浏览器中部署并测试它，User LLM 把通过或失败的结果转成自然语言反馈，供下一轮使用。
- 评测标准按 DAG 排列，所以只有前置测试通过后才会运行后续测试；反馈只列出直接失败项，不写下游症状。
- 数据集包含 50 个网页任务，分布在 6 个类别中，还有 784 个评测任务和 2,402 个预期结果，并包含存在性、功能性和鲁棒性检查。

## 结果
- 在 13 种模型-运行时配置中，3 轮后的累计加权 Task Pass Rate 从 51.8% 到 90.1%，相差 38.3 个百分点。
- 报告中的最佳 3 轮结果是 GPT-5.4 配合 OpenHands：Project Completion Rate 为 52%，加权 Task Pass Rate 为 90.1%，加权 Criteria Pass Rate 为 95.1%。
- Claude-4.6-Sonnet 配合 Claude Code 在 3 轮后达到 46% 的 Project Completion Rate、89.4% 的加权 Task Pass Rate 和 93.6% 的加权 Criteria Pass Rate。
- 报告中最弱的配置是 Seed-2.0-Pro 配合 Claude Code：3 轮后 Project Completion Rate 为 8%，加权 Task Pass Rate 为 51.8%，加权 Criteria Pass Rate 为 60.9%。
- 反馈在第 2 轮帮助最大：加权 Task Pass Rate 约提升 25 个百分点，而第 3 轮再增加 7 到 13 个百分点。
- 报告称，考虑 DAG 的评测流程平均把任务修复率提高 10.5 个百分点，并把评测 token 成本降低 23% 到 26%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05920v1](https://arxiv.org/abs/2606.05920v1)
