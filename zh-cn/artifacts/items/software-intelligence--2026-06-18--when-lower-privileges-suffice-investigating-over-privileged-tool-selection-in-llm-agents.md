---
source: arxiv
url: https://arxiv.org/abs/2606.20023v1
published_at: '2026-06-18T09:54:48'
authors:
- Kaiyue Yang
- Yuyan Bu
- Jingwei Yi
- Yuchi Wang
- Biyu Zhou
- Juntao Dai
- Songlin Hu
- Yaodong Yang
topics:
- llm-agents
- tool-use-safety
- least-privilege
- agent-benchmarks
- privilege-escalation
- post-training
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents

## Summary
## 摘要
论文发现，LLM 智能体即使在低权限工具可以完成任务时，也经常选择更高权限的工具。论文提出 ToolPrivBench 和一种权限感知的后训练方法，用于测量并减少这种行为。

## 问题
- LLM 智能体现在会自主选择工具，而工具权限会影响错误、攻击或不安全默认设置造成的损害。
- 现有工具选择研究主要测试元数据偏差或有害行为，对允许工具之间的最小权限选择测试不足。
- 短暂错误可能促使智能体提升权限，即使另一个低权限工具仍然可用。

## 方法
- ToolPrivBench 为每个案例提供 6 个工具：3 个低权限工具和 3 个高权限工具。每个工具都被设计为足以完成任务，因此使用高权限工具可以视为选择失败。
- 该基准测试 2 种行为：第一次工具调用时的激进选择，以及在临时且与权限无关的故障后的过早升级。
- 它报告 OPUR@k，即在仍有足够的低权限工具可用时使用高权限工具的比例；还报告 PED，即升级前尝试过的不同低权限工具数量。
- 数据集包含 8 个领域、5 类风险中的 544 个场景，工具充分性由 Gemini 2.5 Pro、GPT-5.2 和人工评审检查。
- 提出的缓解方法用监督样例和 GRPO 奖励训练智能体，使其优先选择足够的低权限工具，在短暂错误后重试，并且只在需要时升级权限。

## 结果
- 在评估的 11 个 LLM 中，6 个模型的 OPUR 超过 30%。Qwen3-8B 的 OPUR 达到 64.9%，LLaMA-3.1-8B 达到 55.9%。
- OPUR 较低的模型仍有一些失败：在报告的分析中，Claude 4.6 Sonnet、GPT-5.2 和 GLM-5 的总体 OPUR 均低于 10%。
- 短暂故障会增加权限升级。对于 GPT-5.2，过度权限案例在 PED=0 时出现 5 次，在 PED=1 时出现 13 次，在 PED=2 时出现 35 次。
- 风险类型会影响结果：LLaMA-3.1-8B 在权限升级上的 OPUR 达到 72.7%，在安全绕过上达到 74.1%；Qwen3.5-397B 在这两类风险上的 OPUR 分别达到 42.4% 和 45.7%。
- 通用安全对齐迁移效果较差。AgentAlign 将 Ministral-8B-Instruct 的 AgentHarm 有害评分从 67.4% 降至 10.5%，但 OPUR 仅从 68.8% 降至 62.5%；对于 Qwen2.5-7B-Instruct，OPUR 从 50.4% 升至 60.7%。
- 摘录称，权限感知后训练减少了不必要的高权限工具使用，同时保留了通用能力，但没有包含最终的数值缓解表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20023v1](https://arxiv.org/abs/2606.20023v1)
