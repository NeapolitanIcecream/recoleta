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
本文认为，代码代理如果不是按端到端任务基准训练，而是按一小组可复用的软件工程技能训练，泛化会更好。文章定义了五项原子技能，并用联合强化学习把它们一起训练到同一个共享代理上。

## 问题
- 现有代码代理通常按 bug 修复这类复合任务训练，文章认为这会导致针对特定任务的过拟合，并且对其他软件工程任务的迁移能力较弱。
- 复合任务很难用强化学习扩展，因为任务空间很大，而且每新增一个任务都要重新设计奖励，成本高，标准也不一致。
- 作者希望找到一种更容易评估、能在不同工作流中复用、也更可能迁移到未见任务的训练目标。

## 方法
- 文章定义了五项原子技能：代码定位、代码编辑、单元测试生成、问题复现和代码审查。
- 每项技能都有明确的输入输出格式和基于执行结果的奖励：定位用文件完全匹配，编辑用所有测试通过，单元测试生成用能发现 bug 的测试，审查用正确的二分类判断，问题复现用补丁前失败、补丁后通过。
- 先用 1,500 条已验证轨迹做轻量 SFT 初始化一个共享策略，每项技能 300 条，起始模型是 GLM-4.5-Air-Base。
- 然后在统一任务缓冲区上对所有原子技能做联合 RL，用 GRPO 比较同一输入的多个采样输出，并减少不同技能之间的奖励尺度不一致。
- 训练在沙盒环境中进行，只允许 bash 和 str_replace 工具，使用 10,000+ 并发沙盒和 25,000+ 预构建 Docker 镜像。

## 结果
- 核心结论是，在 **10** 个任务上平均提升 **18.7%**，其中包括 **5** 项原子技能和 **5** 项复合任务。
- 在原子技能上（Avg@3），SFT+RL 在五项技能上都优于 SFT：代码定位 **0.665 -> 0.712**，代码编辑 **0.458 -> 0.611**，问题复现 **0.542 -> 0.605**，单元测试生成 **0.359 -> 0.472**，代码审查 **0.563 -> 0.622**。
- 在未见过的复合任务上（Avg@3），SFT+RL 在五个基准上都优于 SFT：SWE-bench Verified **0.507 -> 0.585**，SWE-bench Multilingual **0.300 -> 0.389**，Terminal-Bench 2.0 **0.151 -> 0.182**，Code Refactoring **0.146 -> 0.171**，SEC-Bench **0.136 -> 0.169**。
- 按论文报告的所有任务平均，联合 RL 达到 **0.452 Avg@3**，高于 SFT 模型的 **0.383** 和 GLM-4.5-Air 的 **0.416**。
- 在原子技能上，与 GLM-4.5-Air 相比，联合 RL 模型更高：定位 **0.712 vs 0.666**，编辑 **0.611 vs 0.556**，问题复现 **0.605 vs 0.555**，单元测试生成 **0.472 vs 0.423**，审查 **0.622 vs 0.536**。
- 在复合基准上，与 GLM-4.5-Air 相比，联合 RL 模型在 SWE-bench Verified **0.585 vs 0.559**、SWE-bench Multilingual **0.389 vs 0.358**、Code Refactoring **0.171 vs 0.159**、SEC-Bench **0.169 vs 0.163** 上更高，但在 Terminal-Bench 2.0 上更低，**0.182 vs 0.187**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05013v1](http://arxiv.org/abs/2604.05013v1)
