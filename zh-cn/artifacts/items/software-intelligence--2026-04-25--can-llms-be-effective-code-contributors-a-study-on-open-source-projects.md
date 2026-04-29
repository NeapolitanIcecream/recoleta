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
本文测试当前 LLM 是否能为真实的开源 C 项目生成可直接提交的代码。作者在 8 个项目的 212 个真实提交上发现，成功率很不均衡，而且常常被编译错误、静态分析失败、测试失败、上下文限制，以及可能存在的训练集记忆所阻碍。

## 问题
- 本文研究 LLM 是否能在真实代码库中修复缺陷或添加小功能，并达到可以直接集成到生产代码中的水平。
- 这个问题很重要，因为 LLM 编写的代码已经很常见，但基准测试上的表现并不能说明模型是否能在大型代码库中与现有文件、构建规则、静态检查和测试套件配合工作。
- 作者还想衡量这些模型会如何失败：语法错误、修复错误、不安全代码、对大上下文处理较弱，以及成功可能来自记住训练样例的情况。

## 方法
- 作者构建了一个自动化评估框架：输入真实源文件和提示词，让 LLM 生成补丁，将补丁插入提交前的代码库，然后用 Clang 静态分析器和项目的测试套件进行检查。
- 他们评估了 8 个开源 C 项目的 212 个真实提交：其中 187 个是缺陷修复，25 个是功能增强，项目包括 FFmpeg、wolfSSL、jansson、Bison、Vsftpd、packcc、libhl 和 Collections-C。
- 测试的模型是 GPT-4o、Ministral3-14B 和 Qwen3-Coder-30B。
- 提示词由真实的提交信息和受影响的函数名组成，并提供父提交中被修改文件的内容作为上下文。
- 研究只使用单次生成；作者没有通过迭代提示反复重试。

## 结果
- 在不同项目上，总体成功率范围是 **0% 到 60%**，取决于项目。
- 在这 212 个提交中，LLM 生成的代码有 **2 到 32 个案例** 无法通过编译，具体取决于模型。
- 对于能够编译的代码，静态验证仍发现了 **9 到 18 个空指针解引用** 和 **9 到 72 个不安全类型转换**。
- 在作者能够运行测试的 **98 到 143 个提交** 中，测试套件通过率为 **71.8% 到 86.7%**，具体取决于模型和项目测试覆盖情况。
- 这些提交都很小，通常只有 **4 到 15 行代码**，但模型仍经常给出不完整修复、空补丁、错误修复、无关删除、未声明标识符，以及对 API 或结构体成员的错误假设。
- 论文认为，当上下文变得过大时，成功率会下降；模型在生成新代码时比做简单编辑更吃力；还有一些成功输出看起来更像是在重复训练中见过的代码改动，而不是根据代码库当前状态进行推理。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23340v1](http://arxiv.org/abs/2604.23340v1)
