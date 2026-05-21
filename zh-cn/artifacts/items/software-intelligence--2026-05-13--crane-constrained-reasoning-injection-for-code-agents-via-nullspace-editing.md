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
## 摘要
CRANE 是一种无需训练的权重编辑方法，可将 Thinking 检查点中的推理行为注入 Instruct 代码智能体检查点，同时保留工具调用规范。

## 问题
- 代码智能体需要在同一模型中完成长周期规划、代码库状态跟踪，并严格遵守工具使用格式。
- Qwen Thinking 检查点会进行更多推理，但可能过度思考、消耗更多输出 token，并在作为智能体时表现更差：在 Roo-Eval 上，30B 规模下 Thinking 的 pass@1 为 34.9%，Instruct 为 46.7%；80B 规模下 Thinking 为 35.4%，Instruct 为 72.8%。
- 这个问题很关键，因为即使推理轨迹看起来更强，代码智能体也可能因使用错误 schema、在错误时间调用工具，或消耗过多上下文而失败。

## 方法
- CRANE 从成对检查点之间的权重差开始：delta = Thinking 权重减去 Instruct 权重。
- 它使用幅度阈值筛选，只保留较大的 delta 坐标，并移除可能增加噪声的小更新。
- Conservative Taylor Gate 使用带掩码的校准损失为每个层/组件块打分，保留同时降低推理迁移损失和智能体行为保留损失的方向。
- Graduated Sigmoidal Projection 使用 Instruct 在格式关键轨迹上的激活，抑制会扰动工具分隔符、JSON/schema token 和聊天模板控制 token 的更新方向。
- 最终模型是经过编辑的 Instruct 检查点，不需要重新训练。

## 结果
- 在使用 Qwen3-30B-A3B 的 Roo-Eval 上，CRANE 达到 129/195 pass@1，即 66.2%；Instruct 为 46.7%，Thinking 为 34.9%，列出的最佳非 CRANE 合并方法为 47.2%。
- 在使用 Qwen3-Next-80B-A3B 的 Roo-Eval 上，CRANE 达到 159/195 pass@1，即 81.5%；Instruct 为 72.8%，Thinking 为 35.4%，AIM-TA 为 80.5%。
- 在 SWE-bench-Verified 上，CRANE 在 30B 规模解决 122/500 个实例，在 80B 规模解决 180/500 个实例；论文报告称，相比 Instruct 分别增加 +14 和 +12 个实例，相比这些规模下最强的合并基线分别增加 +9 和 +7 个实例。
- 在 Terminal-Bench v2 上，CRANE 报告的 pass@1/pass@5 在 30B 规模为 7.6%/17.9%，在 80B 规模为 14.8%/30.3%；pass@1 最高提升 +2.3 个百分点，pass@5 最高提升 +7.8 个百分点。
- 在 30B 规模的 Roo-Eval 上，CRANE 将 TTC 降至 120.9M，Instruct 为 181.1M，同时 pass@1 提高 19.5 个百分点；在 80B 规模下，CRANE 报告的 TTC 为 89.2M，Instruct 为 89.6M。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14084v1](https://arxiv.org/abs/2605.14084v1)
