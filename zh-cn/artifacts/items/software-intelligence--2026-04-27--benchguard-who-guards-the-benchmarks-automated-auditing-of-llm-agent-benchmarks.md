---
source: arxiv
url: https://arxiv.org/abs/2604.24955v1
published_at: '2026-04-27T19:51:25'
authors:
- Xinming Tu
- Tianze Wang
- Yingzhou
- Lu
- Kexin Huang
- Yuanhao Qu
- Sara Mostafavi
topics:
- llm-agent-benchmarks
- benchmark-auditing
- execution-based-evaluation
- human-ai-review
- code-evaluation
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# BenchGuard: Who Guards the Benchmarks? Automated Auditing of LLM Agent Benchmarks

## Summary
## 总结
BenchGuard 通过检查任务说明、参考解答、评测脚本和环境是否一致，来审计基于执行的 LLM agent 基准。论文声称，它以较低的审计成本发现了人工审稿人遗漏的基准缺陷。

## 问题
- 当任务文本、标准代码、评测逻辑或环境设置彼此冲突时，基于执行的基准会把 agent 评分打错。
- 这些错误会让有效的 agent 解法被判失败，让任务变成不可解，也会扭曲排行榜分数。

## 方法
- BenchGuard 读取每个任务的四类材料：任务说明、标准程序、评测脚本和环境配置。
- 结构化 LLM 审计分六步检查这些材料：任务理解、标准程序正确性、评测器逻辑、任务规格、环境检查和去重。
- 审计时会同时运行确定性的静态检查；如果有可用的 agent 程序或执行日志，也会作为补充证据。
- 发现项按 4 类、14 个子类的缺陷分类法标注，覆盖标准答案、评测、说明和环境问题；每个发现都包含严重程度、置信度和引用证据。

## 结果
- 在 ScienceAgentBench 上，审计发现了 12 个经原作者确认的缺陷，覆盖 102 个任务，包括致命任务错误、指标不匹配，以及会拒绝正确输出的评测器。
- 在 ScienceAgentBench 的仅定义审计中，Claude Opus 4.6 的完全召回率为 83.3%，部分匹配召回率为 91.7%；五模型并集的完全召回率为 91.7%，部分匹配召回率为 100%。
- 在 ScienceAgentBench 上加入 agent 程序后，Claude Opus 4.6 的完全召回率升至 91.7%，部分匹配召回率升至 100%；五模型并集的完全召回率达到 100%。
- 在 BIXBench Verified-50 上，五模型并集准确匹配了专家识别出的 24 个原子问题中的 20 个，完全召回率为 83.3%；按部分匹配计算时匹配了 23 个，召回率为 95.8%。
- BIXBench 上表现最好的单模型 Claude Opus 4.6 准确匹配了 24 个问题中的 13 个，召回率为 54.2%，50 个任务的成本为 5.98 美元。
- 50 个 BIXBench 任务的五模型完整审计成本为 14.38 美元，102 个 ScienceAgentBench 任务的仅定义模式成本为 22.72 美元；论文还指出，50 个任务的生物信息学审计成本低于 15 美元。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24955v1](https://arxiv.org/abs/2604.24955v1)
