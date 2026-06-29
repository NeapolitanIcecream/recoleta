---
source: arxiv
url: http://arxiv.org/abs/2604.22601v1
published_at: '2026-04-24T14:28:10'
authors:
- Md Erfan
- Md Kamal Hossain Chowdhury
- Ahmed Ryan
- Md Rayhanur Rahman
topics:
- formal-verification
- dafny
- code-generation
- open-weight-llms
- benchmark-datasets
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# From Natural Language to Verified Code: Toward AI Assisted Problem-to-Code Generation with Dafny-Based Formal Verification

## Summary
## 总结
本文研究开源权重 LLM 是否能把自然语言编程题转成**经过验证的 Dafny 代码**，而不是可能出错的普通代码。作者提出一个 60 题基准，并显示在抽样任务上，验证器反馈和方法签名能把成功率从接近零提升到较高的验证通过率。

## 问题
- LLM 可以写出看起来合理的代码，但代码里常有逻辑错误或幻觉；当软件需要正确性保证时，这个问题很关键。
- 形式化验证可以证明代码符合规格，但要写出 Dafny 规格、循环不变式和证明标注并不容易，而且往往比写程序本身更费力。
- 自然语言需求有歧义，而 Dafny 训练数据很少，所以把自然语言直接映射到经过验证的代码是一个难度很高的合成任务。

## 方法
- 作者构建了 **NL2VC-60**，一个包含 60 个手工编写 Dafny 解法的数据集，题目来自复杂的 UVa Online Judge 问题，且自然语言描述比之前的 Dafny 基准更长、更详细。
- 他们在 **11 个随机抽取的问题集** 上评估 **7 个开源权重 LLM**，使用三种提示设置：**无上下文提示**、提供方法结构的 **签名提示**、以及把 Dafny 验证器错误反馈给模型并进行迭代修复的 **自修复提示**。
- 他们使用 **Dafny** 作为验证语言，因此模型必须同时生成可执行代码和证明所需的形式化标注，例如契约和循环不变式。
- 他们加入 **uDebug** 测试集来发现 **空洞验证**，也就是代码靠很弱或很平凡的规格通过验证器，但并没有真正解决问题。
- 他们还整理了一个面向 Dafny 的编译和验证错误数据集，用来研究模型的失败模式。

## 结果
- 在 **无上下文提示** 下，论文报告测试模型几乎全部失败。
- 在结构引导和修复之后，性能明显提升：**Gemma 4-31B** 在抽样评估中达到 **90.91% 的验证成功率**。
- **GPT-OSS 120B** 在得到 **签名引导反馈** 后，从 **0%** 提升到 **81.82% 的验证成功率**。
- 论文认为，当提供验证器引导的迭代和结构锚点后，开源权重 LLM 现在可以在复杂算法任务上合成经过形式化验证的 Dafny 程序。
- 评估使用了 **60 个基准问题**、**11 个抽样问题集**、**7 个开源权重 LLM**，并通过 **形式化证明加 uDebug 功能测试**进行双重检查。
- 摘录没有给出每个模型的完整结果表、整个数据集的平均值，也没有提供除上述成功率之外与先前已发表基线的直接数值比较。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22601v1](http://arxiv.org/abs/2604.22601v1)
