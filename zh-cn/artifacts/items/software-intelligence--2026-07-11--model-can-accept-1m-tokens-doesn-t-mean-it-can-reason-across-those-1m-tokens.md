---
source: hn
url: https://twitter.com/0xCarnagee/status/2075983721841225885
published_at: '2026-07-11T23:23:57'
authors:
- annjose
topics:
- long-context-reasoning
- context-rot
- coding-agents
- continual-learning
- retrieval-evaluation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Model can accept 1M tokens doesn't mean it can reason across those 1M tokens

## Summary
## 摘要
这段摘录指出，模型能够接受 100 万个 token 的上下文，并不代表它能可靠地处理其中分散的信息。摘录称，随着上下文长度增加，检索准确率会大幅下降，并提出持续学习、使用智能体轨迹训练，以及与真实环境交互等可能的改进方法。

## 问题
- 长上下文模型可能能够接收大型输入，却无法可靠地检索或推理上下文中分散的信息。
- 这会影响编程智能体，因为大型代码仓库、很长的执行轨迹和工具输出可能超出模型可靠工作的范围。

## 方法
- 使用检索任务比较模型在 256k 和 100 万个 token 下的表现。
- 将这种失败模式称为“上下文腐化”（context rot）：随着上下文变长，推理质量下降。
- 建议采用持续学习、使用模型自身的轨迹进行训练，以及与真实环境交互，以改善智能体的长时程行为。

## 结果
- 摘录称，GPT-5.5 在 256k 个 token 下的检索得分为 80%。
- 在 100 万个 token 下，得分据称降至 36%，比 256k 的结果低 44 个百分点，相对下降 55%。
- 摘录没有提供数据集名称、评测流程、统计分析，也没有与其他模型进行比较。
- 摘录还宣传了 Andrew Ng 推出的 Claude Code 短课程，但没有证据表明该课程能提升编程智能体的性能。

## Problem

## Approach

## Results

## Link
- [https://twitter.com/0xCarnagee/status/2075983721841225885](https://twitter.com/0xCarnagee/status/2075983721841225885)
