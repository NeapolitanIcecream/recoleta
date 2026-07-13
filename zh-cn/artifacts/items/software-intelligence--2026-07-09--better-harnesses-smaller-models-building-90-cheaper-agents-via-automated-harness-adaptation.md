---
source: arxiv
url: https://arxiv.org/abs/2607.08938v1
published_at: '2026-07-09T21:08:01'
authors:
- Chenyang Yang
- Xinran Zhao
- Tongshuang Wu
- "Christian K\xE4stner"
topics:
- small-language-models
- agent-harnesses
- automated-harness-optimization
- software-agents
- inference-cost
- business-workflows
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation

## Summary
## 摘要
论文显示，在常规商业工作流中，经过自动适配智能体框架后，小型语言模型可以达到接近前沿智能体的性能。适配效果最好的智能体达到了 LLM 性能的 89.7%，成本仅为其 4%。

## 问题
- 前沿 LLM 智能体在大规模部署时成本高、速度慢；小型语言模型被放入为大型模型设计的框架后，通常会出现性能下降。
- 这一问题关系到常规商业工作流的可靠执行、低推理成本、本地部署和更好的隐私保护。这些工作流通常不需要开放式生成。

## 方法
- 论文将智能体失败分为工具使用、指令遵循、知识、长上下文和规划等类型，并将其对应到三类适配方式：上下文、工具和智能体循环。
- 一个元智能体通过修改提示词、技能、工具、钩子、上下文管理方式和子智能体，自动编辑软件智能体框架。
- 优化器评估候选框架，检查失败轨迹，提出针对性修改，运行健全性检查，并保留能提升验证集性能的候选方案。
- 该方法将可重复的工作流知识和控制逻辑从语言模型转移到提示词、自定义工具、筛选后的工具集和运行时保护机制中。

## 结果
- 在 7 项商业任务、3 个 SLM 系列和 21 个任务-模型组合中，优化后的框架提升了其中 16 个组合的性能，并在 7 个组合中弥合了 SLM 与 LLM 之间的性能差距。
- 性能最好的 SLM 智能体达到了 LLM 智能体 89.7% 的性能，同时降低了 96% 的成本，即成本约为 LLM 的 4%。
- 在预算审批示例中，Gemma-4-26B-A4B 使用默认框架时的准确率为 75.0%，使用适配后的框架后提升至 98.3%；Gemini-3.1-Pro 的准确率为 97.3%，LLM 每次查询的成本为 $0.22。
- 成功的适配最常解决指令遵循和知识方面的失败，这两类问题各出现在 81% 的成功适配中；86% 的适配增加了上下文，43% 创建了工具，29% 管理了工具。
- 当任务实例从多样性最高的设置变为多样性最低的设置时，适配使准确率提高了 21.1 个百分点。
- 更强的 SLM 从适配中获得的收益更大：报告中的提升幅度分别为 48.8% 和 15.5%，这表明框架修改无法弥补模型核心能力的缺失。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08938v1](https://arxiv.org/abs/2607.08938v1)
