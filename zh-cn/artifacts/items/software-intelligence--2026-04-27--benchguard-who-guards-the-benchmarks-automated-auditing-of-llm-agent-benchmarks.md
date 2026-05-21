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
## 摘要
BenchGuard 通过检查指令、参考解法、评估脚本和环境是否一致，审计基于执行的 LLM 智能体基准。论文称，它能以较低审计成本发现人工评审遗漏的基准缺陷。

## 问题
- 当任务文本、标准代码、评估器逻辑或环境设置相互冲突时，基于执行的基准可能会错误地给智能体打分。
- 这些错误会让有效的智能体解法失败，让任务无法求解，并扭曲排行榜分数。

## 方法
- BenchGuard 为每个任务接收四类工件：指令、真实值程序、评估脚本和环境配置。
- 结构化 LLM 审计分六步检查这些工件：任务理解、标准程序正确性、评估器逻辑、任务规格、环境检查和去重。
- 确定性静态检查与 LLM 审计同时运行；在可用时，可选的智能体程序或执行日志会补充证据。
- 发现的问题按一个包含 4 个大类、14 个子类的缺陷分类体系标注，覆盖真实值、评估、指令和环境问题；每个发现都包含严重性、置信度和引用证据。

## 结果
- 在 ScienceAgentBench 上，审计在 102 个任务中发现了 12 个由原作者确认的缺陷，包括致命任务错误、指标不匹配，以及会拒绝正确输出的评估器。
- 在 ScienceAgentBench 的仅定义审计中，Claude Opus 4.6 达到 83.3% 的精确召回率，包含部分匹配时召回率为 91.7%；五模型并集达到 91.7% 的精确召回率，包含部分匹配时为 100%。
- 在 ScienceAgentBench 上加入智能体程序后，Claude Opus 4.6 的精确召回率提高到 91.7%，包含部分匹配时召回率为 100%；五模型并集达到 100% 的精确召回率。
- 在 BIXBench Verified-50 上，五模型并集精确匹配了专家识别的 24 个原子问题中的 20 个，精确召回率为 83.3%；包含部分匹配时匹配了 24 个中的 23 个，召回率为 95.8%。
- BIXBench 上表现最好的单模型 Claude Opus 4.6 精确匹配了 24 个问题中的 13 个，召回率为 54.2%，50 个任务的成本为 5.98 美元。
- 在仅定义模式下，完整五模型审计的成本为：50 个 BIXBench 任务 14.38 美元，102 个 ScienceAgentBench 任务 22.72 美元；论文还称，50 个生物信息学任务的审计成本低于 15 美元。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24955v1](https://arxiv.org/abs/2604.24955v1)
