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
CANTANTE 将一个系统级分数转换为逐个代理的提示更新信号，从而优化基于 LLM 的多代理系统。它在 MBPP、GSM8K 和 HotpotQA 上对 GEPA 和 MIPROv2 取得了最佳平均排名。

## 问题
- 多代理 LLM 系统需要针对任务的提示、角色和工作流，随着代理数量增加，手动调参成本也会上升。
- 评估通常只给出整个工作流的一个分数，而可调参数属于单个代理。
- 这对软件系统和推理系统很重要，因为最终答案出错时，应更新造成错误的那个代理，而不是把同样的信号推给每个提示。

## 方法
- CANTANTE 保持工作流图不变，并把每个代理的提示当作可学习的局部参数。
- 每次迭代中，每个局部优化器提出 K 个提示候选。方法构造 K 个联合多代理配置，并在同一组查询上运行它们。
- 一个带提示的 LLM 归因器在小组内比较 rollout 轨迹和最终分数，然后为每个 rollout 中的每个代理分配一个介于 [-1, 1] 的标量 credit。
- 每个代理的局部优化器接收自己的提示-信用对，并在下一轮更新该代理的提示。
- 默认实现使用 CAPO 作为局部提示优化器，使用 GPT-OSS-120B 作为归因和优化模型，而下游任务代理使用 Qwen3，总参数量为 30B，激活参数量为 3B。

## 结果
- 在 9 组 benchmark-seed 组合中，CANTANTE 有 6 组拿到测试集最高分，平均排名也最好：1.44；MIPROv2 为 2.33，GEPA 为 2.67，初始提示为 3.44。
- 在 MBPP 代码生成任务上，CANTANTE 达到 41.89% 准确率 ± 7.56；GEPA 为 22.96% ± 18.30，MIPROv2 为 18.42% ± 14.13，初始提示为 5.54% ± 1.62。它比最强基线高出 18.93 个百分点。
- 在 GSM8K 上，CANTANTE 达到 82.33% ± 4.35；MIPROv2 为 69.80% ± 7.10，GEPA 为 61.27% ± 2.66，初始提示为 59.20% ± 10.73。它比最强基线高出 12.53 个百分点。
- 在 HotpotQA 上，CANTANTE 达到 11.93% ± 5.06，低于 MIPROv2 的 14.20% ± 5.72，但高于初始提示的 9.67% ± 3.00 和 GEPA 的 10.93% ± 3.91。
- 评估时的 token 使用量在 MBPP 和 GSM8K 上更低：CANTANTE 分别为每个查询 1.99k 和 1.74k tokens；初始提示为 2.11k 和 1.81k，MIPROv2 为 2.09k 和 2.11k，GEPA 为 2.28k 和 1.79k。在 HotpotQA 上，CANTANTE 使用的 token 更多：2.28k；初始提示为 1.17k，MIPROv2 为 1.71k，GEPA 为 1.54k。
- GSM8K 的消融实验显示，在相同步数下，用直接的全局分数归因替换对比式归因会让准确率下降 13.40 个百分点；在相同预算下会下降 4.40 个百分点。把对比组大小降到 2 会让性能下降 54.40 个百分点；组大小 5 比默认的组大小 3 高 0.80 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13295v1](https://arxiv.org/abs/2605.13295v1)
