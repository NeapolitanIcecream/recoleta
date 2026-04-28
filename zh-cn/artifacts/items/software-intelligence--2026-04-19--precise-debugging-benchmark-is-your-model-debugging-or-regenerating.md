---
source: arxiv
url: http://arxiv.org/abs/2604.17338v2
published_at: '2026-04-19T09:08:23'
authors:
- Wang Bill Zhu
- Miaosen Chai
- Shangshang Wang
- Yejia Liu
- Song Bian
- Honghua Dong
- Willie Neiswanger
- Robin Jia
topics:
- debugging-benchmark
- code-llm-evaluation
- precise-editing
- agentic-debugging
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Precise Debugging Benchmark: Is Your Model Debugging or Regenerating?

## Summary
## 摘要
PDB 是一个调试基准，用来检查模型是在做有针对性的修复，还是重写了程序的大部分内容。论文显示，强代码模型常常能通过测试，但会做出许多不必要的修改，因此只看单元测试准确率会掩盖调试行为较弱的问题。

## 问题
- 现有调试基准主要按单元测试通过率给模型打分，因此最小修复、完整重写，以及某些形式的硬编码，可能看起来同样好。
- 真实调试需要定位故障，并进行小而便于审查的修改；大范围重新生成在真实代码库中成本高、风险也高。
- 现有评估也无法反映多缺陷程序中的部分进展，因为修复一个缺陷和一个都没修复，可能得到相同的二元分数。

## 方法
- 作者提出了 **Precise Debugging Benchmarking (PDB)**，这是一条把现有代码数据集转换为调试基准的流程，方法是在正确程序中注入经过验证的缺陷。
- PDB 先构造带有已知真实编辑的 **atomic bugs**，再把彼此独立的缺陷组合成多缺陷程序，这样每个缺陷都可以单独测量。
- 该基准在单元测试之外增加了两个指标：**edit-level precision**，衡量实际修改中有多少是必要的；**bug-level recall**，衡量真正修复了多少个缺陷。
- 它发布了两个基准：**PDB-Single-Hard**，包含 5,751 个由单行缺陷构建的高难度样例；**PDB-Multi**，包含 256 个由连续多行缺陷构建的样例。
- 评估还测试了单次、迭代式和 agentic 调试设置，以检验额外尝试或反馈是否能提升精确编辑能力。

## 结果
- 在 **PDB-Single-Hard** 上，**GPT-5.1-Codex** 的单元测试得分为 **76.1%**，但 **precision** 只有 **39.7%**，**recall** 为 **71.7%**。**DeepSeek-V3.2-Thinking** 的单元测试得分为 **79.0%**，对应 **45.0% precision** 和 **71.2% recall**。
- 单元测试通过率较低的模型，可能反而是更精确的调试器：**Qwen3-Coder-480B** 的单元测试得分为 **70.3%**，但有 **65.8% precision** 和 **77.2% recall**。
- PDB-Single-Hard 上最高的 precision 来自 **Claude-4.5-Sonnet**，其 **precision** 为 **71.8%**、**recall** 为 **81.4%**、单元测试得分为 **75.7%**；**Gemini-2.5-Pro** 的 **precision** 为 **71.4%**、**recall** 为 **83.5%**、单元测试得分为 **78.1%**。即使是这些模型，**precision** 也仍低于 **72%**。
- 在 **PDB-Multi** 上，同样的差距依然存在：**GPT-5.1-Codex** 以 **77.0%** 拿到最高单元测试得分，但 **precision** 只有 **27.9%**，**recall** 为 **59.4%**；**Claude-4.5-Sonnet** 达到 **65.9% precision**、**73.9% recall**、**64.8%** 单元测试得分；**Gemini-2.5-Pro** 为 **57.8% precision**、**73.2% recall**、**72.7%** 单元测试得分。
- 迭代式和 agentic 调试会提升单元测试得分和 recall，但论文指出，它们并没有以有意义的方式提升 precision；即使在 agentic 设置下，**Claude-Code** 的 precision 也只有约 **50%**。
- 提示方式会影响结果：自由形式调试会降低 precision 和 recall。论文报告，即使是强模型，在自由形式提示下 precision 也会降到 **60%** 以下，而 **Gemini-2.5-Pro** 在该消融实验中 precision 下降了约 **40 个百分点**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17338v2](http://arxiv.org/abs/2604.17338v2)
