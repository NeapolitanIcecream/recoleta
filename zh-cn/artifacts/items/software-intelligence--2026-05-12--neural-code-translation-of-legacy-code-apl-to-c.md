---
source: arxiv
url: https://arxiv.org/abs/2605.13896v1
published_at: '2026-05-12T12:11:33'
authors:
- Abdulrahman Ramadan
- Hanen Borchani
- Iben Lilholm
- Mikkel Almind
- Allan Peter Engsig-Karup
topics:
- code-translation
- legacy-code
- apl-to-csharp
- code-intelligence
- llm-fine-tuning
- program-repair
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Neural Code Translation of Legacy Code: APL to C#

## Summary
## 摘要
这篇论文研究用 LLM 将遗留 APL 代码翻译成 C#。主要贡献包括专门的 APL 到 C# 数据集、带引导的翻译方法，以及用于检验功能正确性的编译并运行评估流水线。

## 问题
- APL 简洁、面向数组、动态类型，并大量使用符号字形；C# 是静态类型，写法更冗长。直接翻译通常需要处理类型映射、重载、循环、边界检查，以及从 APL 的 1 基索引转换到 C# 的 0 基索引。
- 随着熟悉 APL 的人员减少，遗留 APL 系统维护难度上升，因此自动迁移到 C# 可以减少人工重写工作。
- 公开的 APL 到 C# 平行语料很少，这限制了监督训练和标准基准评估。

## 方法
- 作者将直接微调的 APL 到 C# 翻译与三种带引导的方法进行比较：通过自然语言描述进行中介、检索增强翻译，以及使用编译器和测试反馈的迭代修复。
- 他们构建了对齐的 APL 和 C# 数据集：800 对人工整理的基础样本、143 个来自生产环境的工具函数、320 对 Rosetta Code 样本，以及 45 个 APL 惯用写法。
- 他们使用 LoRA 和 8-bit 量化微调开放权重模型，训练样本为 1,066 个，序列长度为 2,048 token。
- 他们用一个 F# 工具解析 APL 头部来生成 C# 方法签名，然后在提示中加入这些签名，以帮助模型处理 C# 类型。
- 评估会编译生成的 C#，并用输入输出测试运行；迭代方法最多重试 5 次，每次把编译器错误、期望输出、实际输出和此前尝试放入上下文。

## 结果
- 提供的摘录没有包含主 APL 到 C# 任务的定量翻译准确率、编译通过率或执行通过率。
- 论文报告了数据集规模：Dataset A 有 800 对样本，Dataset B 有 143 个来自生产环境的函数，Dataset C 有 320 对 Rosetta Code 样本，Dataset I 有 45 个惯用写法，训练语料有 1,066 个样本。
- 面向生产环境的测试使用 Dataset B 的测试划分，其中有 49 个样本。
- 分词器分析显示，Qwen3-32B 的 APL 单 token 率为 0.715，每个字形平均 1.284 个 token，每个样本平均 262.274 个 token，往返失败次数为 0。
- Gemma-4-31b-it 的 APL 单 token 率为 0.671，每个字形平均 1.656 个 token，每个样本平均 277.475 个 token，往返失败次数为 1；Deepseek-Coder-6.7b-Instruct 因错误处理 APL 除号而出现 61 次往返失败。
- 摘要称，增加上下文和引导能比直接翻译提升模型性能，但摘录没有给出衡量该提升所需的准确率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13896v1](https://arxiv.org/abs/2605.13896v1)
