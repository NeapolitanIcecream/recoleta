---
source: arxiv
url: https://arxiv.org/abs/2605.09730v3
published_at: '2026-05-10T19:57:32'
authors:
- Will LeVine
- Brendan Evers
- Sam Saltwick
- Abhay Venkatesh
topics:
- tool-use-agents
- code-intelligence
- inference-time-refinement
- software-agents
- rubric-evaluation
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement

## Summary
## 摘要
RubricRefine 通过在代理运行代码前检查工具契约，提升代码模式工具使用代理的可靠性。它生成针对任务的评分细则，用来找出契约错误，并在零次执行尝试的情况下修复代码。

## 问题
- 代码模式代理可以生成可执行程序，调用多个工具，在调用之间传递数据，并格式化最终答案，但许多失败不会触发运行时错误。
- 主要失败包括输出形状错误、工具路由错误、参数来源断裂和调用顺序不当；这些问题可能让程序执行完成，但仍返回错误答案。
- 当实时工具调用可能改变外部状态、产生费用、触发速率限制或违反安全约束时，这一点很重要，因为失败后重试可能不可接受。

## 方法
- 该方法接收任务指令和工具注册表，然后生成针对任务的评分细则，对工具选择、输出契约、调用签名和数据来源进行明确检查。
- 验证器按 1-10 分给候选代码打分，并返回逐项 PASS/FAIL 反馈，包含原因和具体修复方向。
- 生成器在任何环境执行发生前，利用评分细则和验证器反馈修改代码。
- 当代码得分达到 10/10、耐心次数耗尽或达到轮次上限时，循环停止；得分最高的候选代码成为唯一的可执行动作。
- 该方法不需要训练，使用推理时验证，而不是模型微调或执行反馈。

## 结果
- 在 M3ToolEval 上，RubricRefine 在七个模型上的平均成功率为 0.86；单次 CodeAct 为 0.62，绝对提升 +0.24。
- RubricRefine 在每个测试模型上都表现最好：GPT-4.1-mini 0.86、GPT-4o 0.86、o3-mini 0.85、GPT-4.1 0.85、Gemma-4-26B 0.85、Qwen3.6-27B 0.84、Sonnet-4.6 0.88。
- 与 CodeAct 相比，论文报告 RubricRefine 在 M3ToolEval 上的单模型提升为 +0.14 到 +0.38，每个模型的配对 t 检验均为 p<0.001。
- RubricRefine 平均比使用真实执行反馈的 Self-Debug 绝对高 +0.12：0.86 对 0.74。
- Fixed RubricRefine 在七个模型中的六个上比 Self-Refine 高 +0.09 到 +0.20；完整 RubricRefine 在每个模型上都比 Fixed RubricRefine 高 +0.04 到 +0.12。
- 在主要是单步任务的基准 API-Bank 上，四个 OpenAI 模型的表现与 CodeAct 持平或处于噪声范围内，这与论文的说法一致：当任务包含工具间契约时，该方法帮助最大。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09730v3](https://arxiv.org/abs/2605.09730v3)
