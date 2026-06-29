---
source: arxiv
url: https://arxiv.org/abs/2605.20251v1
published_at: '2026-05-18T08:34:48'
authors:
- Jiawei He
- Jie Jia
- Chenbo Liu
- Chaoyi Xue
- Yapeng Song
- Xikai Yang
- Dong Sun
topics:
- llm-coding-agents
- code-agent-evaluation
- process-defects
- control-preservation
- software-benchmarks
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# ProcBench: Evaluating Process-Level Defects and Control Preservation in LLM Coding Agents

## Summary
## 摘要
ProcBench 通过给执行轨迹打分来评估 LLM 编码代理，而不只看最终补丁或测试结果。它会找出重复的过程缺陷，估计其风险，并为编码代理运行报告控制保持分数。

## 问题
- 现有的编码代理基准通常只给任务完成率、编译结果或测试通过率打分，所以它们可能漏掉那些过程脆弱但仍完成任务的运行。
- 这篇论文关注多步骤编码工作中的失败，包括上下文过时、重复工具调用、死步骤、长链、薄弱的工作流结构，以及不好的交接控制。
- 这很重要，因为自主编码代理在执行过程中可能需要监督、回滚或纠正，而不只是等运行结束后再看最终分数。

## 方法
- ProcBench 将原始代理日志转换为共享的轨迹格式。这个格式由按顺序排列的事件组成，包含文本、工具调用、工具返回、外部操作、上下文状态和依赖数据。
- 它检查 11 类缺陷，这些缺陷分为上下文管理、工具使用效率、工作流架构和工具系统一致性四组。
- 每个缺陷检测器先从轨迹中提取证据，再把这些证据映射为经过校准的后验风险，而不是只用硬阈值。
- 评分卡报告缺陷风险、维度级质量分数、控制保持、脆弱成功和总 ProcBench 分数。
- 控制保持通过可解释性、可中断性、可纠正性、可逆性和权限交接来评分。

## 结果
- 研究使用了 200 条标注轨迹：100 条来自 SWE-bench-Verified，40 条来自 AndroidBench，60 条来自 TerminalBench，覆盖 Claude Code、Codex CLI、OpenCode 和 Qoder 的 11 种代理-模型配置。
- 更容易观测的缺陷类能达到较高检测分数：重复步骤 F1 0.85、AUROC 0.92；幽灵上下文 F1 0.85、AUROC 0.91；死步骤 F1 0.82、AUROC 0.90；长链 F1 0.81、AUROC 0.89。
- 更难的结构性缺陷分数更低：包装器工作流 F1 0.59、AUROC 0.71；上下文耦合 F1 0.61、AUROC 0.73；弱工具 F1 0.53、AUROC 0.68。
- 校准把整体期望校准误差从硬阈值的 0.227 降到贝叶斯校准的 0.138。按维度看，上下文管理的 ECE 从 0.214 降到 0.118，工具使用效率从 0.198 降到 0.103，工作流架构从 0.271 降到 0.196，工具系统一致性从 0.223 降到 0.134。
- 使用 Claude Sonnet 4.6 的 Claude Code 报告的 ProcBench 分数最高，为 0.742，CP 为 0.75，脆弱成功率为 10.8%。使用 gpt-5.4-0305-global 的 Codex CLI 得分为 0.731，表中显示的工具使用质量最高，为 0.75。
- 使用 Qwen3 Coder Plus 的 OpenCode 报告的总分最低，为 0.648，脆弱成功率最高，为 20.2%。这说明 ProcBench 能按过程质量和控制风险，把终点表现相近的代理区分开。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20251v1](https://arxiv.org/abs/2605.20251v1)
