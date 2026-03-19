---
source: hn
url: https://news.ycombinator.com/item?id=47317413
published_at: '2026-03-09T23:51:33'
authors:
- dsrtslnd23
topics:
- llm-architecture
- model-scaling
- mixture-of-experts
- inference-time-compute
- closed-vs-open-models
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Ask HN: Any informed guesses on the actual size/architecture of GPT-5.4 etc.?

## Summary
这不是一篇研究论文，而是一则 Hacker News 提问，讨论 GPT-5.4、Gemini 3.1、Opus 4.6 等闭源模型的参数规模、架构形式以及“Pro”版本是否主要依赖更多推理时计算。文本本身没有给出实验、方法或证据，只提出了关于模型大小、MoE 形态和推理编排的猜测性问题。

## Problem
- 试图弄清当前顶级闭源大模型与最佳开源模型相比，**实际有多大、采用什么架构**。
- 关注这些模型是否大致都处在**约 1T 参数、可能为 MoE** 的同一区间，还是闭源模型仍显著更大。
- 追问所谓 **Pro 版本** 是独立模型，还是主要通过**更多推理时计算、更长链路推理或更强 orchestration** 获得提升；这关系到业界对能力来源与成本结构的判断。

## Approach
- 文本没有提出研究方法；其核心形式是**基于公开产品名与行业常识的开放式推测**。
- 问题围绕三个简单维度展开：**参数规模**、**模型架构（如 MoE）**、**推理时计算/编排差异**。
- 还引入了一个比较框架：将 **GPT-5.4、Gemini 3.1、Opus 4.6** 与 **GLM-5** 等开源模型放在同一尺度上进行直觉比较。
- 就最简单地说，这段内容的“机制”就是：**向社区征求线索，判断能力差异究竟更多来自训练出的底座模型，还是来自运行时投入的额外算力与工具链编排**。

## Results
- **没有提供任何定量结果**，没有数据集、指标、基线、实验设置或数值比较。
- 最强的具体陈述只是若干待验证假设：闭源模型可能在**约 1T 参数**量级，并且**可能采用 MoE**。
- 文本提出但未回答的比较对象包括：**GPT-5.4、Gemini 3.1、Opus 4.6、GLM-5**。
- 文本提出但未证明的关键判断是：**“Pro”版本可能不是完全不同的模型，而是同一底模叠加更多 inference-time compute、更长 reasoning 或更强 orchestration**。
- 因为没有证据与实验，无法得出任何关于性能提升幅度、架构优劣或规模差异的可靠结论。

## Link
- [https://news.ycombinator.com/item?id=47317413](https://news.ycombinator.com/item?id=47317413)
