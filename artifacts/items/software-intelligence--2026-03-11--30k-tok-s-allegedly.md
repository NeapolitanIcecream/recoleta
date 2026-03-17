---
source: hn
url: https://www.percepta.ai/blog/can-llms-be-computers
published_at: '2026-03-11T23:28:16'
authors:
- E-Reverance
topics:
- llm-inference
- program-execution
- transformers
- neural-computation
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
---

# 30k Tok/S (Allegedly)

## Summary
这篇文章提出把程序“编译”进 Transformer，使模型在推理时像执行电路一样完成计算，从而宣称可实现远快于逐token生成的推理。其核心卖点是通过在模型内部执行程序，获得带有指数级加速潜力的推理机制。

## Problem
- 现有大语言模型通常按 token 逐步生成，推理延迟高，难以像传统计算机那样高效执行结构化程序。
- 如果模型只能依赖自回归生成来“模拟”计算，那么在复杂推理、工具使用和程序执行场景中，速度与成本都会成为瓶颈。
- 这个问题之所以重要，是因为更快的内部计算机制可能改变代码智能体、自动化软件生产和更广泛 AI 系统的效率边界。

## Approach
- 文章主张让 LLM 不只是预测下一个 token，而是在 Transformer 内部直接“执行程序”。
- 简单理解：把需要做的计算过程编码成模型中的结构，让一次或少数几次前向传播相当于运行一段程序，而不是逐步把每一步都生成出来。
- 其理论叙事是：若程序可在 Transformer 中以合适形式表示，则推理复杂度可能相对传统逐token方式出现指数级改善。
- 标题中的“30k Tok/S”暗示作者将这种内部执行与超高吞吐推理联系起来，试图说明 LLM 可朝“像计算机一样工作”的方向演进。

## Results
- 提供的摘录没有给出可核验的实验设置、数据集、基线模型或完整评测表，因此**没有足够定量结果可报告**。
- 从标题可见，文章最强的量化宣称是大约 **30k tokens/s** 的速度量级，但摘录中未说明硬件、模型规模、任务类型或对比基线。
- 副标题明确宣称“**executing programs inside transformers with exponentially faster inference**”，即相比某些常规推理方式具有**指数级更快**的推理潜力，但摘录未提供证明细节。
- 基于现有文本，能确认的是：作者将贡献定位为一种把 Transformer 视作可执行程序载体的推理范式，而非标准自回归生成优化。

## Link
- [https://www.percepta.ai/blog/can-llms-be-computers](https://www.percepta.ai/blog/can-llms-be-computers)
