---
source: arxiv
url: https://arxiv.org/abs/2606.24245v2
published_at: '2026-06-23T07:31:03'
authors:
- Pingchuan Ma
- Zhaoyu Wang
- Zimo Ji
- Yuguang Zhou
- Zhantong Xue
- Zongjie Li
- Shuai Wang
- Xiaoqin Zhang
topics:
- llm-agent-safety
- symbolic-rules
- inductive-logic-programming
- counterexample-guided-synthesis
- code-execution-safety
- human-feedback
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# AutoSpec: Safety Rule Evolution for LLM Agents via Inductive Logic Programming

## Summary
## 摘要
AutoSpec 使用带标签的执行轨迹更新 LLM agent 的符号安全规则。它让规则保持可读，同时提升代码执行和具身 agent 安全任务上的精确率与召回率。

## 问题
- LLM agent 通过工具使用，可能删除文件、泄露凭据、发送不安全的网络调用，或违反物理世界约束。
- 手写安全规则便于审计，但随着模型、工具、提示词和工作负载变化，规则会逐渐偏离实际需求。
- 神经安全分类器可以适应变化，但无法提供安全敏感部署中审查所需的清晰规则逻辑。

## 方法
- AutoSpec 从专家规则集、谓词库，以及由用户或审查者标注为安全或不安全的轨迹开始。
- 它在这些轨迹上运行当前规则，然后收集误报和漏报作为反例。
- Inductive Logic Programming 通过 ILASP 实现，用于找出能区分漏掉的不安全轨迹与被错误阻止的安全轨迹的谓词。
- 系统将这些谓词转换为规则编辑，例如添加例外、添加合取条件、放宽条件，或添加析取分支。
- 验证器在带标签的轨迹上为候选规则集打分，只有当某次编辑提高分数时才保留它。

## 结果
- 评估使用了 291 条执行轨迹，覆盖代码执行和具身 agent 领域。
- AutoSpec 报告一个领域的 F1 分数为 0.98，另一个领域为 0.93。
- 论文称误报最多降低 94%，同时保持高召回率。
- ILP 引导版本的 F1 最高达到启发式 CEGIS 的 4.8 倍。
- 规则演化循环在 4 到 5 次迭代内收敛。
- 评估中使用的谓词库在每个领域包含 16 到 24 个谓词。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24245v2](https://arxiv.org/abs/2606.24245v2)
