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
DIO-Agent 在没有自然语言规范时，根据输入输出示例合成代码。它把程序归纳当作由 LLM 引导的进化搜索，靠执行错误和从简单到复杂的变异顺序来指导每次修改。

## Problem
- IO2Code 要求模型从可见的输入输出对中推断出一个通用程序，并通过留出的测试。
- 这对黑盒 API 逆向、遗留系统迁移、科学规则归纳，以及通过示例捕捉用户意图都很重要。
- 有限示例会让目标规则变得不完整，所以模型可能用查找表通过可见样例，或写出只适用于特定案例的逻辑而过拟合。

## Approach
- 论文提出了 DIO-Agent 和 IO2CodeBench，一个包含 Base、Algorithm、Geometry 和 Multimodal 层级的基准。
- DIO-Agent 运行一个基于岛屿的进化循环：选择父程序，要求 LLM 生成 SEARCH/REPLACE 代码差分，执行子程序，打分，并保留有用的变体。
- 课程式训练先展示更容易的例子，再加入更难的案例，同时回放早期例子以避免回退。
- Transformation Priority Premise 以从简单到复杂的顺序引导修改：常量、变量、多条语句、条件分支、数组、循环和函数。
- 基于错误的反馈会把具体的失败输入、错误输出、运行时错误，以及对代码复杂度和记忆化示例进行惩罚的分数提供给 LLM。

## Results
- 在使用 DeepSeek V3.2 的 IO2CodeBench 上，DIO-Agent 的平均通过率为 58.63，高于 CodeEvolve 的 49.60、AlphaEvolve 的 47.29、FunSearch 的 45.01、E-PBE 的 38.63、Direct 的 32.18 和 PBE 的 14.58。
- 按层级看，DIO-Agent 在 Base 上得分 61.29，在 Algorithm 上得分 71.43，在 Geometry 上得分 61.11，在 Multimodal 上得分 40.67。
- 与 CodeEvolve 相比，DIO-Agent 将 Algorithm 从 60.00 提升到 71.43，将 Geometry 从 44.44 提升到 61.11，将 Multimodal 从 32.67 提升到 40.67，同时每次迭代使用 3738.31 个 token，而不是 5829.32 个。
- 在不同基础 LLM 上，DIO-Agent 使用 DeepSeek V3.2 的平均得分为 58.63，Qwen-3.6-Plus 为 55.45，Claude-Sonnet-4.6 为 57.31。
- 消融实验会降低平均表现：去掉错误反馈后降到 54.61，去掉 TPP 后降到 53.80，去掉课程式进化后降到 51.33。
- 在匹配的 40 个候选预算下，DIO-Agent 的平均通过率为 63.66，高于 Best-of-N 的 40.28、Self-Consistency 的 25.53 和 Direct 的 14.56。

## Link
- [https://arxiv.org/abs/2605.15334v1](https://arxiv.org/abs/2605.15334v1)
