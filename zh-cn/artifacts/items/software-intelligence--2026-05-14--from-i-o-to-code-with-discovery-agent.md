---
source: arxiv
url: https://arxiv.org/abs/2605.15334v1
published_at: '2026-05-14T18:57:32'
authors:
- Yihong Dong
- Jiaru Qian
- Haoran Zhang
- Peixu Wang
- Binhua Li
- Zhi Jin
- Yongbin Li
- Ge Li
- Xiaokang Yang
- Xue Jiang
topics:
- code-generation
- program-synthesis
- io2code
- llm-agents
- evolutionary-search
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# From I/O to Code with Discovery Agent

## Summary
## 摘要
DIO-Agent 在没有自然语言规格说明时，根据输入-输出示例合成代码。它把程序归纳视为由 LLM 引导的进化搜索，并用执行错误和由简到繁的变异顺序指导每次编辑。

## 问题
- IO2Code 要求模型从可见的输入-输出对推断通用程序，并通过保留测试。
- 这关系到黑盒 API 逆向工程、遗留系统迁移、科学规则归纳，以及通过示例捕获用户意图。
- 有限示例不能完整限定目标规则，因此模型可能用查找表通过可见用例，或通过针对个案的逻辑过拟合。

## 方法
- 论文提出 DIO-Agent 和 IO2CodeBench。IO2CodeBench 是一个包含 Base、Algorithm、Geometry 和 Multimodal 等级的基准。
- DIO-Agent 运行基于岛屿的进化循环：选择父程序，请 LLM 生成 SEARCH/REPLACE 代码差异，执行子程序，打分，并保留有用变体。
- 课程机制先展示较容易的示例，再加入较难用例，同时重放早前示例以避免退化。
- 转换优先前提（Transformation Priority Premise）按由简到繁的顺序指导编辑：常量、变量、多条语句、条件、数组、循环和函数。
- 基于错误的反馈向 LLM 提供具体失败输入、错误输出、运行时错误，以及一个会惩罚代码复杂度和记忆化示例的分数。

## 结果
- 在使用 DeepSeek V3.2 的 IO2CodeBench 上，DIO-Agent 的平均通过率达到 58.63，高于 CodeEvolve 的 49.60、AlphaEvolve 的 47.29、FunSearch 的 45.01、E-PBE 的 38.63、Direct 的 32.18 和 PBE 的 14.58。
- 按等级看，DIO-Agent 在 Base 上得分 61.29，在 Algorithm 上得分 71.43，在 Geometry 上得分 61.11，在 Multimodal 上得分 40.67。
- 相比 CodeEvolve，DIO-Agent 将 Algorithm 从 60.00 提高到 71.43，将 Geometry 从 44.44 提高到 61.11，将 Multimodal 从 32.67 提高到 40.67；每次迭代使用 3738.31 个 token，CodeEvolve 为 5829.32 个。
- 在不同基础 LLM 上，DIO-Agent 使用 DeepSeek V3.2 的平均得分为 58.63，使用 Qwen-3.6-Plus 为 55.45，使用 Claude-Sonnet-4.6 为 57.31。
- 消融实验显示，去除错误反馈后平均性能从 58.63 降至 54.61，去除 TPP 后降至 53.80，去除课程进化后降至 51.33。
- 在相同的 40 个候选预算下，DIO-Agent 的平均通过率为 63.66，高于 Best-of-N 的 40.28、Self-Consistency 的 25.53 和 Direct 的 14.56。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15334v1](https://arxiv.org/abs/2605.15334v1)
