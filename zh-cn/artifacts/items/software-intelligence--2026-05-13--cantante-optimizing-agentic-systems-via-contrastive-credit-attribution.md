---
source: arxiv
url: https://arxiv.org/abs/2605.13295v1
published_at: '2026-05-13T10:09:10'
authors:
- Tom Zehle
topics:
- multi-agent-systems
- prompt-optimization
- credit-assignment
- code-generation
- software-agents
- agentic-ai
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# CANTANTE: Optimizing Agentic Systems via Contrastive Credit Attribution

## Summary
## 摘要
CANTANTE 通过把一个系统级分数转换为每个智能体的提示词更新信号，来优化 LLM 多智能体系统。与 GEPA 和 MIPROv2 相比，它在 MBPP、GSM8K 和 HotpotQA 上报告了最高的平均排名。

## 问题
- 多智能体 LLM 系统需要面向任务的提示词、角色和工作流；随着智能体数量增加，手动调优成本会上升。
- 评估通常只返回整个工作流的一个分数，而可调参数属于各个智能体。
- 这会影响软件和推理系统，因为错误的最终答案应更新导致错误的智能体，而不是把同一个信号推入每个提示词。

## 方法
- CANTANTE 保持工作流图固定，并把每个智能体提示词视为可学习的局部参数。
- 在每次迭代中，每个局部优化器提出 K 个提示词候选。该方法形成 K 个联合多智能体配置，并在同一组查询上运行它们。
- 一个由提示词驱动的 LLM 归因器在小组内比较 rollout 轨迹和最终分数，然后为每个 rollout 中的每个智能体分配一个位于 [-1, 1] 的标量信用值。
- 每个智能体的局部优化器接收自己的提示词-信用值对，并更新该智能体下一轮使用的提示词。
- 默认实现使用 CAPO 作为局部提示词优化器，使用 GPT-OSS-120B 作为归因和优化模型；下游任务智能体使用 Qwen3，总参数量为 30B，激活参数量为 3B。

## 结果
- 在 9 个基准-种子组合中，CANTANTE 在 6 个案例中取得最高测试分数，并获得最佳平均排名：1.44；MIPROv2 为 2.33，GEPA 为 2.67，初始提示词为 3.44。
- 在 MBPP 代码生成上，CANTANTE 达到 41.89% 准确率 ± 7.56；GEPA 为 22.96% ± 18.30，MIPROv2 为 18.42% ± 14.13，初始提示词为 5.54% ± 1.62。它比最强基线高 +18.93 个百分点。
- 在 GSM8K 上，CANTANTE 达到 82.33% ± 4.35；MIPROv2 为 69.80% ± 7.10，GEPA 为 61.27% ± 2.66，初始提示词为 59.20% ± 10.73。它比最强基线高 +12.53 个百分点。
- 在 HotpotQA 上，CANTANTE 达到 11.93% ± 5.06，低于 MIPROv2 的 14.20% ± 5.72，但高于初始提示词的 9.67% ± 3.00 和 GEPA 的 10.93% ± 3.91。
- 在 MBPP 和 GSM8K 上，CANTANTE 的评估时 token 用量更低：每个查询分别为 1.99k 和 1.74k token；初始提示词为 2.11k 和 1.81k，MIPROv2 为 2.09k 和 2.11k，GEPA 为 2.28k 和 1.79k。在 HotpotQA 上，CANTANTE 使用了更多 token：2.28k；初始提示词为 1.17k，MIPROv2 为 1.71k，GEPA 为 1.54k。
- 一项 GSM8K 消融实验显示，在相同步数下，用直接全局分数归因替换对比归因会使准确率下降 13.40 个百分点；在相同预算下会下降 4.40 个百分点。把对比组大小降至 2 会导致 54.40 个百分点的下降，而组大小为 5 时比默认组大小 3 高 0.80 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13295v1](https://arxiv.org/abs/2605.13295v1)
