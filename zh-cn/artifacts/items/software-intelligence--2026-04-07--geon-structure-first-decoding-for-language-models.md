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
## 总结
GEON 改变了解码方式：语言模型先从结构上有效的选项里选择，再选下一个 token。根据给出的代码生成示例和 10 任务基准描述，它声称能让 Python 任务的功能正确性更好，而普通的 token 解码经常写出看起来合理但实际错误的代码。

## 问题
- 标准语言模型解码按概率选下一个 token，这会生成看起来合理但逻辑有误或结构不完整的代码。
- 对代码生成来说，语法正确还不够，输出还需要结构匹配、可接受的后续续写，以及能通过任务的行为。
- 这段内容认为，很多代码错误来自没有结构约束的解码，所以即使模型知道任务模式，也会生成错误程序。

## 方法
- GEON 在 token 选择前加入结构解码层。
- 它把候选 token 映射到等价类，在结构约束下检查这些等价类，并移除不符合条件的选项。
- 经过这一步过滤后，解码器只会从剩下的有效集合里采样或选择 token。
- 这种方法想在生成过程中直接保证语法闭合、控制流结构一致，以及其他有效性规则，而不是在生成后修补输出。
- 简单说：先确定允许的结构，再选择一个适合这个结构的 token。

## 结果
- 这段内容描述了对 10 个 Python 代码生成任务的评估：factorial、sum_list、max_element、count_vowels、reverse_string、is_even、is_sorted、count_positive、first_char 和 square_list。
- 它还提到一个较小的 3 任务 harness，包含 factorial、sum_list 和 max_element。
- 对于基线 token 解码和 GEON，这段内容都说输出是语法有效的 Python。
- 声称的差异出现在结构和语义层面：基线解码经常生成看起来合理但实际错误的程序，而 GEON 在全部 10 个任务上都给出了稳定的语义正确性。
- 这段内容没有给出精确的量化指标：没有通过率、准确率、样本数、模型名称或数值上的基线对比。
- 具体示例说明了它想达到的效果：GEON 会阻止结构无效的续写，比如不匹配的括号和错误的分支结构，作者把这和更好的功能正确性联系起来。

## Problem

## Approach

## Results

## Link
- [https://github.com/singhalpm-hub/geon-decoder](https://github.com/singhalpm-hub/geon-decoder)
