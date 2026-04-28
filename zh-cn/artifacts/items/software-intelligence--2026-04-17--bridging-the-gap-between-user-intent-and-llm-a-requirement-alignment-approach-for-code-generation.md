---
source: arxiv
url: http://arxiv.org/abs/2604.16198v1
published_at: '2026-04-17T16:08:05'
authors:
- Jia Li
- Ruiqi Bai
- Yangkang Luo
- Yiran Zhang
- Wentao Yang
- Zeyu Sun
- Tiankuo Zhao
- Dongming Jin
- Lei Li
- Zhi Jin
topics:
- code-generation
- requirement-alignment
- llm-evaluation
- program-synthesis
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Bridging the Gap between User Intent and LLM: A Requirement Alignment Approach for Code Generation

## Summary
## 摘要
REA-Coder 通过在写代码前后检查模型是否真正理解了需求，提升了 LLM 的代码生成表现。在 4 个 LLM 和 5 个基准上，它都超过了强推理和修复基线，在更难的竞赛编程数据集上提升最大。

## 问题
- 现有代码生成方法通常默认 LLM 已经正确理解提示，然后把重点放在更好的推理或代码修复上。
- 论文认为，很多失败更早就开始了：模型误读了需求，所以后续的规划和修复都是在错误任务上进行。
- 这很重要，因为即使模型能写出语法有效的代码，需求理解错误也会阻碍功能正确性。

## 方法
- REA-Coder 从题目描述中构建一个面向需求的问答清单，并提供覆盖核心需求维度的参考答案。
- LLM 回答这些问题，将自己的答案与参考答案比较，并根据不一致之处重写需求，形成一个对齐后的版本，把缺失或含糊的细节明确写出。
- 模型基于这个对齐后的需求生成代码，并用公开测试进行检查。
- 如果代码未通过，REA-Coder 会遮蔽需求中的关键语义片段，并要求 LLM 根据已生成的代码恢复这些内容。恢复错误会暴露代码与需求仍然不一致的位置。
- 这些新错误会被转成更新后的清单条目，然后重复“需求对齐 + 代码生成”的循环，直到代码通过测试或达到迭代上限。

## 结果
- 论文报告称，在测试的全部 20 个 模型-基准 组合上，REA-Coder 都优于 8 个基线：4 个 LLM × 5 个基准。
- 相比最强基线，平均提升分别为：**APPS 上 7.93%**、**CodeContests-raw 上 30.25%**、**CodeContests 上 26.75%**、**xCodeEval 上 8.59%**、**LiveCodeBench-Lite 上 8.64%**。
- 在 **Qwen3-Coder** 上，REA-Coder 在 **APPS** 上达到 **66.67% Pass@1**，在 **CodeContests-raw** 上达到 **40.61%**，在 **CodeContests** 上达到 **33.33%**，在 **xCodeEval** 上达到 **52.00%**，在 **LC-Lite** 上达到 **38.29%**。相对最强基线的提升分别为 **17.68%**、**76.34%**、**66.65%**、**16.41%** 和 **15.54%**。
- 在 **DeepSeek-v3.2** 上，REA-Coder 在 APPS、CodeContests-raw、CodeContests、xCodeEval 和 LC-Lite 上的 **Pass@1** 分别为 **81.67% / 67.27% / 61.82% / 70.33% / 62.86%**，相对最强基线的提升分别为 **9.87% / 24.71% / 24.39% / 8.20% / 11.12%**。
- 在 **GPT-5-mini** 上，其结果为 **85.00% / 73.33% / 60.61% / 71.33% / 62.86%**，提升分别为 **2.55% / 11.01% / 5.26% / 3.38% / 4.77%**。
- 在 **Gemini-3-Flash** 上，其结果为 **88.33% / 81.21% / 75.15% / 83.33% / 75.43%**，提升分别为 **1.63% / 8.93% / 10.71% / 6.38% / 3.13%**。论文还表示，只使用生成前的需求对齐，也能让第一次生成的代码相对 zero-shot 在 **APPS** 上提升 **210.44%**，在 **xCodeEval** 上提升 **344.67%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16198v1](http://arxiv.org/abs/2604.16198v1)
