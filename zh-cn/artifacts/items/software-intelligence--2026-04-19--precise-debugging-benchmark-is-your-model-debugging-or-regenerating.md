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
PDB 是一个调试基准，用来检查模型是在做有针对性的修复，还是在大段重写程序。论文显示，强代码模型往往能通过测试，但会做很多不必要的编辑，所以单看单元测试准确率会掩盖调试能力不足。

## 问题
- 现有调试基准通常用单元测试通过率给模型打分，因此最小修复、整段重写，以及某些硬编码做法，看起来可能一样好。
- 真实调试需要先定位故障，再做小而可审查的编辑；在真实代码库里，广泛重生成代价高，也更容易出错。
- 现有评估还会漏掉多 bug 程序中的部分进展，因为修复一个 bug 和一个都没修复，二元分数可能一样。

## 方法
- 作者提出 **Precise Debugging Benchmarking (PDB)**，这是一条把现有代码数据集转成调试基准的流程，通过向正确程序注入已验证的 bug 来生成样本。
- PDB 先创建带有已知真实编辑的 **atomic bugs**，再把彼此独立的 bug 组合成多 bug 程序，这样每个 bug 都能单独测量。
- 这个基准在单元测试之外加入了两个指标：**edit-level precision**，衡量实际需要了多少编辑；以及 **bug-level recall**，衡量真正修复了多少个 bug。
- 论文发布了两个基准：**PDB-Single-Hard**，包含 5,751 个基于单行 bug 的困难样本；以及 **PDB-Multi**，包含 256 个基于连续多行 bug 的样本。
- 评测还测试了单次、迭代和 agentic 调试设置，看额外尝试或反馈能否改善精确编辑。

## 结果
- 在 **PDB-Single-Hard** 上，**GPT-5.1-Codex** 的单元测试分数是 **76.1%**，但只有 **39.7% precision** 和 **71.7% recall**。**DeepSeek-V3.2-Thinking** 的单元分数是 **79.0%**，对应 **45.0% precision** 和 **71.2% recall**。
- 单元测试通过率更低的模型，可能反而更会精确调试：**Qwen3-Coder-480B** 的单元分数是 **70.3%**，但 **65.8% precision** 和 **77.2% recall**。
- PDB-Single-Hard 上 precision 最好的模型是 **Claude-4.5-Sonnet**，precision 为 **71.8%**、recall 为 **81.4%**、单元分数为 **75.7%**；**Gemini-2.5-Pro** 的 precision 为 **71.4%**、recall 为 **83.5%**、单元分数为 **78.1%**。即便如此，这些模型的 precision 仍低于 **72%**。
- 在 **PDB-Multi** 上，差距仍然存在：**GPT-5.1-Codex** 的单元测试分数最高，为 **77.0%**，但 precision 只有 **27.9%**、recall 为 **59.4%**；**Claude-4.5-Sonnet** 的 precision 为 **65.9%**、recall 为 **73.9%**、单元分数为 **64.8%**；**Gemini-2.5-Pro** 的 precision 为 **57.8%**、recall 为 **73.2%**、单元分数为 **72.7%**。
- 迭代式和 agentic 调试能提高单元测试分数和 recall，但论文指出它们并没有在有意义的程度上提高 precision；即便是 **Claude-Code**，在 agentic 设置下 precision 也只有大约 **50%**。
- 提示词也会影响结果：自由形式的调试会降低 precision 和 recall。论文报告说，即使是强模型，在自由形式提示下 precision 也会降到 **60%** 以下，而 **Gemini-2.5-Pro** 在这项消融中 precision 下降了约 **40 个百分点**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17338v2](http://arxiv.org/abs/2604.17338v2)
