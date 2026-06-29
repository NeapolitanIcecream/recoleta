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
RubricRefine 通过在代码运行前检查工具契约来提高代码模式工具使用代理的可靠性。它先生成任务特定的评分标准，再用它找出契约错误，并在零次执行尝试的情况下修复代码。

## 问题
- 代码模式代理可以生成可执行程序，调用多个工具，在调用之间传递数据，并格式化最终答案，但很多失败不会触发运行时错误。
- 主要失败包括输出形状错误、工具路由错误、参数来源断裂和调用顺序错误；这些程序可以执行完，却仍然给出错误答案。
- 当一次真实工具调用会改变外部状态、产生费用、触发速率限制或违反安全约束时，这个问题更重要，因为失败后再重试可能无法接受。

## 方法
- 该方法接收任务指令和工具注册表，然后生成一套任务特定的评分标准，明确检查工具选择、输出契约、调用签名和数据来源。
- 验证器按 1 到 10 分给候选代码打分，并返回逐项的 PASS/FAIL 反馈，附带原因和具体修复方向。
- 生成器会在任何环境执行之前，依据评分标准和验证器反馈修改代码。
- 这个循环会在代码得分达到 10/10、耐心耗尽或轮次上限到达时停止；得分最高的候选代码会成为唯一要执行的动作。
- 该方法不需要训练，使用的是推理阶段验证，而不是模型微调或执行反馈。

## 结果
- 在 M3ToolEval 上，RubricRefine 在七个模型上的平均成功率为 0.86，而单次通过的 CodeAct 为 0.62，绝对提升 0.24。
- RubricRefine 在所有测试模型上都最好：GPT-4.1-mini 为 0.86，GPT-4o 为 0.86，o3-mini 为 0.85，GPT-4.1 为 0.85，Gemma-4-26B 为 0.85，Qwen3.6-27B 为 0.84，Sonnet-4.6 为 0.88。
- 与 CodeAct 相比，论文报告 M3ToolEval 上各模型的提升为 +0.14 到 +0.38，所有模型的配对 t 检验都达到 p<0.001。
- RubricRefine 比使用真实执行反馈的 Self-Debug 平均高出 0.12 绝对值：0.86 对 0.74。
- 固定版 RubricRefine 在七个模型中的六个上都比 Self-Refine 高出 +0.09 到 +0.20，而完整 RubricRefine 在每个模型上都比固定版再高 +0.04 到 +0.12。
- 在以单步为主的基准 API-Bank 上，RubricRefine 在四个 OpenAI 模型上的表现与 CodeAct 基本持平，或落在噪声范围内，这与该方法在包含工具间契约的任务上更有效的说法一致。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09730v3](https://arxiv.org/abs/2605.09730v3)
