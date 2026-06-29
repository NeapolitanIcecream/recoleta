---
source: arxiv
url: https://arxiv.org/abs/2605.26177v1
published_at: '2026-05-25T06:26:43'
authors:
- Hanyu Li
- Yichi Zhang
- Speed Zhu
- Hang Su
- Jun Zhu
- Yinpeng Dong
topics:
- code-agents
- repository-context
- swe-bench
- code-intelligence
- multi-file-reasoning
- agent-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations

## Summary
## 摘要
RepoMirage 检验能否解决 SWE-Bench Verified 问题的代码代理是否能跨文件推理仓库上下文。它基于扰动的评测套件显示，当直接的局部线索被移除时，分数会大幅下降，尽管底层任务的行为保持不变。

## 问题
- 现有的仓库级基准报告的是端到端的问题修复成功率，但它们没有区分代理是否真的找到了跨文件并连接了与任务相关的信息。
- 这很重要，因为真实的代码修复通常需要追踪导入、运行时目标、常量和多文件编辑，而许多在 SWE-Bench 上成功的运行只检查了少数几个文件。
- 在论文的文件访问分析中，GPT-5 在 53.8% 的已解决案例中只检查了 1 个文件，在 88.0% 的案例中检查的文件不超过 3 个；DeepSeek-V3.2 在 55.7% 的已解决案例中也只停留在 3 个文件以内。

## 方法
- RepoMirage-Perturb 以 SWE-Bench Verified 为起点，在保留原始问题修复任务和测试的同时，对仓库做保持行为不变的扰动。
- 这三种扰动分别是：通过 4 层代理链进行依赖路径间接化、通过重命名目标和重新导出封装器进行运行时目标遮蔽，以及把局部值外部化到 JSON 资源中。
- RepoMirage-Extend 把这些结构瓶颈转成显式任务：多文件问题修复、代理链补全、运行时目标识别和缺失常量恢复。
- 论文通过 mini-swe-agent 评估了 8 个模型，并记录轨迹，用来衡量文件访问以及探索、编辑、测试动作的变化。
- RepoAnchor 是一个原型工作流，先构建与任务相关的仓库结构摘要，再用该摘要指导求解。

## 结果
- 在 RepoMirage-Perturb 上，8 个模型的平均解决率从 SWE-Bench Verified 的 66.80% 降到 49.78%，而平均访问文件数从 4.77 增加到 13.24。
- 相对解决率降幅从 Claude-Sonnet-4.6 的 15.96% 到 GPT-4.1 的 52.60% 不等；GPT-5 从 65.00% 降到 49.00%。
- 在 RepoMirage-Extend 上，8 个模型的平均成功率从原始设置下的 66.80% 降到 25.25%。
- RepoMirage-Extend 上的任务平均值分别是：多文件问题修复 17.86%，代理链恢复 17.19%，运行时目标识别 28.26%，缺失常量恢复 33.94%。
- 表 2 中 RepoMirage-Extend 的最佳总体平均值是 Gemini-3.1-Pro 的 41.40%；最低的是 GPT-4.1 的 3.40%。
- 摘要提到 RepoAnchor 通过结构化支架提高了性能，但没有给出 RepoAnchor 的具体提升数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26177v1](https://arxiv.org/abs/2605.26177v1)
