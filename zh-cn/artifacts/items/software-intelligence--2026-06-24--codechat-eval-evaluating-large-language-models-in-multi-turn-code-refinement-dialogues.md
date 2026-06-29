---
source: arxiv
url: https://arxiv.org/abs/2606.25747v1
published_at: '2026-06-24T12:16:04'
authors:
- Guoxiang
- Guo
- Kla Tantithamthavorn
- Neelofar Neelofar
- Yuanyuan Qi
- Aldeida Aleti
topics:
- code-intelligence
- software-foundation-models
- code-generation
- multi-turn-evaluation
- llm-benchmarks
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues

## Summary
## 摘要
CodeChat-Eval 测试代码类 LLM 在开发者后续修改中，能否让已经正确的代码继续保持正确。论文发现，在 10 轮代码细化对话中，正确性出现大幅回退。

## 问题
- HumanEval、MBPP、SWE-Bench、BigCodeBench 等现有代码基准主要测试单次请求，因此无法捕捉后续细化指令导致的回退。
- 这个场景很重要，因为开发者经常要求后续修改，例如清理代码风格、重构，或改用另一种实现策略，同时仍希望原有行为保持不变。
- 论文同时测量两件事：细化后的代码是否仍能通过原始测试，以及模型是否遵循了修改指令。

## 方法
- CodeChat-Eval 从 542 个编程任务开始：164 个来自 HumanEval，378 个来自 MBPP。
- 每个评估会话有 10 轮：1 轮初始代码生成，以及 9 轮后续细化。
- 细化指令来自 CodeAlignBench。作者整理了 169 条原始指令，过滤掉 11 条会改变功能或破坏测试框架的指令，并按作用范围和变更操作对其余指令分类。
- 作用范围类别包括外观、结构和语义。变更操作包括添加、删除和修改。
- 一个由议程引导的动态指令选择算法会在每一轮为当前代码选择一条适用指令，然后用原始测试套件测试新代码，并用 LLM 裁判检查指令遵循情况。

## 结果
- 研究评估了来自 Llama、Qwen、DeepSeek 和 GPT 系列的 8 个开放权重和专有 LLM。
- 与此前的正确状态相比，多轮细化后，GPT-5 Nano 的功能正确性下降 19.2%，Llama 3.1 8B 下降 69.2%。
- 论文报告称，所有被评估的 LLM 都出现了具有统计显著性的正确性下降。
- 语义细化指令在作用范围层面的影响最大，正确性下降 21%。
- 添加型变更请求在操作层面的影响最大，正确性下降 17%。
- 作者选择 10 轮设置，是为了覆盖其引用的真实世界对话长度中的 95%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25747v1](https://arxiv.org/abs/2606.25747v1)
