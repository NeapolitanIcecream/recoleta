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
## 总结
REA-Coder 通过在写代码前后检查模型是否真正理解了需求，提升了 LLM 的代码生成效果。在 4 个 LLM 和 5 个基准上，它都优于强基线，包括推理增强和修复类方法；在更难的竞赛编程数据集上提升最大。

## 问题
- 现有代码生成方法通常默认 LLM 已经正确理解了提示词，然后把重点放在更好的推理或代码修复上。
- 论文认为，很多失败更早就发生了：模型误读了需求，后面的规划和修复都是在处理错误任务。
- 这会影响功能正确性，因为即使模型能写出语法正确的代码，也可能没有完成真正的需求。

## 方法
- REA-Coder 先根据题目描述构建一组面向需求的问题检查表，并为这些问题准备覆盖核心需求维度的参考答案。
- LLM 回答这些问题，再把自己的回答和参考答案比较，用不一致之处把需求改写成对齐后的版本，把缺失或含糊的信息明确写出来。
- 模型根据这个对齐后的需求生成代码，并用公开测试用例检查。
- 如果代码失败，REA-Coder 会把需求中的关键语义片段遮蔽起来，让 LLM 从生成的代码中恢复这些片段。恢复错误会指出代码和需求仍然不一致的地方。
- 这些新错误会变成更新后的检查表条目，然后对齐和生成的循环继续，直到代码通过测试或达到迭代上限。

## 结果
- 论文报告称，REA-Coder 在测试的全部 20 组模型-基准设置上都优于 8 个基线：4 个 LLM × 5 个基准。
- 相比最佳基线，平均提升分别是 **APPS 上 7.93%**、**CodeContests-raw 上 30.25%**、**CodeContests 上 26.75%**、**xCodeEval 上 8.59%** 和 **LiveCodeBench-Lite 上 8.64%**。
- 在 **Qwen3-Coder** 上，REA-Coder 在 **APPS** 上达到 **66.67% Pass@1**，在 **CodeContests-raw** 上达到 **40.61%**，在 **CodeContests** 上达到 **33.33%**，在 **xCodeEval** 上达到 **52.00%**，在 **LC-Lite** 上达到 **38.29%**。相对最强基线的提升分别是 **17.68%**、**76.34%**、**66.65%**、**16.41%** 和 **15.54%**。
- 在 **DeepSeek-v3.2** 上，REA-Coder 在 APPS、CodeContests-raw、CodeContests、xCodeEval 和 LC-Lite 上分别得到 **81.67% / 67.27% / 61.82% / 70.33% / 62.86% Pass@1**，相对最佳基线的提升为 **9.87% / 24.71% / 24.39% / 8.20% / 11.12%**。
- 在 **GPT-5-mini** 上，它分别得到 **85.00% / 73.33% / 60.61% / 71.33% / 62.86%**，提升为 **2.55% / 11.01% / 5.26% / 3.38% / 4.77%**。
- 在 **Gemini-3-Flash** 上，它分别得到 **88.33% / 81.21% / 75.15% / 83.33% / 75.43%**，提升为 **1.63% / 8.93% / 10.71% / 6.38% / 3.13%**。论文还指出，只做生成前的需求对齐，就能把首个生成代码相对 zero-shot 的效果提升 **APPS 上 210.44%**、**xCodeEval 上 344.67%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16198v1](http://arxiv.org/abs/2604.16198v1)
