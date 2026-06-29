---
source: arxiv
url: http://arxiv.org/abs/2604.23340v1
published_at: '2026-04-25T15:00:14'
authors:
- Chun Jie Chong
- Muyeed Ahmed
- Zhihao
- Yao
- Iulian Neamtiu
topics:
- llm-code-generation
- open-source-software
- code-repair
- software-testing
- static-analysis
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Can LLMs be Effective Code Contributors? A Study on Open-source Projects

## Summary
## 摘要
这篇论文测试当前的 LLM 是否能为真实的开源 C 项目生成可直接提交的代码。在 8 个项目的 212 个真实提交上，作者发现成功率差异很大，而且经常被编译错误、静态分析失败、测试失败、上下文限制，以及可能的训练集记忆所阻断。

## 问题
- 论文研究的是，LLM 是否能在真实仓库里修复 bug 或添加小功能，并达到可以直接合并进生产代码的程度。
- 这很重要，因为 LLM 写代码已经很常见，但基准测试并不能说明模型是否能在大型代码库里和现有文件、构建规则、静态检查以及测试套件一起工作。
- 作者还想测量这些模型会怎么失败：语法错误、错误修复、不安全代码、对大上下文的处理能力弱，以及成功是否可能来自记住了训练样本中的代码改动。

## 方法
- 作者构建了一个自动化评估框架，输入真实源码文件和提示词，要求 LLM 生成补丁，把补丁应用到提交前的代码库里，然后用 Clang 静态分析器和项目的测试套件检查。
- 他们评估了 8 个开源 C 项目的 212 个真实提交：187 个 bug 修复和 25 个功能增强，项目包括 FFmpeg、wolfSSL、jansson、Bison、Vsftpd、packcc、libhl 和 Collections-C。
- 测试的模型是 GPT-4o、Ministral3-14B 和 Qwen3-Coder-30B。
- 提示词由真实提交信息、受影响的函数名，以及父提交中的变更文件上下文组成。
- 这项研究只使用一次生成，不会用迭代式提示重试。

## 结果
- 在不同项目上，总体成功率介于 **0% 到 60%** 之间。
- 在这 212 个提交里，LLM 生成的代码按模型不同，有 **2 到 32 个** 不能编译。
- 对于能编译的代码，静态验证仍然发现了 **9 到 18 个空指针解引用** 和 **9 到 72 个不安全转换**。
- 在作者能够运行测试的 **98 到 143 个提交** 中，测试套件通过率介于 **71.8% 到 86.7%**，取决于模型和项目覆盖范围。
- 这些提交都很小，通常只有 **4 到 15 行代码**，但模型仍然经常生成部分修复、空补丁、错误修复、无关删除、未声明标识符，以及对 API 或结构体成员的错误假设。
- 论文认为，当上下文变大时，成功率会下降；模型生成新代码的能力比简单编辑差；而一些成功输出看起来像是复述训练中见过的代码改动，而不是基于仓库状态进行推理。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23340v1](http://arxiv.org/abs/2604.23340v1)
