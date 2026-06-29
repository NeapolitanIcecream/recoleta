---
source: arxiv
url: https://arxiv.org/abs/2605.14084v1
published_at: '2026-05-13T20:09:35'
authors:
- Mingzhi Zhu
- Michele Merler
- Raju Pavuluri
- Stacy Patterson
topics:
- code-agents
- model-merging
- software-foundation-models
- tool-use
- code-intelligence
- parameter-editing
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# CRANE: Constrained Reasoning Injection for Code Agents via Nullspace Editing

## Summary
## 总结
CRANE 是一种无需训练的权重编辑方法，它把 Thinking 检查点中的推理行为注入到 Instruct 代码代理检查点，同时保留工具调用的纪律性。

## 问题
- 代码代理需要在同一个模型里同时处理长程规划、仓库状态跟踪和严格的工具使用格式。
- Qwen 的 Thinking 检查点更会推理，但会过度思考、输出更多 token，而且作为代理时表现更差：在 Roo-Eval 上，30B 时 Thinking 的 pass@1 为 34.9%，Instruct 为 46.7%；80B 时分别为 35.4% 和 72.8%。
- 这个问题很重要，因为代码代理即使推理轨迹更强，也可能因为使用了错误的 schema、在错误的时机调用工具，或者消耗掉上下文而失败。

## 方法
- CRANE 从成对检查点的权重差开始：delta = Thinking 权重减去 Instruct 权重。
- 它先做幅值阈值筛选，只保留较大的 delta 坐标，去掉可能带来噪声的小更新。
- Conservative Taylor Gate 用带掩码的校准损失给每个层或组件块打分，保留那些能同时降低推理迁移损失和代理行为保持损失的方向。
- Graduated Sigmoidal Projection 使用 Instruct 在格式关键轨迹上的激活，压制那些会扰动工具分隔符、JSON/schema token 和 chat-template 控制 token 的更新方向。
- 最终模型是一个编辑后的 Instruct 检查点，不需要重新训练。

## 结果
- 在使用 Qwen3-30B-A3B 的 Roo-Eval 上，CRANE 的 pass@1 为 129/195，即 66.2%，而 Instruct 为 46.7%，Thinking 为 34.9%，列表中最好的非 CRANE 合并方法为 47.2%。
- 在使用 Qwen3-Next-80B-A3B 的 Roo-Eval 上，CRANE 的 pass@1 为 159/195，即 81.5%，而 Instruct 为 72.8%，Thinking 为 35.4%，AIM-TA 为 80.5%。
- 在 SWE-bench-Verified 上，CRANE 在 30B 时解决了 122/500 个样例，在 80B 时解决了 180/500 个样例；论文报告称，相比 Instruct 分别多出 14 和 12 个实例，相比这两个规模下最强的合并基线分别多出 9 和 7 个实例。
- 在 Terminal-Bench v2 上，CRANE 在 30B 时的 pass@1/pass@5 为 7.6%/17.9%，在 80B 时为 14.8%/30.3%，pass@1 最多提升 2.3 个百分点，pass@5 最多提升 7.8 个百分点。
- 在 30B 的 Roo-Eval 上，CRANE 的 TTC 为 120.9M，Instruct 为 181.1M，同时 pass@1 提高了 19.5 个百分点；在 80B 上，TTC 为 89.2M，而 Instruct 为 89.6M。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14084v1](https://arxiv.org/abs/2605.14084v1)
