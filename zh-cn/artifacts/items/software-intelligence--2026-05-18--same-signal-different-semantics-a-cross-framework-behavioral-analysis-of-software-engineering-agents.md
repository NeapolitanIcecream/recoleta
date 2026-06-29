---
source: arxiv
url: https://arxiv.org/abs/2605.18332v1
published_at: '2026-05-18T12:49:18'
authors:
- Wei Ma
- Zhi Chen
- Jingxu Gu
- Tianling Li
- Shangqing Liu
- Lingxiao Jiang
topics:
- software-engineering-agents
- swe-bench
- behavioral-analysis
- code-intelligence
- llm-evaluation
- agent-frameworks
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Same Signal, Different Semantics: A Cross-Framework Behavioral Analysis of Software Engineering Agents

## Summary
## 摘要
这篇论文检验了软件工程智能体的行为规则是否能在不同智能体配置之间迁移。主要发现是，很多规则无法迁移，因为框架会改变同一可观测行为的含义。

## 问题
- 以往研究通常从单一智能体框架或一小组相近框架中推断成功规则，因此它们的外部有效性不清楚。
- 这对 SWE-bench 智能体很重要，因为开发者可能会改错地方，比如行为变化其实来自框架工作流，却去调整 LLM。
- 论文想回答的是，像错误率或“修改后再测试”这类行为-结果关系，在不同框架和 LLM 之间是否保持相同方向。

## 方法
- 研究分析了来自 43 个框架的 126 个框架-LLM 配置、共 64,380 条 SWE-bench Verified 轨迹。
- 它用两组切片分离框架效应和 LLM 效应：3 个 tracer LLM 分别在 6 到 8 个框架上运行，以及 33 个 LLM 在一个固定框架 mini-swe-agent 上运行。
- 研究用 45 个解析器处理日志，把动作映射到 6 个类别，检测 15 种错误类型，并构建连续轨迹特征和来自先前工作的 7 个二元行为模式。
- 每个配置贡献一个行为-结果效应量。作者比较了效应方向、用 Higgins' I2 衡量的异质性，以及框架身份与 LLM 家族分别解释的方差。

## 结果
- 错误率的含义分裂：47 个配置在错误率更低时解决更多问题，48 个配置在错误率更高时解决更多问题。
- 6 个连续特征和 7 个二元行为模式中的 3 个，在 126 个配置之间都出现了方向分化的效应。
- 对于平均轮次，框架身份解释了配置间方差的 64%，而 LLM 家族解释了 10%。
- 在通过置换诊断的 7 个特征中，框架身份解释的方差是 LLM 家族的 2.1 到 6.4 倍。
- 方向稳定的信号包括更短的轨迹、更少的重复访问、更低的熵和更低的回溯率，至少 88% 的配置在符号上达成一致。
- 预处理流水线在 5 个框架上的 500 个人工标注轮次中报告 Cohen's kappa 大于 0.85，每个配置的未识别动作中位数为 0.4%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18332v1](https://arxiv.org/abs/2605.18332v1)
