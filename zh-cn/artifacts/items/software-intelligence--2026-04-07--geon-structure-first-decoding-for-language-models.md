---
source: hn
url: https://github.com/singhalpm-hub/geon-decoder
published_at: '2026-04-07T22:51:23'
authors:
- singhalpm
topics:
- code-generation
- structured-decoding
- language-models
- program-synthesis
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# GEON: Structure-first decoding for language models

## Summary
## 摘要
GEON 改变了解码过程：语言模型在选择下一个 token 之前，先从结构上有效的选项中进行筛选。根据给出的代码生成示例和 10 项任务基准测试说明，其宣称的提升是：在 Python 任务上获得更好的函数正确性，而普通 token 解码经常会生成看起来合理但实际错误的代码。

## 问题
- 标准语言模型解码按概率选择下一个 token，这会生成看起来合理、但逻辑错误或结构不完整的代码。
- 对代码生成来说，仅有语法正确还不够；输出还需要结构匹配、后续展开合法，并且行为能通过任务要求。
- 论文认为这一点很重要，因为许多代码错误并不是模型不知道任务模式，而是解码时缺少结构约束，因此即使模型知道模式，也会生成错误程序。

## 方法
- GEON 在 token 选择之前加入了一层结构解码层。
- 它将候选 token 映射到等价类，在结构约束下检查这些类，并移除不合法的选项。
- 完成这一步过滤后，解码器才会只从剩余的有效集合中采样或选择 token。
- 该方法的目标是在生成过程中直接保证语法闭合、一致的控制流结构和其他有效性规则，而不是在生成后再修复输出。
- 简单说，就是先确定允许的结构，再选择符合该结构的 token。

## 结果
- 摘录描述了对 10 个 Python 代码生成任务的评估：factorial、sum_list、max_element、count_vowels、reverse_string、is_even、is_sorted、count_positive、first_char 和 square_list。
- 文中还提到一个较小的 3 任务测试集，包括 factorial、sum_list 和 max_element。
- 对于基线 token 解码和 GEON，摘录都表示输出在语法上是有效的 Python。
- 宣称的差异出现在结构和语义层面：基线解码经常生成看起来合理但实际错误的程序，而 GEON 在全部 10 个任务上都实现了一致的语义正确性。
- 摘录没有给出精确的量化指标：没有通过率、准确率、样本数量、模型名称，也没有数值化的基线对比。
- 具体示例展示了该方法想达到的效果：GEON 会阻止结构上无效的后续展开，例如不匹配的括号和错误的分支结构；作者据此认为它能提升函数正确性。

## Problem

## Approach

## Results

## Link
- [https://github.com/singhalpm-hub/geon-decoder](https://github.com/singhalpm-hub/geon-decoder)
