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
## 摘要
这篇论文研究开放权重 LLM 是否能把自然语言编程题转成**经过验证的 Dafny 代码**，而不是只生成可能出错的普通代码。论文提出了一个包含 60 道题的基准，并显示在抽样任务上，验证器反馈加上方法签名可以把成功率从接近零提高到较高的验证通过率。

## 问题
- LLM 可以写出看起来合理的代码，但这些代码常常包含逻辑错误或幻觉内容；当软件需要正确性保证时，这一点很重要。
- 形式化验证可以证明代码符合规格，但编写 Dafny 规格、循环不变式和证明注释很难，而且往往比写程序本身更费力。
- 自然语言需求有歧义，而 Dafny 训练数据又很少，因此把自然语言直接映射为已验证代码是一个困难的合成任务。

## 方法
- 作者构建了 **NL2VC-60**，这是一个包含 60 个手工编写 Dafny 解答的数据集，题目来自复杂的 UVa Online Judge 问题，其自然语言描述比以往 Dafny 基准更长也更详细。
- 他们在 **11 个随机选取的问题集**上评估了**7 个开放权重 LLM**，使用三种提示设置：**无上下文提示**、提供方法结构的**签名提示**，以及把 Dafny 验证器错误反馈给模型进行迭代修复的**自愈提示**。
- 他们使用 **Dafny** 作为验证语言，因此模型必须同时生成可执行代码和证明所需的形式化注释，例如契约和循环不变式。
- 他们加入了 **uDebug** 测试套件，用来发现**空洞验证**：代码虽然凭借弱或无意义的规格通过验证器，但并没有真正解决问题。
- 他们还整理了一个 Dafny 特有的编译和验证错误数据集，用来研究模型的失败模式。

## 结果
- 在**无上下文提示**下，论文报告说，测试的各个模型几乎全部失败。
- 加入结构引导和修复后，性能明显提升：**Gemma 4-31B** 在抽样评估中达到 **90.91% 的验证成功率**。
- **GPT-OSS 120B** 在获得**签名引导反馈**后，验证成功率从 **0%** 提高到 **81.82%**。
- 论文认为，当提供验证器引导的迭代和结构锚点时，开放权重 LLM 现在已经能够在复杂算法任务上合成经过形式化验证的 Dafny 程序。
- 评估覆盖 **60 道基准题**、**11 个抽样问题集**、**7 个开放权重 LLM**，并通过**形式化证明加 uDebug 功能测试**进行双重检查。
- 摘要片段没有给出完整的各模型结果表、整个数据集上的平均值，或与以往已发表基线的直接数值对比；除了上面报告的成功率之外，没有更多具体数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22601v1](http://arxiv.org/abs/2604.22601v1)
