---
source: arxiv
url: http://arxiv.org/abs/2604.05013v1
published_at: '2026-04-06T16:36:21'
authors:
- Yingwei Ma
- Yue Liu
- Xinlong Yang
- Yanhao Li
- Kelin Fu
- Yibo Miao
- Yuchong Xie
- Zhexu Wang
- Shing-Chi Cheung
topics:
- coding-agents
- reinforcement-learning
- software-engineering
- code-intelligence
- generalization
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Scaling Coding Agents via Atomic Skills

## Summary
## 摘要
这篇论文认为，与其在端到端任务基准上训练，不如在一小组可复用的软件工程技能上训练，这样编码代理的泛化能力更强。论文定义了五种原子技能，并用联合强化学习训练一个共享代理来覆盖这五种技能。

## 问题
- 当前编码代理通常在修复 bug 这类复合任务上训练。论文认为，这会导致针对特定任务的过拟合，并且迁移到其他软件工程任务时表现较弱。
- 复合任务很难用强化学习扩展，因为任务空间很宽，每增加一种新任务都需要单独设计奖励，成本高且标准不一致。
- 作者希望找到一种更容易评估、能在不同工作流中复用、也更可能迁移到未见任务上的训练目标。

## 方法
- 论文定义了五种原子技能：代码定位、代码编辑、单元测试生成、问题复现和代码审查。
- 每种技能都有具体的输入输出格式和基于执行结果的奖励：定位用文件精确匹配，编辑用全部测试通过，单元测试生成用能检测出 bug 的测试，审查用正确的二元判断，问题复现用补丁前失败且补丁后通过。
- 一个共享策略先用轻量 SFT 初始化，训练数据是 1,500 条已验证轨迹，每种技能 300 条，起始模型是 GLM-4.5-Air-Base。
- 然后，代理在统一任务缓冲区上做联合 RL 训练，使用 GRPO 对同一输入的多个采样输出进行比较，以减少不同技能之间的奖励尺度不匹配。
- 训练在沙箱环境中进行，只使用 bash 和 str_replace 工具，配备 10,000+ 个并发沙箱，以及 25,000+ 个预构建 Docker 镜像。

## 结果
- 核心结论是：在 **10 个任务**上，模型平均性能提升 **18.7%**，其中包括 **5 种原子技能**和 **5 个复合任务**。
- 在原子技能上（Avg@3），SFT+RL 模型在五项技能上都优于 SFT：代码定位 **0.665 -> 0.712**，代码编辑 **0.458 -> 0.611**，问题复现 **0.542 -> 0.605**，单元测试生成 **0.359 -> 0.472**，代码审查 **0.563 -> 0.622**。
- 在未见过的复合任务上（Avg@3），SFT+RL 在五个基准上都优于 SFT：SWE-bench Verified **0.507 -> 0.585**，SWE-bench Multilingual **0.300 -> 0.389**，Terminal-Bench 2.0 **0.151 -> 0.182**，Code Refactoring **0.146 -> 0.171**，SEC-Bench **0.136 -> 0.169**。
- 在所有已报告任务上的平均结果中，联合 RL 达到 **0.452 Avg@3**，SFT 模型为 **0.383**，GLM-4.5-Air 为 **0.416**。
- 与 GLM-4.5-Air 在原子技能上的结果相比，联合 RL 模型在定位 **0.712 vs 0.666**、编辑 **0.611 vs 0.556**、问题复现 **0.605 vs 0.555**、单元测试生成 **0.472 vs 0.423**、审查 **0.622 vs 0.536** 上都更高。
- 在复合基准上，与 GLM-4.5-Air 相比，联合 RL 模型在 SWE-bench Verified **0.585 vs 0.559**、SWE-bench Multilingual **0.389 vs 0.358**、Code Refactoring **0.171 vs 0.159**、SEC-Bench **0.169 vs 0.163** 上更高，但在 Terminal-Bench 2.0 **0.182 vs 0.187** 上更低。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05013v1](http://arxiv.org/abs/2604.05013v1)
